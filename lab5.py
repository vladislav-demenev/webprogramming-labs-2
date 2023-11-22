from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, redirect, render_template, request, session
import psycopg2

lab5 = Blueprint("lab5", __name__)

# Функции подключения и закрытия базы данных
def dbConnect():
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="knowledge_base",
        user="vladislav_knowledge_base",
        password="123"
    )
    return conn

def dbClose(cursor, connection):
    # Закрытие курсора и соединения с базой данных
    cursor.close()
    connection.close()

# Функция для проверки разрешений пользователя
def user_has_permission_to_create_article(user_id):
    # Подключение к базе данных
    conn = dbConnect()
    cur = conn.cursor()

    try:
        # Проверка существования пользователя с указанным ID
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,)) #Это сам SQL-запрос. В данном случае, он выбирает id из таблицы users, где значение id равно заданному значению, переданному через параметр.
        result = cur.fetchone() #извлекает одну строку из результата запроса.
        return result is not None #указывает, что у пользователя есть права на создание статьи.
    finally:
        # Закрытие курсора и соединения с базой данных
        dbClose(cur, conn)

# Маршрут для вывода всех пользователей в консоль
@lab5.route("/lab5")
def main():
    # Проверка аутентификации пользователя
    user_is_authenticated = 'user_id' in session
#Эта строка создает переменную user_is_authenticated, которая проверяет, есть ли ключ "user_id" в объекте сеанса (session). Если этот ключ присутствует, то считается, что пользователь аутентифицирован.
    current_user = {"username": "Гость"}
#Создается словарь current_user, представляющий информацию о текущем пользователе. В данном случае, устанавливается значение "Гость
    if user_is_authenticated:
        # Если пользователь аутентифицирован, установить его имя пользователя
        current_user["username"] = session["username"]

    # Отображение главной страницы
    return render_template("lab5.html", user_is_authenticated=user_is_authenticated, current_user=current_user)

@lab5.route("/lab5/users")
def show_users(): #обработчик
    # Подключение к базе данных
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;") #Этот код выполняет SQL-запрос, выбирая все столбцы (*) из таблицы users. Результат запроса будет содержать информацию о всех пользователях в базе данных.

    # Получение всех пользователей из базы данных
    result = cur.fetchall()#извлекает одну строку из результата запроса

    # Закрытие курсора и соединения с базой данных
    dbClose(cur, conn)#закрывает курсор и соединение с базой данных

    # Отображение страницы с пользователями
    return render_template("users.html", users=result)

@lab5.route('/lab5/register', methods=["GET", "POST"]) #Эта строка указывает на создание обработчика маршрута для пути
def registerPage(): #является обработчиком для данного маршрута
    errors = []
#Если метод запроса - GET, то отображается страница регистрации с формой. Переменная errors передается в шаблон для отображения возможных ошибок.
    if request.method == "GET":
        # Отображение страницы регистрации при GET-запросе
        return render_template("register.html", errors=errors)

    # Получение данных формы при POST-запросе
    #Если метод запроса - POST, то извлекаются данные формы из запроса. Это делается с использованием объекта request
    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        # Проверка наличия заполненных полей
        errors.append("Пожалуйста, заполните все поля")
        return render_template("register.html", errors=errors)
#Проверяется, заполнены ли оба поля формы (имя пользователя и пароль). Если нет, то добавляется соответствующее сообщение об ошибке
    # Хеширование пароля
    hashPassword = generate_password_hash(password)
#Пароль хешируется с использованием функции generate_password_hash из Flask. Это обеспечивает безопасное хранение пароля в базе данных.
    # Подключение к базе данных
    conn = dbConnect()
    cur = conn.cursor()
