import json
import os
import time
from flask import Flask, render_template, request, redirect, url_for, session

# Настройка приложения
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Случайный секретный ключ для защиты сессий

CREDENTIALS_FILE = "credentials.json"  # Файл с учетными данными

# Функция загрузки учетных данных пользователей
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

# Главная страница
@app.route("/")
def home():
    return render_template("index.html")

# Страница входа
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        credentials = load_credentials()
        
        # Проверяем, есть ли такой пользователь и совпадает ли пароль
        for user_id, (stored_username, stored_password) in credentials.items():
            if username == stored_username and password == stored_password:
                session["user_id"] = user_id
                return redirect(url_for("success"))

        return redirect(url_for("failure"))  # Если вход неудачен

    return render_template("login.html")

# Страница успешного входа
@app.route("/success")
def success():
    if "user_id" not in session:
        return redirect(url_for("login"))  # Перенаправляем на вход, если нет сессии
    return render_template("success.html")

# Страница неудачного входа
@app.route("/failure")
def failure():
    time.sleep(2)  # Небольшая задержка для защиты от брутфорса
    return render_template("failure.html")

# Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
