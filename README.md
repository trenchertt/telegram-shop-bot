Telegram Shop Bot
This is a Telegram bot with an integrated Web App, designed as a simple online store. Users can interact with the bot via commands or use the Web App for a richer interface with Home, Categories, and Profile sections. The project includes a Python-based bot and backend, and a frontend Web App built with HTML/CSS/JavaScript.
Features

Bot Commands:
/start: Displays a welcome message and a button to open the Web App.
/balance: Shows the user's balance.
/categories: Lists available product categories.


Web App:
Home: Welcomes users and can display featured products.
Categories: Lists product categories (fetched from the backend).
Profile: Shows user information, including Telegram ID and balance.
UI: Includes a top bar with settings (left) and balance (right), and a bottom navigation menu.


Backend: Provides REST API endpoints for categories and user data.
Database: SQLite for storing users, categories, and products.

Project Structure

bot.py: Telegram bot implementation using aiogram, handles commands and launches the Web App.
app.py: Flask backend with API endpoints for the Web App.
index.html: Web App frontend with HTML/CSS/JavaScript, integrated with Telegram Web App API.
shop.db: SQLite database (created automatically on first run).
.gitignore: Ignores virtual environment, database, and Python cache files.

Prerequisites

Python 3.8+: For running the bot and backend.
Node.js (optional): For local testing of the Web App with http-server.
Git: For version control.
Telegram Bot Token: Provided by BotFather (included in bot.py).

Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/telegram-shop-bot.git
cd telegram-shop-bot


Set Up Python Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install aiogram flask


Run the Bot:
python bot.py


Open Telegram, find your bot, and test commands (/start, /balance, /categories).
Note: The Web App button requires a deployed URL (see Deployment).


Run the Backend:
python app.py


Access API at http://127.0.0.1:5000/api/categories to verify.


Test the Web App Locally (optional):

Install http-server:npm install -g http-server


Run:http-server


Open http://localhost:8080 in a browser to test the Web App UI.



Deployment

Web App (Frontend):

Deploy index.html to Vercel:
Sign up at vercel.com.
Connect your GitHub repository.
Vercel will provide a URL (e.g., https://telegram-shop-bot.vercel.app).
Update the web_app URL in bot.py (in the InlineKeyboardButton for /start).




Backend:

Deploy app.py to Render or Heroku:
On Render: Create a "Web Service," connect GitHub, set the start command to python app.py.
Get the backend URL (e.g., https://telegram-shop-backend.onrender.com).
Update index.html with this URL in the fetchCategories and fetchBalance functions.




Set Up Webhook (Optional):

For production, replace polling in bot.py with a webhook:curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-backend-url.com/webhook


Add webhook handling to app.py (see aiogram documentation for details).



Database

The bot creates a SQLite database (shop.db) on first run.
Tables: users (Telegram ID, balance), categories (ID, name), products (ID, name, price, category_id, image_url).
Initial data: One category ("Электроника") and one product ("Телефон").

Future Improvements

Add product cards with images and "Buy" buttons in the Web App.
Implement a shopping cart using Telegram.WebApp.MainButton.
Integrate Telegram Payments for real transactions.
Add more bot commands (e.g., /buy <id>).
Enhance security with Telegram initData validation.

Contributing
Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue to discuss.
License
MIT License. See LICENSE for details.