#Устанавливается соединение с базой данных и создается курсор. Затем выполняется запрос на проверку уникальности имени пользователя и, если проверка проходит успешно, происходит вставка нового пользователя в базу данных
    cur.execute(f"SELECT username FROM users WHERE username = %s;", (username,))

    if cur.fetchone() is not None:
        # Проверка уникальности имени пользователя
        errors.append("Пользователь с данным именем уже существует")
        conn.close()
        cur.close()
        return render_template("register.html", errors=errors)
#Если имя пользователя уже существует в базе данных, то добавляется сообщение об ошибке, и соединение с базой данных закрывается.
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashPassword))
    conn.commit()
    conn.close()
    cur.close()
#Если проверки пройдены успешно, то транзакция фиксируется, и соединение с базой данных закрывается.
    # Перенаправление на страницу логина после успешной регистрации
    return redirect("/lab5/logins")

@lab5.route('/lab5/logins', methods=["GET", "POST"])
def loginPage():#является обработчиком для данного маршрута
    errors = []
#Если метод запроса - GET, то отображается страница входа с формой. Переменная errors передается в шаблон для отображения возможных ошибок.
    if request.method == "GET":
        # Отображение страницы логина при GET-запросе
        return render_template("logins.html", errors=errors)

    # Получение данных формы при POST-запросе
    username = request.form.get("username")
    password = request.form.get("password")
#Если метод запроса - POST, то извлекаются данные формы из запроса. Это делается с использованием объекта request из Flask.
    if not (username or password):
        # Проверка наличия заполненных полей
        errors.append("Пожалуйста, заполните все поля")#используется для добавления элемента в конец списка
        return render_template("logins.html", errors=errors)
#Проверяется, заполнены ли оба поля формы (имя пользователя и пароль). Если нет, то добавляется соответствующее сообщение об ошибке
    with dbConnect() as conn, conn.cursor() as cur:
#Используется конструкция with для обеспечения правильного закрытия соединения и курсора даже в случае возникновения исключения.
        try:
            # Проверка правильности логина и пароля
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
#Выполняется SQL-запрос для выбора id и password из таблицы users, где username соответствует введенному имени пользователя.
            if result is None:
                errors.append("Неправильный логин или пароль")
                return render_template("logins.html", errors=errors)
#Если результат запроса равен None, это означает, что в базе данных не был найден пользователь с введенным именем (username). В таком случае, добавляется сообщение об ошибке в список errors
            userID, hashPassword = result
#Если результат запроса не равен None, значит, был найден пользователь с введенным именем. Далее извлекаются данные пользователя: userID и хешированный пароль (hashPassword).
 
#Затем проверяется введенный пароль с хешированным паролем в базе данных с использованием функции check_password_hash из Flask. Если пароль верен, то аутентификация считается успешной.
            if check_password_hash(hashPassword, password):
                # Успешная аутентификация
                session['user_id'] = userID
                session['username'] = username
                return redirect("/lab5")
            else:
                errors.append("Неправильный логин или пароль")
                return render_template("logins.html", errors=errors)
#В случае возникновения исключения при выполнении запроса к базе данных, добавляется сообщение об ошибке в список errors. Это может произойти, например, если произошла ошибка в самом SQL-запросе или при взаимодействии с базой данных.
        except Exception as e:
            errors.append(f"Ошибка при выполнении запроса: {str(e)}")
            return render_template("logins.html", errors=errors)
#В случае возникновения исключения, ошибка перехватывается, и выполняется код в блоке except. В данном коде добавляется сообщение об ошибке (включающее текст самой ошибки str(e)) в список 
@lab5.route('/lab5/logout')
def logout():
    # Выход пользователя из системы
    #Здесь используется метод pop() для удаления значений из сеанса. В данном случае, удаляются ключи 'user_id' и 'username'. Если ключи не существуют в сеансе, метод pop() возвращает None.
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect("/lab5/logins")

@lab5.route('/lab5/new_article', methods=["GET", "POST"])
def new_article():
    # Проверка аутентификации пользователя
    #Если в сеансе нет информации о пользователе (то есть пользователь не аутентифицирован), происходит перенаправление на страницу входа
    if 'user_id' not in session:
        return redirect('/lab5/logins')
