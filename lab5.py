from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, redirect, url_for, render_template, request, session
import psycopg2


# Создаем Blueprint с именем "lab5"
lab5 = Blueprint("lab5", __name__)

# Функции подключения и закрытия базы данных остаются без изменений
def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="knowledge_base",
        user="vladislav_knowledge_base",
        password="123")
    return conn

def dbClose(cursor, connection):
    cursor.close()
    connection.close()

# Маршрут для вывода всех пользователей в консоль
@lab5.route("/lab5")
def main():

    # Устанавливаем соединение с базой данных
    conn = dbConnect()

    # Создаем курсор для выполнения SQL-запросов
    cur = conn.cursor()

    # Выполняем запрос к базе данных для получения всех пользователей
    cur.execute("SELECT * FROM users;")
    
    # Получаем все строки с результатами запроса
    result = cur.fetchall()
    
    # Выводим результат в консоль (это можно убрать в боевом приложении)
    print(result)
    
    # Закрываем курсор и соединение с базой данных
    dbClose(cur, conn)
    
    return render_template('lab5.html')

# Маршрут для вывода имен пользователей в HTML
@lab5.route("/lab5/users")
def show_users():
    # Устанавливаем соединение с базой данных
    conn = dbConnect()

    # Создаем курсор для выполнения SQL-запросов
    cur = conn.cursor()

    # Выполняем запрос к базе данных для получения всех пользователей
    cur.execute("SELECT * FROM users;")
    
    # Получаем все строки с результатами запроса
    result = cur.fetchall()
    
    # Закрываем курсор и соединение с базой данных
    dbClose(cur, conn)

    # Рендерим HTML-шаблон "users.html" с данными пользователей
    return render_template("users.html", users=result)

@lab5.route('/lab5/register', methods=["GET", "POST"])
def registerPage():
    errors = []
    
    # Если это метод GET, то вернуть шаблон и завершить выполнение
    if request.method == "GET":
        return render_template("register.html", errors=errors)
    
    # Если мы попали сюда, значит это метод POST, так как GET мы уже обработали и сделали return.
    # После return функция немедленно завершается
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Проверяем username и password на пустоту
    # Если любой из них пустой, то добавляем ошибку и рендерим шаблон
    if not (username and password):
        errors.append("Пожалуйста, заполните все поля")
        print(errors)
        return render_template("register.html", errors=errors)
    
    hashPassword=generate_password_hash(password)

    conn = dbConnect()
    cur = conn.cursor()
    
    cur.execute(f"SELECT username FROM users WHERE username = '{username}';")
    
    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")
        conn.close()
        cur.close()
        return render_template("register.html", errors=errors)
    
    # Если мы попали сюда, то значит в cur.fetchone нет ни одной строки
    # значит пользователя с таким же логином не существует
    cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashPassword}');")
    
    # Делаем commit - т.е. фиксируем изменения
    conn.commit()
    conn.close()
    cur.close()

    return redirect("/lab5/login")

@lab5.route('/lab5/login', methods=["GET", "POST"])
def loginPage():
    errors = []

    if request.method == "GET":
        return render_template("login.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        return render_template("login.html", errors=errors)

    with dbConnect() as conn, conn.cursor() as cur:
        try:
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            result = cur.fetchone()

            if result is None:
                errors.append("Неправильный логин или пароль")
                return render_template("login.html", errors=errors)

            userID, hashPassword = result

            if check_password_hash(hashPassword, password):
                session['id'] = userID
                session['username'] = username
                return redirect("/lab5")
            else:
                errors.append("Неправильный логин или пароль")
                return render_template("login.html", errors=errors)

        except Exception as e:
            errors.append(f"Ошибка при выполнении запроса: {str(e)}")
            return render_template("login.html", errors=errors)



    