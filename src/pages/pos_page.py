from playwright.sync_api import Page, expect


class POSPage:
    def __init__(self, page: Page):
        self.page = page

        self.select_customer_button = page.get_by_role("button", name="Select Customer")
        self.customer_dialog = page.get_by_role("dialog", name="Select Customer")
        self.search_customer_input = self.customer_dialog.get_by_role("textbox")
        self.save_customer_button = page.get_by_role("button", name="Save")

        self.search_product_button = page.get_by_role("button", name="Search Products")
        self.product_cards = page.locator(".card-body")

        self.promotion_button = page.get_by_role("button", name="Promotion")
        self.promotion_checkbox = page.locator(
            ".modal-body input.form-check-input"
        ).first

        self.close_popup = page.get_by_role("button", name="Close")
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.payment_button = page.locator(".checkout-action")

        self.payout_confirm_button = page.get_by_label("Confirm Payment").get_by_role(
            "button", name="Confirm"
        )

        self.saleman_button = page.get_by_role("button", name="back Select Sales")
        self.saleman = page.locator(
            ".form-outline input.form-control[type='text'][required]"
        )
        self.save_button = page.get_by_role("button", name="Save")

        self.receipt = page.get_by_text("RECEIPT")
        self.receipt_table_rows = page.locator("table tbody tr")
        self.void_transaction_dropdown = (
            page.get_by_role("list").locator("a").filter(has_text="Void")
        )
        self.void_textarea = page.locator("textarea.form-control")
        self.void_success_alert = page.locator("#layout-container").get_by_text(
            "This bill has been voided"
        )
        self.void_close_button = page.locator("#layout-container").get_by_text(
            "Close", exact=True
        )

        self.branch = page.get_by_role("combobox", name="Please select Branch")
        self.branch_code = page.get_by_role("option", name="Test")

    def ensure_branch(self):
        self.branch.click()

        selected = (
            self.page.locator(
                '[role="option"][aria-selected="true"] .select-option-text'
            ).text_content()
            or ""
        )

        if (
            "TMES BR : 02" not in selected
            and "Test" not in selected
            and "TMES HQ (Branch)" not in selected
        ):
            self.page.get_by_role("option", name="Test").click()

    def should_skip_before_pos(tier):
        expected = tier.get("expected")
        void_cfg = tier.get("void")

        if not expected or all(v is None for v in expected.values()):
            if isinstance(void_cfg, dict):
                return None
            return "NO API Checking"

        return None

    def customer_item(self, display: str):
        return self.page.get_by_text(display)

    def select_saleman(self):
        self.saleman_button.click()
        self.saleman.fill("test")
        self.save_button.click()

    def open_customer_dialog(self):
        expect(self.select_customer_button).to_be_visible(timeout=30000)
        self.select_customer_button.click()

    def search_customer(self, customer_id: str):
        expect(self.search_customer_input).to_be_visible(timeout=30000)
        self.search_customer_input.fill(customer_id)

    def choose_customer(self, customer_id: str):
        item = self.customer_item(customer_id).first
        self.search_customer_input.click()
        expect(item).to_be_visible(timeout=30000)
        item.click()
        expect(self.save_customer_button).to_be_visible(timeout=30000)
        self.save_customer_button.click()

    def select_customer(self, customer_id: str):
        self.open_customer_dialog()
        self.search_customer(customer_id)
        self.choose_customer(customer_id)

    def open_product_search(self):
        self.page.wait_for_load_state("networkidle")
        expect(self.search_product_button).to_be_visible(timeout=5000)
        self.search_product_button.click()

        modal = self.page.locator(".modal-dialog")
        expect(modal).to_be_visible(timeout=10000)

        expect(self.product_cards.first).to_be_visible(timeout=10000)

    def add_product(self, product_name: str, times: int = 1):
        self.open_product_search()

        card = self.product_cards.filter(has_text=product_name).first
        expect(card).to_be_visible(timeout=10000)

        add_button = card.get_by_role("button", name="ADD TO CART")
        expect(add_button).to_be_visible(timeout=5000)

        for _ in range(times):
            add_button.click()

        expect(self.close_popup).to_be_visible(timeout=5000)
        self.close_popup.click()

        expect(self.page.locator(".modal-dialog")).not_to_be_visible(timeout=10000)

    def wait_promotion_modal_ready(self):
        expect(self.confirm_button).to_be_visible(timeout=5000)

    def uncheck_all_promotions(self):
        self.wait_promotion_modal_ready()

        checkboxes = self.page.locator(".modal-body input.form-check-input")

        if not checkboxes.first.is_visible():
            self.confirm_button.click()
            return

        total = checkboxes.count()
        for i in range(total):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                cb.uncheck(force=True)

        self.confirm_button.click()

    def open_receipt(self):
        expect(self.receipt).to_be_visible(timeout=5000)
        self.receipt.click()
        expect(self.receipt_table_rows.first).to_be_visible(timeout=10000)

    def void_transaction(self, row_index: int, reason: str):
        row = self.receipt_table_rows.nth(row_index)

        action_cell = row.locator("td").first
        action_cell.click()

        expect(self.void_transaction_dropdown).to_be_visible(timeout=5000)
        self.void_transaction_dropdown.click()

        expect(self.void_textarea).to_be_visible(timeout=5000)
        self.void_textarea.fill(reason)

        expect(self.confirm_button).to_be_enabled(timeout=5000)
        self.confirm_button.click()

        expect(self.void_success_alert).to_be_visible(timeout=10000)
        self.void_close_button.click()

    def proceed_to_payment(self):
        self.promotion_button.click()

        self.uncheck_all_promotions()

        self.payment_button.click()
        self.confirm_button.click()

        with self.page.context.expect_page(timeout=80000) as receipt_page_info:
            self.payout_confirm_button.click()

        receipt_page = receipt_page_info.value
        receipt_page.wait_for_load_state(timeout=80000)
        print(receipt_page.url)
        receipt_page.close()

    def create_orders(self, customer_id, product_name, rounds):
        if not rounds:
            return

        for r in rounds:
            times = r.get("times", 0)
            if times > 0:
                self.select_saleman()
                self.select_customer(customer_id)
                self.add_product(product_name, times)
                self.proceed_to_payment()

    def void_if_needed(self, void_config):
        if not isinstance(void_config, dict):
            return

        row_index = void_config.get("row", 0)
        reason = void_config.get("reason", "Auto void by test")

        self.open_receipt()
        self.void_transaction(row_index, reason)
