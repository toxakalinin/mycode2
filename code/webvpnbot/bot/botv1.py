import logging
import os
import secrets
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.future import select
from sqlalchemy import delete
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Подключение к базе данных
from database import AsyncSessionLocal, AuthorizedUser, OTPSession
#import bot.init_db_async

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение"""
    await update.message.reply_text("Отправьте /login, чтобы сгенерировать временные учетные данные.")

async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация OTP-кода для авторизованных пользователей"""
    try:
        async with AsyncSessionLocal() as db:
            query = select(AuthorizedUser).where(AuthorizedUser.telegram_id == update.effective_user.id)
            result = await db.execute(query)
            user = result.scalars().first()

            if user:
                otp = secrets.token_urlsafe(6)[:8].upper()
                expires_at = datetime.utcnow() + timedelta(minutes=10)

                otp_session = OTPSession(telegram_id=user.telegram_id, otp=otp, expires_at=expires_at)
                db.add(otp_session)
                await db.commit()

                await update.message.reply_text(
                    f"🔑 Временные учетные данные:\n"
                    f"🆔 Telegram ID: {user.telegram_id}\n"
                    f"🔢 OTP: {otp}\n"
                    f"⏳ Действителен 10 минут"
                )
            else:
                await update.message.reply_text("❌ Авторизация отклонена")

    except Exception as e:
        logger.error(f"Ошибка в handle_login: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Временная ошибка сервиса")

async def cleanup_otp(context: ContextTypes.DEFAULT_TYPE):
    """Удаление устаревших OTP-кодов"""
    async with AsyncSessionLocal() as db:
        await db.execute(delete(OTPSession).where(OTPSession.expires_at < datetime.utcnow()))
        await db.commit()

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление пользователя в БД"""
    if context.args and len(context.args) == 1:
        try:
            telegram_id = int(context.args[0])
            async with AsyncSessionLocal() as db:
                query = select(AuthorizedUser).where(AuthorizedUser.telegram_id == telegram_id)
                result = await db.execute(query)
                existing_user = result.scalars().first()

                if existing_user:
                    await update.message.reply_text("⚠️ Пользователь уже существует!")
                    return

                user = AuthorizedUser(telegram_id=telegram_id)
                db.add(user)
                await db.commit()
                await update.message.reply_text("✅ Пользователь успешно добавлен")

        except ValueError:
            await update.message.reply_text("❌ Ошибка: Telegram ID должен быть числом")
        except Exception as e:
            logger.error(f"Ошибка в add_user: {e}", exc_info=True)
            await update.message.reply_text("❌ Ошибка при добавлении пользователя")
    else:
        await update.message.reply_text("Использование: /adduser <telegram_id>")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод списка всех пользователей"""
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(AuthorizedUser))
            users = result.scalars().all()

            if users:
                users_list = "\n".join([f"👤 ID: {u.telegram_id}" for u in users])
                await update.message.reply_text(f"📜 Список пользователей:\n{users_list}")
            else:
                await update.message.reply_text("📭 Нет зарегистрированных пользователей.")

    except Exception as e:
        logger.error(f"Ошибка в list_users: {e}", exc_info=True)
        await update.message.reply_text("❌ Ошибка при получении списка пользователей")

async def verify_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение OTP-кода"""
    if not context.args:
        await update.message.reply_text("Использование: /verify <otp>")
        return

    otp_input = context.args[0]

    try:
        async with AsyncSessionLocal() as db:
            query = select(OTPSession).where(OTPSession.otp == otp_input, OTPSession.expires_at > datetime.utcnow())
            result = await db.execute(query)
            session = result.scalars().first()

            if session:
                await db.execute(delete(OTPSession).where(OTPSession.otp == otp_input))
                await db.commit()
                await update.message.reply_text("✅ OTP-код подтвержден! Доступ разрешен.")
            else:
                await update.message.reply_text("❌ Неверный или истекший OTP-код.")

    except Exception as e:
        logger.error(f"Ошибка в verify_otp: {e}", exc_info=True)
        await update.message.reply_text("❌ Ошибка при проверке OTP-кода")

async def main():
    """Основная функция запуска бота"""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("❌ Ошибка: BOT_TOKEN не задан в переменных окружения!")
        return

    # Запускаем приложение
    application = ApplicationBuilder().token(bot_token).build()

    # Планировщик задач для очистки OTP-кодов
    job_queue = application.job_queue
    job_queue.run_repeating(cleanup_otp, interval=3600)

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", handle_login))
    application.add_handler(CommandHandler("adduser", add_user))
    application.add_handler(CommandHandler("listusers", list_users))
    application.add_handler(CommandHandler("verify", verify_otp))

    logger.info("✅ Бот запущен")
    await init_db_async()
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
