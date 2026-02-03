import pytest
from utils.assert_amount import assert_amount_equal


def should_skip_before_pos(tier):
    times = tier.get("times")
    expected = tier.get("expected")
    void = tier.get("void")

    if times == 0 and isinstance(void, dict):
        return None

    if not expected or all(v is None for v in expected.values()):
        return "No expected defined"

    return None


def assert_member_spending(member: dict, expected: dict):
    assert_amount_equal(
        member["total_spending_current_period"],
        expected["total_spending_current_period"],
    )
    assert_amount_equal(
        member["spending_to_next_tier"],
        expected["spending_to_next_tier"],
    )
    assert_amount_equal(
        member["spending_to_keep_tier"],
        expected["spending_to_keep_tier"],
    )
