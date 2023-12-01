# Импорт необходимых модулей и функций из Flask
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
# Импорт объекта базы данных из модуля или пакета с именем 'Db'
from Db import db
# Импорт моделей 'users' и 'articles' из модуля/пакета 'models' внутри 'Db'
from Db.models import users, articles
# Импорт функций для хэширования и проверки паролей с использованием Werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
# Импорт функций и объектов, связанных с аутентификацией пользователя с использованием Flask-Login
from flask_login import login_user, login_required, current_user, logout_user

# Создание Blueprint Flask с именем 'lab6'
lab6 = Blueprint("lab6", __name__)

# Определение маршрута '/lab6' и функции, которая будет выполняться при обращении к нему
@lab6.route("/lab6")
def main():
    # Проверка, аутентифицирован ли текущий пользователь
    user_is_authenticated = current_user.is_authenticated
    # Если пользователь аутентифицирован, установить его имя пользователя
    current_username = current_user.username if user_is_authenticated else "Аноним"
    # Отображение шаблона 'lab6.html' с передачей переменных в шаблон
    return render_template("lab6.html", user_is_authenticated=user_is_authenticated, current_user={"username": current_username})


# Маршрут для проверки и вывода всех пользователей из таблицы 'users' в базе данных
@lab6.route("/lab6/check")
def main1():
    # Получаем всех пользователей из таблицы 'users'
    my_users = users.query.all()
    
    # Выводим список пользователей в консоль
    print(my_users)
    
    # Возвращаем простую строку в качестве ответа клиенту
    return "результат в консоли!"

# Маршрут для проверки и вывода всех статей из таблицы 'articles' в базе данных
@lab6.route("/lab6/checkarticles")
def mainart():
    # Получаем все статьи из таблицы 'articles'
    my_articles = articles.query.all()
    
    # Итерируемся по каждой статье и выводим её заголовок и текст в консоль
    for article_item in my_articles:
        print(f"{article_item.title}-{article_item.article_text}")
    
    # Возвращаем простую строку в качестве ответа клиенту
    return "Результат в консоли!"

# Маршрут для обработки регистрации пользователя с поддержкой запросов GET и POST
@lab6.route("/lab6/register", methods=["GET", "POST"])
def register():
    # Проверяем, если метод запроса — GET
    if request.method == "GET":
        # Рендерим шаблон 'register6.html' для запросов GET
        return render_template("register6.html")
    
    # Если метод запроса — POST, извлекаем отправленные имя пользователя и пароль из данных формы
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    # Проверяем, существует ли пользователь с таким же именем в базе данных
    isUserExist = users.query.filter_by(username=username_form).first()

    # Инициализируем пустой список для хранения ошибок валидации или сообщений
    errors = []


        # Проверка, существует ли пользователь с таким именем
    if isUserExist is not None:
        # Если пользователь существует, добавляем сообщение об ошибке в список ошибок
        errors.append("Такой пользователь уже существует!")
        
        # Возвращаем шаблон 'register6.html' с сообщениями об ошибках
        return render_template("register6.html", errors=errors)

    # Проверка, что поле с именем пользователя не пусто
    elif not username_form:
        # Если поле с именем пользователя пусто, добавляем сообщение об ошибке в список ошибок
        errors.append("Введите имя пользователя!")
        
        # Возвращаем шаблон 'register6.html' с сообщениями об ошибках
        return render_template("register6.html", errors=errors)

    # Проверка, что длина пароля больше или равна 5 символам
    elif len(password_form) < 5:
        # Если длина пароля меньше 5 символов, добавляем сообщение об ошибке в список ошибок
        errors.append("Пароль должен содержать не менее 5 символов!")
        
        # Возвращаем шаблон 'register6.html' с сообщениями об ошибках
        return render_template("register6.html", errors=errors)

    # Если все проверки прошли успешно, хешируем пароль
    hashedPswd = generate_password_hash(password_form, method="pbkdf2")

    # Создаем нового пользователя с именем пользователя и хешированным паролем
    newUser = users(username=username_form, password=hashedPswd)

    # Добавляем нового пользователя в сессию базы данных и сохраняем изменения
    db.session.add(newUser)
    db.session.commit()

    # Перенаправляем пользователя на страницу входа
    return redirect("/lab6/login")

