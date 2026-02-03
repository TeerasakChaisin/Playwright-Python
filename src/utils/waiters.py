import time


def wait_until(condition_fn, timeout=60, interval=2, error_msg="Timeout"):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return
        time.sleep(interval)
    raise AssertionError(error_msg)


def wait_crm_spending_updated(
    crm,
    member_id: str,
    wallet_code: str,
    expected_amount: float,
    timeout: int = 60,
):
    def condition():
        member = crm.get_member(member_id, wallet_code)
        return member["total_spending_current_period"] >= expected_amount

    wait_until(
        condition_fn=condition,
        timeout=timeout,
        error_msg=f"CRM spending not updated for member {member_id}",
    )
