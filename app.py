from flask import Flask, redirect, url_for
app=Flask(__name__)

@app.route("/")
def slesh():
    return redirect('/menu', code=302)


@app.route("/index")
def start():
    return redirect('/menu', code=302)


@app.route('/lab1')
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Деменев Владислав Вячеславович, Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.         
            <a href="/lab1/oak" target="_blank">Дуб</a>
        </h1>

        <footer>
            &copy; Владислав Деменев, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
"""

@app.route('/menu')
def menu():
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <h2><a href="/lab1" target="_blank">Первая лабораторная</a></h2>

        <footer>
            &copy; Владислав Деменев, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
"""

@app.route('/lab1/oak')
def oak():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>   
    <body>
        <h1><a href="/lab1" target="_blank">Дуб</a></h1>
        <div class='photo'><img src="''' + url_for('static', filename='oak.jpg') + '''">
        </div>    
    </body>
'''