import sqlite3
from faker import Faker
import random

# Підключення до бази (створить файл, якщо його нема)
conn = sqlite3.connect("task_manager.db")
cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

# Заповнення таблиць
fake = Faker()

# Статуси (тільки 1 раз)
statuses = ['new', 'in progress', 'completed']
cursor.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", [(s,) for s in statuses])

# Користувачі
users = []
for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    users.append((fullname, email))
cursor.executemany("INSERT INTO users (fullname, email) VALUES (?, ?)", users)

# Отримуємо IDs для випадкових зв’язків
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

# Завдання
tasks = []
for _ in range(30):
    title = fake.sentence(nb_words=4)
    description = fake.text(max_nb_chars=100)
    status_id = random.choice(status_ids)
    user_id = random.choice(user_ids)
    tasks.append((title, description, status_id, user_id))

cursor.executemany("""
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (?, ?, ?, ?)
""", tasks)

# Збереження
conn.commit()
conn.close()

print("База створена та заповнена: task_manager.db")