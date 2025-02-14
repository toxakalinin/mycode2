import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from bot.otp_manager import OTPManager

# Настройки
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
otp_manager = OTPManager()
CONFIG_STORAGE = "config_storage"

# Главная страница (логин)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        telegram_id = session.get("telegram_id")
        otp = request.form.get("otp")
        if otp_manager.verify_otp(telegram_id, int(otp)):
            session["authenticated"] = True
            return redirect(url_for("files"))
        return "Неверный или истекший код", 403
    return render_template("login.html")

# Страница файлов
@app.route("/files")
def files():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    files = os.listdir(CONFIG_STORAGE)
    return render_template("files.html", files=files)

# Скачать файл
@app.route("/files/<filename>")
def download_file(filename):
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return send_from_directory(CONFIG_STORAGE, filename)

# Старт приложения
if __name__ == "__main__":
    app.run(debug=True)
