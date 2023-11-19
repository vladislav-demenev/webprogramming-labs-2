from flask import Flask, render_template, Blueprint
import psycopg2

app = Flask(__name__)

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

# Регистрация Blueprint в приложении Flask
app.register_blueprint(lab5)

if __name__ == "__main__":
    # Запуск приложения Flask в режиме отладки
    app.run(debug=True)