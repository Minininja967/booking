import pytest
import allure
from pages.main_page import MainPage


@allure.feature("Main page")
class TestMainPage:
    """Main page tests"""

    @allure.story("Main page loading")
    @allure.title("Main page loading check")
    @allure.description(
        "The test checks that main page load correct with correct title and visible load button"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_page_loads_correctly_test(self, page, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step("Check the title"):
            main_page.check_title()

        with allure.step("Che the login button"):
            main_page.check_login_button_visible()

    @allure.story("Horses profile")
    @allure.title("Open horse profile by clicking on photo")
    @allure.description("The test checks that horse profile can be opened")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_horse_profile_opens_on_card_click(self, page, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step("Check that cards exist"):
            main_page.assert_cards_exist()

        with allure.step("Click on the card"):
            main_page.click_card_by_index(0)

        with allure.step("Verify that description is visible"):
            main_page.check_description_visible()

        with allure.step("Verify that booking book is visible"):
            main_page.check_booking_button_visible()

    @allure.story("Horses profile")
    @allure.title("Names check")
    @allure.description(
        "Verifying that names in the slider matches the name in the profile"
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_horse_names_match_profile_names(self, page, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step("Get all cards with horses"):
            cards = main_page.assert_cards_exist()
            cards_count = int(cards.count())
            allure.attach(
                str(cards_count), "Number of founded cards", allure.attachment_type.TEXT
            )

        with allure.step(f"Check matching names for {cards_count} cards"):
            for i in range(cards_count):
                expected_name = main_page.get_card_name_by_index(i)
                main_page.click_card_by_index(i)
                actual_name = main_page.get_opened_profile_name()
                assert (
                    actual_name == expected_name
                ), f"Name '{actual_name}' at the profile is not matches name on the card '{expected_name}'"

    @allure.story("Login popup")
    @allure.title("Login popup appearance by login botton click")
    @allure.description(
        "Verifying that login popup appears after clicking login button"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_popup_opening_by_clicking_login_button(self, page, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step("Click login button"):
            main_page.click_login_button()

        with allure.step("Verifying that pop is opened"):
            main_page.popup_is_opened()

    @allure.story("Login popup")
    @allure.title("Login popup appearance by booking botton click")
    @allure.description(
        "Verifying that login popup appears after clicking booking button"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_popup_openenig_by_clicking_booking_button(self, page, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step("Click horse card"):
            main_page.click_horse_card(0)

        with allure.step("Verifying that booking button is visible"):
            main_page.check_booking_button_visible()

        with allure.step("Click login button"):
            main_page.click_booking_button()

        with allure.step("Verifying that pop is opened"):
            main_page.popup_is_opened()

    @allure.story("Horses profile")
    @allure.title("Checking specific horse cards (parameterized test)")
    @allure.description(
        "The test checks that chosen horse profiles can be opened and descrition and booking button are visible"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("card_index", [0, 1, 2])
    def test_specific_horse_cards(self, page, card_index, base_url):
        main_page = MainPage(page, base_url)

        with allure.step("Open main page"):
            main_page.open()

        with allure.step(f"get all cards for checking index {card_index}"):
            cards = main_page.get_horse_cards()
            cards_count = int(cards.count())
            allure.attach(
                str(cards_count),
                "Общее количество карточек",
                allure.attachment_type.TEXT,
            )
            allure.attach(
                str(card_index),
                "Проверяемый индекс карточки",
                allure.attachment_type.TEXT,
            )

        if int(cards.count()) > card_index:
            with allure.step(f"Click card with index {card_index}"):
                main_page.click_horse_card(card_index)

            with allure.step("Check that description is visible"):
                main_page.check_description_visible()

            with allure.step("Check that booking buton is visible"):
                main_page.check_booking_button_visible()
        else:
            with allure.step(f"Pass test - not enough cards for index {card_index}"):
                allure.attach(
                    f"Need card with index {card_index}, but there are only {cards_count} cards",
                    "Reason why test is missed",
                    allure.attachment_type.TEXT,
                )
                pytest.skip(f"not enough cards for index {card_index}")