#Проверяется, есть ли у пользователя разрешение на создание статьи. Если нет, происходит перенаправление на главную страницу
    user_id = session['user_id']

    if not user_has_permission_to_create_article(user_id):
        # Проверка разрешений пользователя на создание статьи
        return redirect('/lab5')

    sent = False
#Если запрос пришел методом GET, отображается страница создания новой статьи с пустым списком ошибок и флагом sent равным False
    if request.method == "GET":
        # Отображение страницы создания новой статьи при GET-запросе
        return render_template("new_article.html", errors=[], sent=sent)
#Если запрос пришел методом POST, извлекаются данные формы (заголовок и текст статьи)
    elif request.method == "POST":
        # Получение данных формы при POST-запросе
#Эти строки кода предназначены для получения значений, введенных пользователем в поля формы с соответствующими именами ("title_article" и "text_article")
        title = request.form.get("title_article")
        text_article = request.form.get("text_article")
#Если хотя бы одно из полей не заполнено, добавляется сообщение об ошибке в список errors, и страница отображается снова с сообщением об ошибке.
        if not (title and text_article):
            # Проверка наличия заполненных полей
            errors = ["Пожалуйста, заполните все поля"]
            return render_template("new_article.html", errors=errors, sent=sent)

        # Подключение к базе данных
        conn = dbConnect()
        cur = conn.cursor()

        try:
            # Вставка новой статьи в базу данных
            # В этой строке кода выполняется SQL-запрос, который вставляет новую статью в таблицу "articles". Значения для вставки берутся из переменных user_id, title, text_article, и True
            cur.execute(
                "INSERT INTO articles (user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s) RETURNING id;",
                (user_id, title, text_article, True)
            )
        #После выполнения запроса используется метод fetchone(), чтобы получить первую строку результата запроса. Затем из этой строки извлекается значение идентификатора статьи
            new_article_id = cur.fetchone()[0]
        #Эта строка кода фиксирует изменения в базе данных, сделанные в пределах текущей транзакции.
            conn.commit()
#Здесь выводится информация о вставленной статье, включая ее идентификатор.
            print(f"Inserted new article with ID: {new_article_id}")
#Если код успешно дошел до этого момента, это означает, что вставка статьи выполнена успешно, и флаг sent устанавливается в True
            sent = True
#Если в блоке try произошла ошибка (в данном случае, при выполнении SQL-запроса), код переходит в блок except, где создается список ошибок, содержащий сообщение об ошибке. Затем происходит возврат к шаблону "new_article.html" с передачей списка ошибок 
        except Exception as e:
            errors = [f"Ошибка при выполнении запроса: {str(e)}"]
            return render_template("new_article.html", errors=errors, sent=sent)
        finally:
            # Закрытие курсора и соединения с базой данных
            dbClose(cur, conn)
#Здесь проверяется, был ли успешно получен идентификатор новой статьи после вставки. Если переменная new_article_id не является None, то это означает, что идентификатор был получен успешно.
        if new_article_id is not None:
            return render_template("new_article.html", errors=[], sent=sent)
        else:
            errors = ["Не удалось получить идентификатор новой статьи"]
            return render_template("new_article.html", errors=errors, sent=sent)

@lab5.route("/lab5/articles/<int:article_id>") #это часть маршрута, которая ожидает целочисленное значение и передает его в аргумент article_id функции getArticle
def getArticle(article_id): 
    user_id = session.get("user_id")  # Получение ID пользователя из сессии
    # Проверка аутентификации пользователя
    if user_id is not None: #Извлекается ID пользователя из сессии, если таковой присутствует. Если пользователь не аутентифицирован, user_id будет равен None
        conn = dbConnect()
        cur = conn.cursor()
        # при выполнении этого запроса, база данных вернет результат, содержащий title и article_text для статьи, удовлетворяющей условиям id и user_id.
        cur.execute("SELECT title, article_text FROM articles WHERE id = %s AND user_id = %s", (article_id, user_id)) #%s является местозаполнителем (placeholder) для параметров запроса. Он представляет собой маркер, который будет заменен на конкретное значение при выполнении SQL-запроса.
        # Получение одной строки из результата запроса
        articleBody = cur.fetchone() #метод fetchone(), чтобы получить первую строку результата запроса
        dbClose(cur, conn)
