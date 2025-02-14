import os
from dotenv import load_dotenv
from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY', '/config_files')

# Клавиатуры
main_keyboard = ReplyKeyboardMarkup(
    [["НАЧАТЬ", "ПОЛУЧИТЬ КОНФИГ"], ["ПОКА"]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для работы с конфигурационными файлами.",
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "НАЧАТЬ":
        await update.message.reply_text("Давайте начнём! Используйте кнопки для управления.")
    elif text == "ПОЛУЧИТЬ КОНФИГ":
        await show_file_selection(update, context)
    elif text == "ПОКА":
        await update.message.reply_text(
            "До свидания! Для возобновления работы напишите /start",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text("Извините, я не понимаю эту команду.")

async def show_file_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        files = os.listdir(FILES_DIRECTORY)
        if not files:
            await update.message.reply_text("Файлы не найдены!")
            return
        
        # Создаем инлайн-кнопки для каждого файла
        keyboard = []
        for file in files:
            keyboard.append([InlineKeyboardButton(file, callback_data=file)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Выберите файл:",
            reply_markup=reply_markup
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

async def handle_file_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    selected_file = query.data
    file_path = os.path.join(FILES_DIRECTORY, selected_file)
    
    try:
        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=open(file_path, 'rb'),
            filename=selected_file
        )
    except Exception as e:
        await query.message.reply_text(f"Ошибка при отправке файла: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_file_selection))

    application.run_polling()

if __name__ == "__main__":
    main()
