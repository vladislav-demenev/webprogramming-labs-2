from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, redirect, render_template, request, session
import psycopg2

# Создаем Blueprint с именем "lab5"
lab5 = Blueprint("lab5", __name__)

# Функции подключения и закрытия базы данных остаются без изменений
def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="knowledge_base",
        user="vladislav_knowledge_base",
        password="123"
    )
    return conn

def dbClose(cursor, connection):
    cursor.close()
    connection.close()

# Добавленная функция для проверки разрешений пользователя
def user_has_permission_to_create_article(user_id):
    conn = dbConnect()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        return result is not None
    finally:
        dbClose(cur, conn)

# Маршрут для вывода всех пользователей в консоль
@lab5.route("/lab5")
def main():
    user_is_authenticated = 'user_id' in session
    current_user = {"username": "Гость"}

    if user_is_authenticated:
        current_user["username"] = session["username"]

    return render_template("lab5.html", user_is_authenticated=user_is_authenticated, current_user=current_user)

@lab5.route("/lab5/users")
def show_users():
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")

    result = cur.fetchall()

    dbClose(cur, conn)

    return render_template("users.html", users=result)

@lab5.route('/lab5/register', methods=["GET", "POST"])
def registerPage():
    errors = []

    if request.method == "GET":
        return render_template("register.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        errors.append("Пожалуйста, заполните все поля")
        return render_template("register.html", errors=errors)

    hashPassword = generate_password_hash(password)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute(f"SELECT username FROM users WHERE username = %s;", (username,))

    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")
        conn.close()
        cur.close()
        return render_template("register.html", errors=errors)

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashPassword))
    conn.commit()
    conn.close()
    cur.close()

    return redirect("/lab5/logins")

@lab5.route('/lab5/logins', methods=["GET", "POST"])
def loginPage():
    errors = []

    if request.method == "GET":
        return render_template("logins.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        return render_template("logins.html", errors=errors)

    with dbConnect() as conn, conn.cursor() as cur:
        try:
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            result = cur.fetchone()

            if result is None:
                errors.append("Неправильный логин или пароль")
                return render_template("logins.html", errors=errors)

            userID, hashPassword = result

            if check_password_hash(hashPassword, password):
                session['user_id'] = userID
                session['username'] = username
                return redirect("/lab5")
            else:
                errors.append("Неправильный логин или пароль")
                return render_template("logins.html", errors=errors)

        except Exception as e:
            errors.append(f"Ошибка при выполнении запроса: {str(e)}")
            return render_template("logins.html", errors=errors)

@lab5.route('/lab5/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect("/lab5/logins")

@lab5.route('/lab5/new_article', methods=["GET", "POST"])
def new_article():
    if 'user_id' not in session:
        return redirect('/lab5/logins')

    user_id = session['user_id']

    if not user_has_permission_to_create_article(user_id):
        return redirect('/lab5')

    sent = False

    if request.method == "GET":
        return render_template("new_article.html", errors=[], sent=sent)
    elif request.method == "POST":
        title = request.form.get("title_article")
        text_article = request.form.get("text_article")

        if not (title and text_article):
            errors = ["Пожалуйста, заполните все поля"]
            return render_template("new_article.html", errors=errors, sent=sent)

        conn = dbConnect()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s) RETURNING id;",
                (user_id, title, text_article, True)
            )
            new_article_id = cur.fetchone()[0]
            conn.commit()

            print(f"Inserted new article with ID: {new_article_id}")

            sent = True

        except Exception as e:
            errors = [f"Ошибка при выполнении запроса: {str(e)}"]
            return render_template("new_article.html", errors=errors, sent=sent)
        finally:
            dbClose(cur, conn)

        if new_article_id is not None:
            return render_template("new_article.html", errors=[], sent=sent)
        else:
            errors = ["Не удалось получить идентификатор новой статьи"]
            return render_template("new_article.html", errors=errors, sent=sent)

@lab5.route("/lab5/articles/<int:article_id>")
def getArticle(article_id):
    user_id = session.get("user_id")  # Исправлено
    # Проверяем авторизован ли пользователь
    if user_id is not None:
        conn = dbConnect()
        cur = conn.cursor()
        # SQL injection example!!!!|
        cur.execute("SELECT title, article_text FROM articles WHERE id = %s AND user_id = %s", (article_id, user_id))
        # Возьми одну строку
        articleBody = cur.fetchone()
        dbClose(cur, conn)
        if articleBody is None: 
            return "Not found!"
        # Разбиваем строку на массив по "Enter", чтобы
        # с помощью цикла for в jinja разбить статью на параграфы
        text = articleBody[1].splitlines()
        return render_template("articleN.html", article_text=text, article_title=articleBody[0], username=session.get("username"))
    else:
        return redirect("/lab5/logins")

# Add this route in your Flask application file

@lab5.route("/lab5/my_articles")
def my_articles():
    current_user = {"username": None}  # Corrected assignment
    if 'user_id' in session:
        user_id = session['user_id']

        conn = dbConnect()
        cur = conn.cursor()

        try:
            # Retrieve articles belonging to the logged-in user
            cur.execute("SELECT id, title, article_text, likes FROM articles WHERE user_id = %s;", (user_id,))
            articles = [{'id': row[0], 'title': row[1], 'article_text': row[2], 'likes': row[3]} for row in cur.fetchall()]

            current_user["username"] = session.get("username")  # Set the username for the current user

            return render_template("articles.html", user_is_authenticated=True, articles=articles, current_user=current_user)
        finally:
            dbClose(cur, conn)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('/lab5/logins')

# Добавьте новый маршрут для добавления статьи в избранное
@lab5.route('/lab5/articles/<int:article_id>/add_to_favorite')
def add_to_favorite(article_id):
    if 'user_id' not in session:
        return redirect('/lab5/logins')

    user_id = session['user_id']

    conn = dbConnect()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE articles SET is_favorite = true WHERE id = %s AND user_id = %s;", (article_id, user_id))
        conn.commit()
    finally:
        dbClose(cur, conn)

    return redirect('/lab5/my_articles')  # Перенаправьте на страницу с избранными статьями

# Добавьте новый маршрут для лайка статьи
# Ваш текущий маршрут
@lab5.route('/lab5/like_article/<int:article_id>', methods=["POST"])
def like_article(article_id):
    if 'user_id' not in session:
        return redirect('/lab5/logins')

    user_id = session['user_id']

    conn = dbConnect()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE articles SET likes = likes + 1 WHERE id = %s;", (article_id,))
        conn.commit()

        # Получите обновленное количество лайков
        cur.execute("SELECT likes FROM articles WHERE id = %s;", (article_id,))
        likes_count = cur.fetchone()[0]

        return redirect('/lab5/my_articles')  # Перенаправление на главную страницу или куда-то еще после лайка
    finally:
        dbClose(cur, conn)
