import re
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
        self.confirm_button = page.get_by_role("button", name="Confirm")
        self.payment_button = page.locator(".checkout-action")

        self.close_button = page.get_by_role("button", name="Close")

        self.payout_confirm_button = page.get_by_label("Confirm Payment").get_by_role(
            "button", name="Confirm"
        )

        self.saleman_button = page.get_by_role("button", name="back Select Sales")
        self.saleman = page.locator(".form-outline input.form-control[type='text'][required]")
        self.save_button = page.get_by_role("button", name="Save")

        self.branch = page.get_by_role("combobox", name="Please select Branch")

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

        self.privilege = page.get_by_role("button", name="Privilege")

        self.coupon = page.get_by_text("COUPON", exact=True)
        self.coupon_modal = page.locator("#couponModal")
        self.coupon_textbox = self.coupon_modal.locator("input[type='text']")
        self.close_coupon = page.locator("#couponModal").get_by_role("button", name="Close")

        self.redeem = page.get_by_text("REDEEM")
        self.redeem_card = page.locator(".redeem-card")
        self.confirm_redeem = page.get_by_role("heading", name="Confirm Redeem")
        
        self.bill_discount_modal = page.locator("#billDiscountModal")

        self.bill_discount = page.get_by_role("button", name="Bill Discount")
        self.bill_discount_type = self.bill_discount_modal.locator(".select-input")
        self.bill_discount_amount = self.bill_discount_modal.locator("input[type='text']")


    def ensure_branch(self):
        self.branch.click()

        selected = (
            self.page.locator(
                '[role="option"][aria-selected="true"] .select-option-text'
            ).text_content()
            or ""
        )

        if "Test" not in selected and "TMES BR : 02" not in selected:
            self.page.get_by_role("option", name="Test").click()

    def select_saleman(self):
        self.saleman_button.click()
        self.saleman.fill("test")
        self.save_button.click()
    
    def customer_item(self, display: str):
        return self.page.get_by_text(display)

    def choose_customer(self, customer_id: str):
        item = self.customer_item(customer_id).first
        self.search_customer_input.click()
        expect(item).to_be_visible(timeout=30000)
        item.click()
        expect(self.save_customer_button).to_be_visible(timeout=30000)
        self.save_customer_button.click()

    def select_customer(self, customer_id: str):
        self.select_customer_button.click()
        self.search_customer_input.fill(customer_id)
        self.choose_customer(customer_id)

    def open_product_search(self):
        self.search_product_button.click()
        expect(self.page.locator(".modal-dialog")).to_be_visible(timeout=10000)

    def add_product(self, product_name: str, times: int):
        self.open_product_search()

        card = self.product_cards.filter(has_text=product_name).first
        add_button = card.get_by_role("button", name="ADD TO CART")

        for _ in range(times):
            add_button.click()

        self.close_button.click()
        expect(self.page.locator(".modal-dialog")).not_to_be_visible(timeout=10000)

    def cart_line_by_product(self, product_name: str):
        return self.page.locator(".cart-pos-product-line").filter(
            has_text=product_name
        ).last

    def apply_discount(self, product_name: str, discount: dict | None):
        if not discount:
            return

        line = self.cart_line_by_product(product_name)

        discount_type_input = line.locator(
            ".cart-pos-product-line-action-discount-type input.select-input"
        )
        discount_amount_input = line.locator(
            ".cart-pos-product-line-action-discount input[type='number']"
        )

        discount_type_input.click()

        option = self.page.locator(".select-option-text").filter(
            has_text=str(discount["type"])
        ).first
        option.click()

        discount_amount_input.fill(str(discount["amount"]))

    def uncheck_all_promotions(self):
        checkboxes = self.page.locator(".modal-body input.form-check-input")

        total = checkboxes.count()
        for i in range(total):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                cb.uncheck(force=True)

    def check_promotions_by_name(self, promotions: list | None):
        if not promotions:
            return

        for name in promotions:
            container = self.page.locator(".promotion-container").filter(
                has_text=name
            ).first

            if not container.is_visible():
                continue

            checkbox = container.locator("input.form-check-input")

            if not checkbox.is_checked():
                checkbox.check(force=True)

    def open_privilege(self):
            self.privilege.click()

    def apply_redeem(self, points):
        if points is None:
            return

        self.redeem.click()

        card = self.redeem_card.filter(has_text=str(points)).first
        expect(card).to_be_visible()
        card.click()

        expect(self.confirm_redeem).to_be_visible()
        self.confirm_button.click()

    def apply_coupon(self, coupon):
        if coupon is None:
            return

        self.coupon.click()
        expect(self.coupon_modal).to_be_visible()

        self.coupon_textbox.fill(str(coupon))
        self.confirm_button.first.click()
        self.confirm_button.nth(1).click()

    def apply_privileges(self, privileges: dict | None):
        if not privileges:
            return

        coupon = privileges.get("coupon")
        redeem_points = privileges.get("redeem_points")

        if coupon:
            self.open_privilege()
            self.apply_coupon(coupon)

        if redeem_points:
            self.open_privilege()
            self.apply_redeem(redeem_points)

    def apply_bill_discount(self, discount: dict | None):
        if not discount:
            return

        discount_type = discount.get("type")
        amount = discount.get("amount")

        self.bill_discount.click()
        expect(self.bill_discount_modal).to_be_visible()

        self.bill_discount_type.click()
        self.page.get_by_text(discount_type, exact=True).click()

        self.bill_discount_amount.fill(str(amount))

        self.confirm_button.click()

    def _get_cart_rows(self):
        return self.page.locator(".cart-pos-product-line")

    def _parse_money(self, text: str) -> float:
        if not text:
            return 0.0

        cleaned = re.sub(r"[^\d.\-]", "", text)
        return float(cleaned or 0)


    def _get_price_from_row(self, row):
        current = row.locator(
            ".cart-pos-product-line-detail-defualt-price-current"
        )

        if current.count() > 0:
            return self._parse_money(current.inner_text())

        sale = row.locator(
            ".cart-pos-product-line-detail-defualt-price-sale"
        )

        return self._parse_money(sale.inner_text())

    def _calculate_row_total(self, price, qty, discount_amount, discount_type, ui_total=None):
        subtotal = price * qty
        dtype = (discount_type or "").strip().lower()

        if "free" in dtype:
            return ui_total

        if not discount_amount:
            return subtotal

        if "%" in dtype:
            return subtotal - (subtotal * discount_amount / 100)

        return subtotal - (discount_amount * qty)

    def assert_cart_totals(self):
        rows = self._get_cart_rows()
        count = rows.count()

        assert count > 0, "Cart is empty"

        sum_rows = 0

        for i in range(count):
            row = rows.nth(i)

            name = row.locator(
                ".cart-pos-product-line-detail-name"
            ).inner_text().strip()

            price = self._get_price_from_row(row)

            qty = int(
                row.locator("input[type='number']").first.input_value() or 0
            )

            discount_amount = float(
                row.locator("input[type='number']").nth(1).input_value() or 0
            )

            discount_type = row.locator(
                ".cart-pos-product-line-action-discount-type input.select-input"
            ).input_value()

            ui_total = self._parse_money(
                row.locator(
                    ".cart-pos-product-line-action-total"
                ).inner_text()
            )

            expected = round(
                self._calculate_row_total(
                    price,
                    qty,
                    discount_amount,
                    discount_type,
                    ui_total,
                ),
                2,
            )

            actual = round(ui_total, 2)

            print(
                f"price={price} qty={qty}"
                f"discount={discount_amount} type={discount_type}"
                f"expected={expected} actual={actual}"
            )

            assert expected == actual, (
                f"{name} expected {expected} but got {actual}"
            )

            sum_rows += actual

        ui_total = self._parse_money(
            self.page.locator(
                ".cart-pos-total-result-price-detail"
            ).inner_text()
        )

        expected_total = round(sum_rows, 2)
        actual_total = round(ui_total, 2)

        print(
            f"Expect TOTAL | expected={expected_total} actual={actual_total}"
        )

        assert expected_total == actual_total, (
            f"Expect total mismatch {expected_total} != {actual_total}"
        )

    def assert_checkout_totals(self):
        container = self.page.locator(".checkout-pos-calculate")
        lines = container.locator(".checkout-pos-calculate-line")

        count = lines.count()
        values = {}
        vat_rate = 0

        for i in range(count):
            line = lines.nth(i)

            name = line.locator(".checkout-pos-calculate-name").inner_text().strip()
            value = self._parse_money(
                line.locator(".checkout-pos-calculate-content").inner_text()
            )

            values[name] = value

            m = re.search(r"VAT\s*(\d+)%", name)
            if m:
                vat_rate = float(m.group(1))

        total = values.get("Sub Grand Total :")
        pretax = values.get("Pretax Total :")
        vat = 0

        if vat_rate > 0:
            vat = values.get(f"VAT {int(vat_rate)}% :", 0)
            expected_vat = round(total * vat_rate / (100 + vat_rate), 2)
            expected_pretax = round(total - expected_vat, 2)
        else:
            expected_vat = 0
            expected_pretax = total

        print(
            f"Checkout | rate={vat_rate}% | "
            f"VAT {expected_vat}/{vat} | "
            f"Pretax {expected_pretax}/{pretax} | "
            f"SubGrand {total}"
        )

        assert round(pretax, 2) == round(expected_pretax, 2)
        assert round(vat, 2) == round(expected_vat, 2)

        grand_total = self._parse_money(
            self.page.locator(".grand-total-data").inner_text()
        )

        print(f"GrandTotal | expected={total} actual={grand_total}")

        assert round(total, 2) == round(grand_total, 2), (
            f"Grand total mismatch {total} != {grand_total}"
        )

    def proceed_to_payment(
    self,
    promotions: list | None,
    privileges: dict | None = None,
    bill_discount: dict | None = None,
    ):
        self.promotion_button.click()

        modal = self.page.locator(".modal-body")
        expect(modal).to_be_visible()

        self.uncheck_all_promotions()

        if promotions:
            self.check_promotions_by_name(promotions)

        self.confirm_button.click()

        self.apply_privileges(privileges)

        self.apply_bill_discount(bill_discount)
        self.assert_cart_totals()
        self.assert_checkout_totals()

        self.payment_button.click()
        self.confirm_button.click()

        with self.page.context.expect_page(timeout=80000) as receipt_page_info:
            self.payout_confirm_button.click()

        receipt_page = receipt_page_info.value
        receipt_page.wait_for_load_state(timeout=80000)
        receipt_page.close()

    def create_order_items(
    self,
    customer_id: str,
    items: list,
    promotions=None,
    privileges=None,
    bill_discount=None,
    ):
        self.select_saleman()
        self.select_customer(customer_id)

        for item in items:
            product = item["product"]
            discount = item.get("discount")

            for r in item.get("rounds", []):
                times = r.get("times", 1)
                self.add_product(product, times=times)

            if discount:
                self.apply_discount(product, discount)

        self.proceed_to_payment(promotions, privileges, bill_discount)

    def open_receipt(self):
        self.receipt.click()
        expect(self.receipt_table_rows.first).to_be_visible(timeout=10000)

    def void_transaction(self, row_index: int, reason: str | None = None):
        row = self.receipt_table_rows.nth(row_index)

        action_cell = row.locator("td").first
        action_cell.click()

        expect(self.void_transaction_dropdown).to_be_visible(timeout=5000)
        self.void_transaction_dropdown.click()

        if reason:
            expect(self.void_textarea).to_be_visible(timeout=5000)
            self.void_textarea.fill(reason)

        self.confirm_button.click()

        expect(self.void_success_alert).to_be_visible(timeout=10000)
        self.void_close_button.click()

    def void_if_needed(self, void_cfg):
        if not isinstance(void_cfg, dict):
            return

        self.open_receipt()
        self.void_transaction(
            row_index=void_cfg.get("row", 0),
            reason=void_cfg.get("reason"),
        )
