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

# Заданные данные
SITE_LINK = "https://vpnconfigurator.online"
INSTRUCTION_TEXT = "Это инструкция по использованию бота и сервиса.\n Суть проста - обеспечить вам доступ к ВПН, а также обновить файл конфига, если текущий вдруг перестал работать.\n Нажмите 'ПОЛУЧИТЬ ЛОГИН/ПАРОЛЬ' и 'ПОЛУЧИТЬ ССЫЛКУ' - я отправлю вам необходимые данные.\n Далее, зайдите на сайт по ссылке, введите данные, что я вам отправил. Лучше скопировать, чтобы не допустить ошибки. После чего вы получите доступ к нужным файлам и сможете их скачать.\n\n После скачивания - определите расположение загруженного файла, перейдите в приложение Wireguard (красное, с белым драконом), справа внизу нажмите +, затем 'Импорт из файла...'. В открывшемся меню выберите загруженный файл. После чего - переведите ползунок в положение 'ВКЛ' (вправо) и проверьте отправку и получение данных.\n\n Если на любом из этапов возникнут трудности - нажмите 'ПОЛУЧИТЬ ПОМОЩЬ', чтобы я отправил сообщение с проблемой прямиком админу.\n\n И не беспокойтесь о конфиденциальности, Алексей Викторович, я отвечаю только вам и администратору, а остальным отправляю сообщение 'ПОШЕЛ НАХ*Й', что бы оно не означало.\n\n Всегда к вашим услугам и надeюсь быть полезным.\n Хорошего дня!"

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [
        ["ПОЛУЧИТЬ ЛОГИН/ПАРОЛЬ", "СБРОСИТЬ ЛОГИН/ПАРОЛЬ"],
        ["ПОМОЩЬ", "ПОЛУЧИТЬ ССЫЛКУ НА САЙТ"],
        ["ИНСТРУКЦИЯ"]
    ],
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
        await update.message.reply_text("ПОШЕЛ НАХУЙ")
        return
    await update.message.reply_text("Привет! Чем могу помочь?", reply_markup=main_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("ПОШЕЛ НАХУЙ")
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
    
    elif text == "ПОЛУЧИТЬ ССЫЛКУ НА САЙТ":
        await update.message.reply_text(f"Вот ссылка на сайт: {SITE_LINK}")
    
    elif text == "ИНСТРУКЦИЯ":
        await update.message.reply_text(INSTRUCTION_TEXT)
    
    # Вежливые ответы
    elif text.lower() in ["привет", "здравствуй", "здравствуйте", "hi", "hello"]:
        await update.message.reply_text("Приветствую! Чем могу помочь?")
    elif text.lower() in ["спасибо", "благодарю"]:
        await update.message.reply_text("Рад помочь!")
    elif text.lower() in ["пока", "до свидания", "до встречи"]:
        await update.message.reply_text("До свидания! Буду рад помочь в любое время.")
    else:
        await update.message.reply_text("Извините, я не понял ваш запрос. Выберите действие из меню.")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
