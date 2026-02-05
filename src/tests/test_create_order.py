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
    product_name = products[tier["product"]]["name"]
    rounds = tier.get("rounds", [])
    expected = tier.get("expected")

    pos.ensure_branch()
    pos.create_orders(
        customer_id=customer_id,
        product_name=product_name,
        rounds=rounds,
    )

    pos.void_if_needed(tier.get("void"))

    if SKIP_CRM_ASSERT:
        print("PASS without CRM API check")
        return

    if not expected:
        print("PASS without CRM check (no expected in yaml)")
        return

    wait_crm_spending_updated(
        crm=crm_client,
        member_id=customer_id,
        wallet_code=WALLET_CODE,
        expected_amount=expected["total_spending_current_period"],
    )

    member = crm_client.get_member(customer_id, WALLET_CODE)

    assert member["member_id"] == customer_id
    assert_member_spending(member, expected)
