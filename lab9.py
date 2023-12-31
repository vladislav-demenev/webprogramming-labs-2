# Импорт необходимых модулей Flask
from flask import Blueprint, render_template, request, abort, jsonify, url_for, redirect

# Создание Blueprint с именем 'lab9'
lab9 = Blueprint('lab9', __name__)

# Маршрут для главной страницы
@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')

# Пользовательский обработчик ошибки для 404 Not Found
@lab9.app_errorhandler(404)
def not_found(e):
    return 'Нет такой страницы, вернуться обратно ❄️❄️❄️ <a href="/menu">Меню</a> ❄️❄️❄️', 404

# Маршрут для страницы с ошибкой 500 Internal Server Error
@lab9.route('/lab9/500')
def main1():
    return render_template('lab9/500.html'), 500

# Маршрут для обработки формы открытки, поддерживающий методы GET и POST
@lab9.route('/lab9/greeting_card', methods=['GET', 'POST'])
def greeting_card():
    if request.method == 'POST':
        recipient_name = request.form.get('recipient_name')
        recipient_gender = request.form.get('recipient_gender')
        sender_name = request.form.get('sender_name')

        # Перенаправление на URL с параметрами
        return redirect(url_for('lab9.show_card', recipient_name=recipient_name,
                                recipient_gender=recipient_gender, sender_name=sender_name))

    # Отображение формы, если запрос сделан методом GET
    return render_template('lab9/greeting_card_form.html')

# Маршрут для отображения открытки на основе параметров в URL
@lab9.route('/lab9/show_card')
def show_card():
    # Получение параметров из URL
    recipient_name = request.args.get('recipient_name')
    recipient_gender = request.args.get('recipient_gender')
    sender_name = request.args.get('sender_name')

    # Создание текста для открытки
    card_text = f"С Новым Годом, {recipient_name}! Желаю быть счастлив{'ой' if recipient_gender == 'female' else 'ым'}! С наилучшими пожеланиями, {sender_name}!"

    # Отображение результирующего шаблона с текстом открытки
    return render_template('lab9/greeting_card_result.html', card_text=card_text)
