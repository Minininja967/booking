# Используем официальный образ Node.js
FROM node:22-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем package.json и package-lock.json (если есть)
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install
RUN npm ci --only=production

# Копируем остальные файлы проекта
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Открываем порт 3000
EXPOSE 3000

RUN apk add --no-cache curl
# Запускаем приложение
CMD ["node", "server.js"]