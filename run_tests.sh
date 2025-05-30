#!/bin/bash

# Скрипт для запуска тестов с генерацией Allure отчета

echo "=== Запуск тестов с Allure отчетностью ==="

# Установка необходимых пакетов (выполнить один раз)
echo "1. Установка зависимостей..."
if ! pip list | grep -q allure-pytest; then
  echo "→ Устанавливаю зависимости..."
  pip install allure-pytest pytest-playwright
else
  echo "→ Зависимости уже установлены."
fi

echo "2. Очистка предыдущих результатов..."
rm -rf allure-results
rm -rf allure-report

echo "3. Запуск тестов..."
# Основная команда для запуска тестов с Allure
pytest tests/ \
    --alluredir=allure-results \
    -v \
    --tb=short \
    "$@"

echo "4. Генерация HTML отчета..."
# Генерация HTML отчета
allure generate allure-results -o allure-report --clean

echo "5. Открытие отчета в браузере..."
# Открытие отчета в браузере
allure open allure-report

echo "=== Готово! ==="

# Альтернативные команды для различных сценариев:

# Запуск только smoke тестов:
# pytest tests/ -m smoke --alluredir=allure-results

# Запуск с параллельным выполнением:
# pytest tests/ -n auto --alluredir=allure-results

# Запуск конкретного теста:
# pytest tests/test_main_page.py::TestMainPage::test_main_page_loads_correctly_test --alluredir=allure-results

# Запуск с дополнительной информацией:
# pytest tests/ --alluredir=allure-results -v -s --tb=long