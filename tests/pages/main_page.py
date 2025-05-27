# tests/pages/main_page.py
from playwright.sync_api import Page, expect

class MainPage: 
    def __init__(self, page: Page):
        self.page = page
        self.url = "http://localhost:3000"

    def open(self):
        """Переход на главную страницу"""
        self.page.goto(self.url)

    def check_title(self):
        """Проверяем заголовок страницы"""
        expect(self.page).to_have_title("Бронирование лошадей")

    def get_horse_card(self):
        """Возвращаем все карточки лошадей"""
        return self.page.locator(".slide")

    def click_card_by_index(self, index: int):
        """Кликаем по карточке с индексом"""
        self.get_horse_card().nth(index).click()

    def get_card_name_by_index(self, index: int) -> str:
        """Получаем текст из карточки"""
        return self.get_horse_card().nth(index).inner_text()
    
    def get_opened_block_name(self) -> str:
        """Получаем имя лошади из блока описания"""
        return self.page.locator(".profile-info [id='horse-name']").inner_text()