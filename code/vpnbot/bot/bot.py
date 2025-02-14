import os
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from otp_manager import OTPManager

# Настройки
BOT_TOKEN = os.getenv("TOKEN")
OTP_EXPIRATION = 300  # Время жизни кода (в секундах)
WEBSITE_URL = os.getenv("WEBSITE_URL")  # Ссылка на сайт

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Менеджер одноразовых паролей
otp_manager = OTPManager()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /get_code, чтобы получить доступ к конфигурациям.")

# Команда /get_code
async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    otp = otp_manager.generate_otp(telegram_id, OTP_EXPIRATION)
    await update.message.reply_text(
        f"Ваш код: {otp}\nСсылка на сайт: {WEBSITE_URL}\nКод действителен {OTP_EXPIRATION // 60} минут."
    )
    logger.info(f"Код {otp} выдан для пользователя {telegram_id}")

# Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_code", get_code))
    application.run_polling()

if __name__ == "__main__":
    main()
