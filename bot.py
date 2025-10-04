import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# Initialize bot with token
bot = Bot(token="8498877795:AAGYiEaLmFHy15_mo6WYqZHaH3bC5VqmddY")
dp = Dispatcher()

# Initialize database
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
    # Test data
    c.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Electronics')")
    c.execute("INSERT OR IGNORE INTO products (id, name, price, category_id, image_url) VALUES (1, 'Phone', 10000, 1, 'https://example.com/phone.jpg')")
    conn.commit()
    conn.close()

# Command /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Open Shop", web_app=types.WebAppInfo(url="https://telegram-shop-bot-teal.vercel.app"))]
    ])
    await message.answer("Welcome to the shop! Click the button to open the Web App or use commands: /wallet, /ref.", reply_markup=kb)

# Command /wallet
@dp.message(Command("wallet"))
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
    await message.answer(f"Your balance: {balance} USD")

# Command /ref
@dp.message(Command("ref"))
async def cmd_categories(message: types.Message):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT name FROM categories")
    categories = c.fetchall()
    conn.close()
    if categories:
        response = "Categories:\n" + "\n".join([cat[0] for cat in categories])
    else:
        response = "Categories are empty."
    await message.answer(response)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())