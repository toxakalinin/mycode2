from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object('config.ProductionConfig')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/webdownload')
def webdownload():
    return render_template('webdownload.html')

@app.route('/dashpanel')
def dashpanel():
    return render_template('dashpanel.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/social')
def social():
    return render_template('social.html')

@app.route('/loginadmin', methods=['POST'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    honeypot = request.form.get('honeypot')

    if honeypot:  # Если поле-ловушка заполнено — это бот
        logging.warning(f'Бот попытался войти с именем: {username}')
        return jsonify({"error": "Bot detected!"}), 403

    if username == 'admin' and password == 'securepassword':  # Заменить на хэшированный пароль
        return redirect(url_for('dashboard'))
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
