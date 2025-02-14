from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash, abort
import os
import sys
from datetime import datetime
from werkzeug.utils import safe_join
from dotenv import load_dotenv

# Подключаем переменные окружения
load_dotenv()

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SessionLocal, OTPSession  # Исправлено с Session на SessionLocal

app = Flask(__name__)
app.secret_key = os.getenv("WEB_SECRET_KEY") or 'your_secret_key_here'

# Директория для загрузки файлов
FILES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'user_files')
os.makedirs(FILES_DIR, exist_ok=True)  # Создаём папку, если её нет

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            with SessionLocal() as db:
                otp_session = db.query(OTPSession).filter(
                    OTPSession.username == request.form['username'],
                    OTPSession.otp == request.form['password'],
                    OTPSession.expires_at > datetime.now()
                ).first()

                if otp_session:
                    session['authenticated'] = True
                    session.permanent = True
                    db.delete(otp_session)
                    db.commit()
                    return redirect(url_for('configs'))

                flash('Invalid credentials or expired OTP', 'danger')
                return redirect(url_for('login'))

        except Exception as e:
            print(f"Login error: {e}")
            flash('Authentication service unavailable', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/configs')
def configs():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    # Проверка наличия каталога перед загрузкой файлов
    if not os.path.exists(FILES_DIR):
        files = []
    else:
        files = os.listdir(FILES_DIR)

    return render_template('configs.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    # Предотвращаем атаки через Path Traversal
    safe_path = safe_join(FILES_DIR, filename)

    if not os.path.exists(safe_path):
        abort(404, "File not found")

    try:
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    except Exception as e:
        print(f"File download error: {e}")
        abort(500, "Internal server error")

if __name__ == '__main__':
    app.run(debug=True)
