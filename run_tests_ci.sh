#!/bin/bash
set -euo pipefail

echo "=== CI: Запуск тестов с Allure ==="

echo "[1/4] Очистка предыдущих результатов..."
rm -rf allure-results allure-report

echo "[2/4] Запуск тестов..."
pytest tests/ \
  --alluredir=allure-results \
  -v --tb=short \
  "$@"

echo "[3/4] Генерация HTML отчета..."
allure generate allure-results -o allure-report --clean

echo "[4/4] ✅ Готово!"

