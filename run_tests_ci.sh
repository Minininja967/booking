#!/bin/bash
set -euo pipefail

echo "=== CI: Запуск тестов ==="

# Ждем готовности приложения
echo "Проверка доступности приложения..."
timeout 60 bash -c 'until curl -f $BASE_URL/health 2>/dev/null; do echo "Waiting..."; sleep 2; done' || {
    echo "❌ Приложение недоступно"
    exit 1
}

echo "✅ Приложение готово, запускаем тесты..."

# Запуск тестов с Allure
pytest tests/ \
  --alluredir=/tests/allure-results \
  -v --tb=short \
  --maxfail=5 \
  "$@"

echo "✅ Тесты завершены"