import os
import pytest
from playwright.sync_api import Page

from pages.pos_page import POSPage
from apis.customer_wallet_detail import customer_wallet_detail
from utils.data_loader_pos import get_customers, get_products, get_tiers
from utils.waiters import wait_crm_spending_updated
from utils.pos_checking import assert_member_spending


WALLET_CODE = "GCTHB"


def is_true_env(name: str) -> bool:
    return os.getenv(name, "").lower() in {"1", "true", "yes"}


SKIP_CRM_ASSERT = is_true_env("SKIP_CRM_ASSERT")


@pytest.fixture(scope="session")
def crm_client():
    return customer_wallet_detail()


@pytest.fixture(scope="session")
def customers():
    return get_customers()


@pytest.fixture(scope="session")
def products():
    return get_products()


tiers = get_tiers()


@pytest.mark.parametrize(
    "tier",
    tiers,
    ids=[t["name"] for t in tiers],
)
def test_tier_spending_flow(
    pos_page: Page,
    tier: dict,
    customers: dict,
    products: dict,
    crm_client,
):
    pos = POSPage(pos_page)

    customer_id = customers[tier["customer"]]["id"]

    pos.ensure_branch()

    if "orders" in tier:
        orders = tier["orders"]
    else:
        orders = [
            {
                "items": [
                    {
                        "product": products[tier["product"]]["name"],
                        "rounds": tier.get("rounds", []),
                        "discount": tier.get("discount"),
                    }
                ],
                "promotions": tier.get("promotions"),
                "void": tier.get("void"),
            }
        ]

    for order in orders:
        items = []

        for item in order.get("items", []):
            items.append(
                {
                    "product": products[item["product"]]["name"],
                    "rounds": item.get("rounds", []),
                    "discount": item.get("discount"),
                }
            )

        promotions = order.get("promotions")

        pos.create_order_items(
            customer_id=customer_id,
            items=items,
            promotions=promotions,
        )

        pos.void_if_needed(order.get("void"))

    expected = tier.get("expected")

    if SKIP_CRM_ASSERT or not expected:
        return

    wait_crm_spending_updated(
        crm=crm_client,
        member_id=customer_id,
        wallet_code=WALLET_CODE,
        expected_amount=expected["total_spending_current_period"],
    )

    member = crm_client.get_member(customer_id, WALLET_CODE)
    assert_member_spending(member, expected)

