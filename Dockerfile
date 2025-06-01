FROM node:22-slim

# Установка зависимостей для health-check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Создание безопасного пользователя
RUN groupadd -r nodeuser && useradd -r -g nodeuser nodeuser

# Установка переменной окружения для продакшена
ENV NODE_ENV=production

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci --omt=dev

# Копируем остальной код
COPY . .

# Создаем директорию для данных и устанавливаем права
RUN mkdir -p /app/data && chown -R nodeuser:nodeuser /app

# Переключаемся на безопасного пользователя
USER nodeuser

# Открываем порт
EXPOSE 3000

# Запускаем приложение
CMD ["node", "server.js"]
