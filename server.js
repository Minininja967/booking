const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const app = express();
const port = 3000;
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const JWT_SECRET = 'your_super_secret_key'; // в .env в проде
const SALT_ROUNDS = 10;

app.use(cors());
app.use(express.json());
app.use(express.static('public')); // Добавлено для статических файлов

const db = new sqlite3.Database('./bookings.db');

// Создание таблицы
db.run(`
  CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    horse_id TEXT,
    horse_name TEXT,
    date TEXT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT
  )
`);

// Таблица пользователей
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
  )
`);

// Получение занятых дат по лошади
app.get('/booked-dates/:horseId', (req, res) => {
  const horseId = req.params.horseId;
  db.all('SELECT date FROM bookings WHERE horse_id = ?', [horseId], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    const dates = rows.map(row => row.date);
    res.json({ bookedDates: dates });
  });
});

// Бронирование
app.post('/book', authenticateToken, (req, res) => {
  const { horse_id, horse_name, date, first_name, last_name, phone, email } = req.body;

  // Проверка занятости
  db.get('SELECT * FROM bookings WHERE horse_id = ? AND date = ?', [horse_id, date], (err, row) => {
    if (row) {
      return res.status(400).json({ error: 'Лошадь уже забронирована на эту дату' });
    }

    // Запись брони
    db.run(
      'INSERT INTO bookings (horse_id, horse_name, date, first_name, last_name, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)',
      [horse_id, horse_name, date, first_name, last_name, phone, email],
      function (err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ success: true });
      }
    );
  });
});

// Авторизация/регистрация
app.post('/auth', (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) return res.status(400).json({ error: 'Email и пароль обязательны' });

  db.get('SELECT * FROM users WHERE email = ?', [email], async (err, user) => {
    if (err) return res.status(500).json({ error: err.message });

    if (!user) {
      // Регистрация нового пользователя
      try {
        const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);
        db.run('INSERT INTO users (email, password) VALUES (?, ?)', [email, hashedPassword], function (err) {
          if (err) return res.status(500).json({ error: err.message });

          const token = jwt.sign({ id: this.lastID, email }, JWT_SECRET);
          res.json({ success: true, action: 'registered', token });
        });
      } catch (hashErr) {
        res.status(500).json({ error: hashErr.message });
      }
    } else {
      // Вход существующего пользователя
      try {
        const match = await bcrypt.compare(password, user.password);
        if (!match) return res.status(401).json({ error: 'Неверный пароль' });

        const token = jwt.sign({ id: user.id, email }, JWT_SECRET);
        res.json({ success: true, action: 'login', token });
      } catch (compareErr) {
        res.status(500).json({ error: compareErr.message });
      }
    }
  });
});

// Проверка авторизации с JWT
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // "Bearer TOKEN"

  if (!token) return res.status(401).json({ error: 'Нет токена авторизации' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Недействительный токен' });
    req.user = user;
    next();
  });
}

// Защищенный маршрут для получения данных текущего пользователя
app.get('/me', authenticateToken, (req, res) => {
  db.get('SELECT id, email FROM users WHERE id = ?', [req.user.id], (err, user) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!user) return res.status(404).json({ error: 'Пользователь не найден' });
    
    res.json({ 
      id: user.id,
      email: user.email
    });
  });
});

// Получение бронирований пользователя
app.get('/my-bookings', authenticateToken, (req, res) => {
  db.all('SELECT * FROM bookings WHERE email = ?', [req.user.email], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ bookings: rows });
  });
});

app.listen(port, () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});

// Отмена бронирования
app.delete('/cancel-booking/:id', authenticateToken, (req, res) => {
  const bookingId = req.params.id;

  // Удаляем только бронирование текущего пользователя
  db.run('DELETE FROM bookings WHERE id = ? AND email = ?', [bookingId, req.user.email], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    if (this.changes === 0) {
      return res.status(404).json({ error: 'Бронирование не найдено или нет доступа' });
    }
    res.json({ success: true });
  });
});
