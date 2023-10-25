
from flask import Blueprint, redirect, url_for, render_template, request
lab4 = Blueprint('lab4',__name__)


@lab4.route('/lab4/')
def lab ():
    return render_template('lab4.html')


@lab4.route('/lab4/login/', methods = ['GET', 'POST'])
def login ():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        error = 'Не введен логин'
        return render_template('login.html', error=error, username=username, password=password)

    if not password:
        error = 'Не введен пароль'
        return render_template('login.html', error=error, username=username, password=password)

    if username == 'alex' and password == '123':
        return render_template('logining.html', username=username)


    error = 'Неверные логин и/или пароль'
    return render_template('login.html', error=error, username=username, password=password)


@lab4.route('/lab4/fridge/', methods = ['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')
    message = ""

    if request.method == 'POST':
        if not temperature:
            message = "Ошибка: не задана температура"
        else:
            temperature = int(temperature)
            if temperature < -12:
                message = "Не удалось установить температуру — слишком низкое значение"
            elif temperature > -1:
                message = "Не удалось установить температуру — слишком высокое значение"
            elif -12 <= temperature <= -9:
                message = f"Установлена температура: {temperature}°С" + "❄️❄️❄️"
            elif -8 <= temperature <= -5:
                message = f"Установлена температура: {temperature}°С" + "❄️❄️"
            elif -4 <= temperature <= -1:
                message = f"Установлена температура: {temperature}°С" + "❄️"

    return render_template('fridge.html', message=message, temperature=temperature)