# tests/pages/main_page.py
from playwright.sync_api import Page, expect
import allure
import time


class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "http://localhost:3000"

        # Локаторы выносим в константы
        self.HORSE_CARDS = ".slide"
        self.PROFILE_IMAGE = ".profile-image"
        self.HORSE_NAME_IN_PROFILE = ".profile-info [id='horse-name']"
        self.BOOKING_BUTTON = ".profile-info [id='book-from-profile']"
        self.LOGIN_BUTTON = "button:has-text('Личный кабинет')"
        self.HORSE_PROFILE = "[id='horse-profile']"
        self.POPUP = "[id='pop-up']"

    @allure.step("Open main page")
    def open(self):
        """Main page opening"""
        with allure.step(f"Go to URL: {self.url}"):
            self.page.goto(self.url)

        with allure.step("Wait for page loading"):
            self.page.wait_for_load_state("networkidle")

        allure.attach(
            self.page.screenshot(), "Main page screenshot", allure.attachment_type.PNG
        )

    @allure.step("Check title")
    def check_title(self):
        """Checking name of the page"""
        excepted_title = "Бронирование лошадей"
        with allure.step(f"Check that title matches {excepted_title}"):
            expect(self.page).to_have_title(excepted_title)

        actual_title = self.page.title()
        allure.attach(
            actual_title, "Актуальный заголовок страницы", allure.attachment_type.TEXT
        )

    @allure.step("Click on the card with index {index}")
    def click_horse_card(self, index: int = 0):
        """Finding horses foto by index and clicking it"""
        with allure.step(f"Get all cards"):
            cards = self.get_horse_cards()

        with allure.step("Click on the card"):
            cards.nth(index).click()

        with allure.step("Check that profile image is visible"):
            expect(self.page.locator(self.PROFILE_IMAGE)).to_be_visible()

            allure.attach(
                self.page.screenshot(),
                f"Opened profile (profile with index: {index})",
                allure.attachment_type.PNG,
            )

    @allure.step("Check visibility of the horse profile")
    def check_description_visible(self):
        """Verifying that horses profile is opened and visible"""
        with allure.step("Check that horse profile is visible"):
            expect(self.page.locator(self.HORSE_PROFILE)).to_be_visible()

        allure.attach(
            self.page.screenshot(), "Видимый профиль лошади", allure.attachment_type.PNG
        )

    @allure.step("Receiving all cards")
    def get_horse_cards(self):
        """Receiving all cards of the horses"""
        return self.page.locator(self.HORSE_CARDS)

    @allure.step("Click on the card with index {index}")
    def click_card_by_index(self, index: int):
        """Clicking on the card with index"""
        with allure.step("Click on the card with index {index}"):
            self.get_horse_cards().nth(index).click()

    @allure.step("Receiving name of the horse with index {index}")
    def get_card_name_by_index(self, index: int) -> str:
        """Getting name of the horse on the photo"""
        with allure.step(f"Retrieve name from the card #{index + 1}"):
            cards = self.get_horse_cards()
            if index >= cards.count():
                raise IndexError(f"Card with index {index} not found")

            card_text = cards.nth(index).inner_text().strip()
            allure.attach(
                card_text, f"Text of the card #{index + 1}", allure.attachment_type.TEXT
            )
            return card_text

    @allure.step("Receiving name of the horse in the gorse profile")
    def get_opened_profile_name(self) -> str:
        """Getting name of the horse in the horse profile"""
        with allure.step("Find element with name of the horse in the profile"):
            profile_name = self.page.locator(self.HORSE_NAME_IN_PROFILE)
            expect(profile_name).to_be_visible()

        with allure.step("Retrieve name of the horse"):
            name_text = profile_name.inner_text().strip()
            allure.attach(
                name_text, "Name of the horse from profile", allure.attachment_type.TEXT
            )
            return name_text

    @allure.step("Verifying that booking button is visible")
    def check_booking_button_visible(self):
        """Verifying that booking button is visible"""
        with allure.step("Check that button is visible"):
            expect(self.page.locator(self.BOOKING_BUTTON)).to_be_visible()

    @allure.step("Verifying that login button is visible")
    def check_login_button_visible(self):
        """Verifying that login button is visible"""
        with allure.step("Check that button is visible"):
            expect(self.page.locator(self.LOGIN_BUTTON)).to_be_visible()

    @allure.step("Check the availability of horse cards")
    def assert_cards_exist(self):
        """Verifying cards appearence"""
        cards = self.get_horse_cards()
        cards_count = int(cards.count())
        with allure.step(f"Check that cards were found {cards_count} > 0"):
            assert int(cards.count()) > 0, "There are no horses cards"
        return cards

    @allure.step("Clicking the login botton")
    def click_login_button(self):
        """Clicking the login botton"""
        with allure.step("Clicking the login botton"):
            self.page.locator(self.LOGIN_BUTTON).click()

    @allure.step("Clicking the booking botton")
    def click_booking_button(self):
        """Clicking the booking button"""
        with allure.step("Clicking the booking botton"):
            self.page.locator(self.BOOKING_BUTTON).click()

    @allure.step("Veryfying that popup is opened and visible")
    def popup_is_opened(self):
        """Veryfying that popup is opened and visible"""
        with allure.step("Veryfying that popup is opened and visible"):
            expect(self.page.locator(self.POPUP)).to_be_visible()
