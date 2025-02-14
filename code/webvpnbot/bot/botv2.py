import os
import json
import random
import string
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
AUTHORIZED_USERS = json.loads(os.getenv('AUTHORIZED_USERS', '[]'))  # Список разрешенных Telegram ID
CREDENTIALS_FILE = "credentials.json"

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [["ПОЛУЧИТЬ ЛОГИН/ПАРОЛЬ", "СБРОСИТЬ ЛОГИН/ПАРОЛЬ"], ["ПОМОЩЬ"]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def generate_credentials():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return username, password

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("Доступ запрещен.")
        return
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=main_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("Доступ запрещен.")
        return
    
    text = update.message.text
    credentials = load_credentials()
    
    if text == "ПОЛУЧИТЬ ЛОГИН/ПАРОЛЬ":
        if str(user_id) in credentials:
            username, password = credentials[str(user_id)]
        else:
            username, password = generate_credentials()
            credentials[str(user_id)] = (username, password)
            save_credentials(credentials)
        await update.message.reply_text(f"Ваши данные:\nЛогин: {username}\nПароль: {password}")
    
    elif text == "СБРОСИТЬ ЛОГИН/ПАРОЛЬ":
        username, password = generate_credentials()
        credentials[str(user_id)] = (username, password)
        save_credentials(credentials)
        await update.message.reply_text(f"Ваш новый логин и пароль:\nЛогин: {username}\nПароль: {password}")
    
    elif text == "ПОМОЩЬ":
        admin_id = os.getenv("ADMIN_TELEGRAM_ID")
        if admin_id:
            await context.bot.send_message(chat_id=admin_id, text=f"Запрос помощи от {user_id}")
        await update.message.reply_text("Ваш запрос отправлен администратору.")


def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
