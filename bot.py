import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot with token
bot = Bot(token="8498877795:AAGYiEaLmFHy15_mo6WYqZHaH3bC5VqmddY")
dp = Dispatcher()

# Initialize database
def init_db():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        tg_id TEXT PRIMARY KEY,
        balance REAL DEFAULT 100.0,
        referrals INTEGER DEFAULT 0
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
    referral_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    if referral_id and referral_id.startswith("REF_"):
        referrer_id = referral_id.replace("REF_", "")
        conn = sqlite3.connect("shop.db")
        c = conn.cursor()
        referrer = c.execute("SELECT tg_id, referrals FROM users WHERE tg_id = ?", (referrer_id,)).fetchone()
        if referrer:
            c.execute("UPDATE users SET referrals = referrals + 1 WHERE tg_id = ?", (referrer_id,))
            conn.commit()
            logger.info(f"Referred user {message.from_user.id} by referrer {referrer_id}")
        conn.close()
    await message.answer("Welcome to the shop! Click the button to open the Web App or use commands: /wallet, /ref.", reply_markup=kb)
    # Ensure user is in database
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (tg_id, balance, referrals) VALUES (?, 100.0, 0)", (str(message.from_user.id),))
    conn.commit()
    conn.close()

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
async def cmd_referral(message: types.Message):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (tg_id, balance, referrals) VALUES (?, 100.0, 0)", (str(message.from_user.id),))
    c.execute("SELECT referrals FROM users WHERE tg_id = ?", (str(message.from_user.id),))
    result = c.fetchone()
    if result:
        referrals = result[0]
    else:
        referrals = 0
    referral_link = f"https://t.me/testrfrn_bot?start=REF_{message.from_user.id}"
    conn.commit()
    conn.close()
    await message.answer(f"Your referral link: {referral_link}\nInvited friends: {referrals}")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())