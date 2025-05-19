const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

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
app.post('/book', (req, res) => {
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

app.listen(port, () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});