# Маршрут для обработки запросов GET и POST на странице входа
@lab6.route("/lab6/login", methods=["GET", "POST"])
def login():
    # Если метод запроса - GET, возвращаем шаблон 'login6.html' для отображения формы входа
    if request.method == "GET":
        return render_template("login6.html")
    
    # Инициализируем список ошибок
    errors = []
    
    # Получаем отправленные из формы имя пользователя и пароль
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    # Ищем пользователя с заданным именем в базе данных
    my_user = users.query.filter_by(username=username_form).first()

    # Проверка наличия введенного имени пользователя и пароля
    if not (username_form and password_form):
        # Если не введены имя пользователя и пароль, добавляем сообщение об ошибке в список
        errors.append("Введите имя пользователя и пароль!")
        # Возвращаем шаблон 'login6.html' с сообщением об ошибке
        return render_template("login6.html", errors=errors)

    # Проверка существования пользователя с введенным именем
    elif my_user is None:
        # Если пользователя с таким именем не существует, добавляем сообщение об ошибке в список
        errors.append("Такого пользователя не существует! Зарегистрируйтесь!")
        # Возвращаем шаблон 'login6.html' с сообщением об ошибке
        return render_template("login6.html", errors=errors)

    # Проверка соответствия введенного пароля хешированному паролю пользователя
    elif not check_password_hash(my_user.password, password_form):
        # Если пароль не соответствует хешированному паролю пользователя, добавляем сообщение об ошибке в список
        errors.append("Введите правильный пароль!")
        # Возвращаем шаблон 'login6.html' с сообщением об ошибке
        return render_template("login6.html", errors=errors)

    # Если все проверки успешны, выполняем вход пользователя и перенаправляем на домашнюю страницу
    elif my_user is not None:
        if check_password_hash(my_user.password, password_form):
            # Если пароль верный, выполняем вход пользователя без сохранения сессии (remember=False)
            login_user(my_user, remember=False)
            # Перенаправляем на домашнюю страницу '/lab6'
            return redirect("/lab6")
    
    # Возврат шаблона 'login6.html' при любых других сценариях
    return render_template("login6.html")


# Маршрут для отображения списка статей текущего пользователя
@lab6.route("/lab6/articles")
@login_required
def articles_list():
    # Получаем только статьи текущего пользователя из базы данных
    my_articles = articles.query.filter_by(user_id=current_user.id).all()
    # Возвращаем шаблон 'list_articles.html' с переданным списком статей
    return render_template("list_articles.html", articles=my_articles)

# Маршрут для просмотра деталей конкретной статьи
@lab6.route("/lab6/articles/<int:article_id>")
@login_required
def view_article(article_id):
    # Получаем статью по её идентификатору, или возвращаем 404 ошибку, если статья не найдена
    article = articles.query.get_or_404(article_id)
    # Возвращаем шаблон 'article_details.html' с переданной статьей
    return render_template("article_details.html", article=article)

# Маршрут для выхода пользователя из системы
@lab6.route("/lab6/logout")
@login_required
def logout():
    # Выполняем выход текущего пользователя из системы
    logout_user()
    # Перенаправляем на домашнюю страницу '/lab6'
    return redirect("/lab6")


# Определение нового маршрута в вашем Flask-приложении.
@lab6.route("/lab6/new_article", methods=["GET", "POST"])
@login_required
def create_article():
    # Этот блок выполняется, когда пользователь отправляет форму методом POST.
    if request.method == "POST":
        # Извлечение данных из отправленной пользователем формы.
        title = request.form.get("title_article")
        text = request.form.get("text_article")

        # Проверка, заполнены ли оба поля: заголовок и текст.
        if not title or not text:
            return render_template("new_article2.html", error="Пожалуйста, заполните все поля.")

        # Создание нового объекта 'articles' с указанным заголовком, текстом и ID текущего пользователя.
        new_article = articles(title=title, article_text=text, user_id=current_user.id)
        
        # Добавление новой статьи в сессию базы данных.
        db.session.add(new_article)
        
        # Фиксация изменений в базе данных.
        db.session.commit()

        # Установка флага 'sent' в True для отображения сообщения об успешной отправке на веб-странице.
        sent = True
        return render_template("new_article2.html", sent=sent)

    # Этот блок выполняется, когда пользователь обращается к маршруту с GET-запросом.
    # Он рендерит шаблон "new_article2.html".
    return render_template("new_article2.html")