#Если articleBody равно None, то статья не найдена, и возвращается строка "Not found!
        if articleBody is None: 
            return "Not found!"
        # Разделение текста статьи на абзацы
        #Текст статьи разделяется на абзацы с использованием метода splitlines()
        text = articleBody[1].splitlines()
        return render_template("articleN.html", article_text=text, article_title=articleBody[0], username=session.get("username"))
    else:
        # Перенаправление на страницу логина, если пользователь не аутентифицирован
        return redirect("/lab5/logins")

# Добавление маршрута для отображения статей пользователя
@lab5.route("/lab5/my_articles")
def my_articles():
#Проверяется, присутствует ли user_id в сессии. Если пользователь аутентифицирован, его ID сохраняется в переменной user_id.
    current_user = {"username": None} 
    if 'user_id' in session:
        user_id = session['user_id']

        conn = dbConnect()
        cur = conn.cursor()

        try:
            # Получение статей, принадлежащих текущему пользователю
            #В этом запросе выбираются столбцы id, title, article_text и likes из таблицы articles, где значение столбца user_id равно переданному значению user_id.
            cur.execute("SELECT id, title, article_text, likes FROM articles WHERE user_id = %s;", (user_id,))
#После выполнения запроса вызывается метод fetchall(), который возвращает список кортежей, представляющих результаты запроса. Затем создается список словарей (articles), где каждый словарь представляет одну статью. Словари содержат ключи 'id', 'title', 'article_text' и 'likes', соответствующие столбцам выборки.
            articles = [{'id': row[0], 'title': row[1], 'article_text': row[2], 'likes': row[3]} for row in cur.fetchall()]

            current_user["username"] = session.get("username")  # Установка имени пользователя для текущего пользователя

            return render_template("articles.html", user_is_authenticated=True, articles=articles, current_user=current_user)
        finally:
            # Закрытие курсора и соединения с базой данных
            dbClose(cur, conn)
    else:
        # Если пользователь не аутентифицирован, перенаправление на страницу логина
        return redirect('/lab5/logins')

# Добавление маршрута для добавления статьи в избранное
@lab5.route('/lab5/articles/<int:article_id>/add_to_favorite')#Этот маршрут обрабатывает запросы
def add_to_favorite(article_id):
#Если в сессии нет идентификатора пользователя (user_id), то происходит перенаправление на страницу логина.
    if 'user_id' not in session:
        return redirect('/lab5/logins')
#Если пользователь аутентифицирован, извлекается его идентификатор из сессии.
    user_id = session['user_id']
#Создается соединение с базой данных, создается курсор, и затем выполняется SQL-запрос 
    conn = dbConnect()#подключение
    cur = conn.cursor()#выполнение sql

    try:
        # Обновление флага "избранное" для статьи
#В этом запросе выполняется обновление записей в таблице articles. Значение true устанавливается в столбце is_favorite для тех записей, где значение столбца id равно переданному значению article_id, и значение столбца user_id равно переданному значению user_id.
        cur.execute("UPDATE articles SET is_favorite = true WHERE id = %s AND user_id = %s;", (article_id, user_id))
#После выполнения запроса метод commit() вызывается для фиксации изменений в базе данных
        conn.commit()
    finally:
        # Закрытие курсора и соединения с базой данных
        dbClose(cur, conn)

    # Перенаправление на страницу со статьями пользователя
    return redirect('/lab5/my_articles')
