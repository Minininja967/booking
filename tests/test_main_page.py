import pytest
from pages.main_page import MainPage

def test_main_page_title(page):
   """
   Проверка: при открытии главной страницы заголовк правильный
   """
   main = MainPage(page)
   main.open()
   main.check_title
#    main.click_horse_card
#    main.check_description_visible

def test_horse_cards_matches_description(page):
  main = MainPage(page)
  main.open()

  cards = main.get_horse_card()
  count = cards.count()

  for i in range(count):
     expected_name = main.get_card_name_by_index(i)

     main.click_card_by_index(i)

     actual_name = main.get_opened_block_name()

     assert actual_name == expected_name, f"Имя в блоке: {actual_name}, ожидали: {expected_name}"
