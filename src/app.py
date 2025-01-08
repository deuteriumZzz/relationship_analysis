from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from model import RelationshipModel
import pandas as pd
from flask_dance.contrib.telegram import make_telegram_blueprint, telegram
from flask_dance.contrib.vk import make_vk_blueprint, vk

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Инициализация модели
model = RelationshipModel()

# Настройка Telegram
telegram_bp = make_telegram_blueprint(token='YOUR_TELEGRAM_BOT_TOKEN')
app.register_blueprint(telegram_bp, url_prefix='/telegram')

# Настройка ВКонтакте
vk_bp = make_vk_blueprint(app_id='YOUR_VK_APP_ID', client_secret='YOUR_VK_CLIENT_SECRET')
app.register_blueprint(vk_bp, url_prefix='/vk')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<platform>')
def login(platform):
    if platform == 'telegram':
        return redirect(url_for('telegram.login'))
    elif platform == 'vk':
        return redirect(url_for('vk.login'))
    else:
        return "Unsupported platform", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/analysis/<platform>', methods=['GET', 'POST'])
def analysis(platform):
    if platform == 'telegram' and telegram.authorized:
        user_id = telegram.get("me")['id']
        # Здесь вы можете получить сообщения и передать их в модель
        if request.method == 'POST':
            texts = request.form.getlist('texts')  # Получение текстов из формы
            predictions = model.predict(texts)
            return render_template('analysis.html', platform='Telegram', user_id=user_id, predictions=predictions.tolist())
        return render_template('analysis.html', platform='Telegram', user_id=user_id)

    elif platform == 'vk' and vk.authorized:
        vk_session = vk.get_session()
        vk_api_instance = vk_session.get_api()
        user_info = vk_api_instance.users.get()[0]
        # Аналогично, получение сообщений для анализа
        if request.method == 'POST':
            texts = request.form.getlist('texts')  # Получение текстов из формы
            predictions = model.predict(texts)
            return render_template('analysis.html', platform='VK', user_info=user_info, predictions=predictions.tolist())
        return render_template('analysis.html', platform='VK', user_info=user_info)

    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    texts = data['texts']
    predictions = model.predict(texts)
    return jsonify(predictions.tolist())

if __name__ == '__main__':
    app.run(debug=True)
