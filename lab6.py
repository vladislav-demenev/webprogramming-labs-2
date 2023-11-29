from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from Db import db
from Db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

lab6 = Blueprint("lab6", __name__)

@lab6.route("/lab6")
def main():
    user_is_authenticated = 'user_id' in session
    current_user_info = {"username": "Гость"}

    if user_is_authenticated:
        current_user_info["username"] = session["username"]

    return render_template("lab6.html", user_is_authenticated=user_is_authenticated, current_user=current_user_info)

@lab6.route("/lab6/check")
def main1():
    my_users = users.query.all()
    print(my_users)
    return "result in console!"

@lab6.route("/lab6/checkarticles")
def mainart():
    my_articles = articles.query.all()
    for article_item in my_articles:
        print(f"{article_item.title}-{article_item.article_text}")
    return "Result in console!"

@lab6.route("/lab6/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register6.html")
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    isUserExist = users.query.filter_by(username=username_form).first()

    errors = []

    if isUserExist is not None:
        errors.append("Такой пользователь уже существует!")
        return render_template("register6.html", errors=errors)
    elif not username_form:
        errors.append("Введите имя пользователя!")
        return render_template("register6.html", errors=errors)
    elif len(password_form) < 5:
        errors.append("Пароль должен содержать не менее 5 символов!")
        return render_template("register6.html", errors=errors)

    hashedPswd = generate_password_hash(password_form, method="pbkdf2")

    newUser = users(username=username_form, password=hashedPswd)

    db.session.add(newUser)
    db.session.commit()

    return redirect("/lab6/login")

@lab6.route("/lab6/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login6.html")
    
    errors = []
    
    username_form = request.form.get("username")
    password_form = request.form.get("password")

    my_user = users.query.filter_by(username=username_form).first()

    if not (username_form and password_form):
        errors.append("Введите имя пользователя и пароль!")
        return render_template("login6.html", errors=errors)
    elif my_user is None:
        errors.append("Такого пользователя не существует! Зарегистрируйтесь!")
        return render_template("login6.html", errors=errors)
    elif not check_password_hash(my_user.password, password_form):
        errors.append("Введите правильный пароль!")
        return render_template("login6.html", errors=errors)
    elif my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect("/lab6")
    
    return render_template("login6.html")

@lab6.route("/lab6/articles")
@login_required
def articles_list():
    # Получаем только статьи текущего пользователя
    my_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template("list_articles.html", articles=my_articles)

@lab6.route("/lab6/articles/<int:article_id>")
@login_required
def view_article(article_id):

    article = articles.query.get_or_404(article_id)
    return render_template("article_details.html", article=article)

@lab6.route ("/lab6/logout")
@login_required
def logout():
    logout_user()
    return redirect ("/lab6")

@lab6.route("/lab6/new_article", methods=["GET", "POST"])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form.get("title_article")
        text = request.form.get("text_article")

        # Проверка наличия данных
        if not title or not text:
            return render_template("new_article2.html", error="Пожалуйста, заполните все поля.")

        new_article = articles(title=title, article_text=text, user_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()

        # Установите флаг sent для отображения сообщения об успешной отправке
        sent = True
        return render_template("new_article2.html", sent=sent)

    # Ваш текущий код для GET-запроса остается здесь
    return render_template("new_article2.html")

