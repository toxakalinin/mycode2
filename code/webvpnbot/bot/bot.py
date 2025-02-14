from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv
from sqlalchemy.future import select
import sys
import os

sys.path.append("/home/toxakalinin/code/webvpnbot/")

from bot.database import AsyncSessionLocal, AuthorizedUser, OTPSession

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send /login to generate temporary credentials"
    )

async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with AsyncSessionLocal() as db:
            query = select(AuthorizedUser).where(AuthorizedUser.telegram_id == update.effective_user.id)
            result = await db.execute(query)
            user = result.scalars().first()

            if user:
                otp = secrets.token_urlsafe(6)[:8].upper()
                expires_at = datetime.now() + timedelta(minutes=10)

                otp_session = OTPSession(
                    username=user.username,
                    otp=otp,
                    expires_at=expires_at
                )
                db.add(otp_session)
                await db.commit()

                await update.message.reply_text(
                    f"🔑 Temporary credentials:\n"
                    f"👤 Username: {user.username}\n"
                    f"🔢 OTP: {otp}\n"
                    f"⏳ Valid for 10 minutes"
                )
            else:
                await update.message.reply_text("❌ Authorization denied")

    except Exception as e:
        print(f"Error in handle_login: {e}")
        await update.message.reply_text("⚠️ Service temporarily unavailable")


async def cleanup_otp(context: ContextTypes.DEFAULT_TYPE):
    async with AsyncSessionLocal() as db:
        expired = db.query(OTPSession).filter(OTPSession.expires_at < datetime.now())
        await expired.delete()
        await db.commit()

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and len(context.args) == 2:
        try:
            async with AsyncSessionLocal() as db:
                user = AuthorizedUser(
                    telegram_id=int(context.args[0]),
                    username=context.args[1]
                )
                db.add(user)
                await db.commit()
                await update.message.reply_text("✅ User added successfully")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("Usage: /adduser <telegram_id> <username>")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(AuthorizedUser))
            users = result.scalars().all()

            if users:
                users_list = "\n".join([f"👤 {u.username} (ID: {u.telegram_id})" for u in users])
                await update.message.reply_text(f"📜 Authorized users:\n{users_list}")
            else:
                await update.message.reply_text("📭 No authorized users found.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and len(context.args) == 2:
        try:
            async with AsyncSessionLocal() as db:
                query = select(AuthorizedUser).where(AuthorizedUser.telegram_id == int(context.args[0]))
                result = await db.execute(query)
                existing_user = result.scalars().first()

                if existing_user:
                    await update.message.reply_text("⚠️ User already exists!")
                    return

                user = AuthorizedUser(
                    telegram_id=int(context.args[0]),
                    username=context.args[1]
                )
                db.add(user)
                await db.commit()
                await update.message.reply_text("✅ User added successfully")

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("Usage: /adduser <telegram_id> <username>")

def main():
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Добавляем JobQueue вручную
    job_queue = application.job_queue
    job_queue.run_repeating(cleanup_otp, interval=3600)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("login", handle_login))
    application.add_handler(CommandHandler("adduser", add_user))
    application.add_handler(CommandHandler("listusers", list_users))


    application.run_polling()

if __name__ == '__main__':
    main()
