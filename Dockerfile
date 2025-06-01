# Используем официальный образ Node.js
FROM node:22-slim

# Устанавливаем curl для health-check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN groupadd -r nodeuser && useradd -r -g nodeuser nodeuser

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем package.json и package-lock.json (если есть)
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci --only=production

# Копируем остальные файлы проекта
COPY . .

# Создаем директорию для базы данных и меняем владельца
RUN mkdir -p /app/data && chown -R nodeuser:nodeuser /app

# Переключаемся на пользователя nodeuser
USER nodeuser

# Открываем порт 3000
EXPOSE 3000

# Запускаем приложение
CMD ["node", "server.js"]