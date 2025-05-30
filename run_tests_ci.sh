#!/bin/bash

echo "=== CI: Запуск тестов с Allure ==="

echo "1. Установка зависимостей..."
pip install allure-pytest pytest-playwright

echo "2. Очистка предыдущих результатов..."
rm -rf allure-results
rm -rf allure-report

echo "3. Запуск тестов..."
pytest tests/ \
    --alluredir=allure-results \
    -v \
    --tb=short \
    "$@"

echo "4. Генерация HTML отчета..."
allure generate allure-results -o allure-report --clean

echo "=== Готово! ==="
