from playwright.sync_api import Page, expect
from utils.config import Urls
import time
import os


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page

        self.first_name_input = page.locator("#firstName")
        self.last_name_input = page.locator("#lastName")
        self.dob_input = page.locator("#birthDate")

        self.phone_country_input = page.locator("input#phone[role='combobox'][type='search']")
        self.phone_number_input = page.locator("input#phone[placeholder='Your phone number']")
        self.gender_input = page.locator("input#gender[role='combobox'][type='search']")
        self.nationality_input = page.locator("input#nationality[role='combobox'][type='search']")
        self.email_input = page.locator("#email")

        self.marketing_checkbox = page.get_by_role("checkbox", name="I agree to receive marketing")
        self.consent = page.get_by_role("checkbox", name="I agree to the Terms and")

        self.submit_button = page.get_by_role("button", name="Submit arrow-right")

        self.alert_duplicate = page.get_by_text("Phone or Email duplicate , please input data again.OK")
        self.alert_ok = page.get_by_role("button", name="OK")
        self.alert_success = page.locator(".flex.flex-col.items-center")

        self._base_data = None
        self._result_file = os.path.abspath("created_users.txt")

    def _gen_seed(self) -> str:
        return f"{time.time_ns() % 100_000_000:08d}"

    def open_register(self):
        self.page.goto(Urls.REGISTER)
        expect(self.first_name_input).to_be_visible(timeout=10000)

    def agree_marketing(self):
        if not self.marketing_checkbox.is_checked():
            self.marketing_checkbox.check()

        if self.consent.count() > 0 and not self.consent.is_checked():
            self.consent.check()

    def _init_base_data(self, data: dict):
        if self._base_data is None:
            self._base_data = data.copy()

    def _generate_new_data(self, data: dict):
        seed = self._gen_seed()

        firstName = self._base_data.get("first_name") or "Auto-"
        eMail = self._base_data.get("email") or f"{firstName}"

        data["first_name"] = f"{firstName}{seed}"
        data["phone_number"] = seed
        data["email"] = f"{eMail}{seed}@gmail.com"
        
    def _fill_form(self, data: dict):
        self.first_name_input.fill(data["first_name"])
        self.phone_number_input.fill(data["phone_number"])
        self.email_input.fill(data["email"])

        if data.get("agree_marketing"):
            self.agree_marketing()

    def _save_success_member_id(self, member_id: str):
        with open(self._result_file, "a", encoding="utf-8") as f:
            f.write(member_id + "\n")

    def _clear_success_file(self):
        with open(self._result_file, "w", encoding="utf-8") as f:
            f.write("")

    def register(self, data: dict):
        working_data = data.copy()
        self._init_base_data(working_data)

        times = working_data.get("times", 1)

        self._clear_success_file()

        for _ in range(times):
            self.open_register()
            self.page.wait_for_load_state("domcontentloaded")

            expect(self.last_name_input).to_be_visible()
            self.last_name_input.fill(working_data["last_name"])

            expect(self.dob_input).to_be_visible()
            self.dob_input.fill(working_data["dob"])

            expect(self.phone_country_input).to_be_visible()
            self.phone_country_input.fill(working_data["phone_country"])
            self.phone_country_input.press("Enter")

            expect(self.gender_input).to_be_enabled()
            self.gender_input.click()
            expect(self.page.get_by_text(working_data["gender"], exact=True)).to_be_visible()
            self.page.get_by_text(working_data["gender"], exact=True).click()

            expect(self.nationality_input).to_be_visible()
            self.nationality_input.fill(working_data["nationality"])
            self.nationality_input.press("Enter")

            self._generate_new_data(working_data)
            self._fill_form(working_data)

            expect(self.submit_button).to_be_enabled()

            with self.page.expect_response(lambda r: r.status in (200, 201)) as resp:
                self.submit_button.click()

            response = resp.value.json()
            member_id = response["member_id"]

            try:
                expect(self.alert_success).to_be_visible(timeout=5000)
                self._save_success_member_id(member_id)
                continue
            except:
                pass

            try:
                expect(self.alert_duplicate).to_be_visible(timeout=3000)
                self.alert_ok.click()
                continue
            except:
                pass

            break
