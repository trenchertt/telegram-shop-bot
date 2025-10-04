import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# Инициализация бота с токеном
bot = Bot(token="8498877795:AAGYiEaLmFHy15_mo6WYqZHaH3bC5VqmddY")
dp = Dispatcher()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        tg_id TEXT PRIMARY KEY,
        balance REAL DEFAULT 100.0
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        category_id INTEGER,
        image_url TEXT
    )""")
    # Тестовые данные
    c.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Электроника')")
    c.execute("INSERT OR IGNORE INTO products (id, name, price, category_id, image_url) VALUES (1, 'Телефон', 10000, 1, 'https://example.com/phone.jpg')")
    conn.commit()
    conn.close()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть магазин", web_app=types.WebAppInfo(url="https://your-web-app-url.com"))]
    ])
    await message.answer("Добро пожаловать в магазин! Нажми кнопку, чтобы открыть Web App, или используй команды: /balance, /categories.", reply_markup=kb)

# Команда /balance
@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE tg_id = ?", (str(message.from_user.id),))
    result = c.fetchone()
    if not result:
        c.execute("INSERT INTO users (tg_id, balance) VALUES (?, 100.0)", (str(message.from_user.id),))
        conn.commit()
        balance = 100.0
    else:
        balance = result[0]
    conn.close()
    await message.answer(f"Ваш баланс: {balance} руб.")

# Команда /categories
@dp.message(Command("categories"))
async def cmd_categories(message: types.Message):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT name FROM categories")
    categories = c.fetchall()
    conn.close()
    if categories:
        response = "Категории:\n" + "\n".join([cat[0] for cat in categories])
    else:
        response = "Категории пока пусты."
    await message.answer(response)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())