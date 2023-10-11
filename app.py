from flask import Flask, redirect, url_for, render_template 
from lab1 import lab1

app=Flask(__name__)
app.register_blueprint(lab1)

@app.route('/lab2')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/example')
def example():
    name, number, groupe, course='Владислав Деменев', 2, 'ФБИ-13', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95}, 
        {'name': 'манго', 'price': 321},
    ]

    books = [
        {'author': 'Маргарет Митчелл', 'name': 'Унесенные ветром', 'genre': 'роман', 'pages': '1056'},
        {'author': 'Джордж Оруэлл', 'name': '1984', 'genre': 'роман', 'pages': '1152'},
        {'author': 'Михаил Булгаков', 'name': 'Мастер и Маргарита', 'genre': 'роман-эпопея', 'pages': '1360'},
        {'author': 'Лев Толстой', 'name': 'Война и мир', 'genre': 'роман', 'pages': '1376'},
        {'author': 'Харпер Ли', 'name': 'Убить пересмешника', 'genre': 'роман', 'pages': '1424'},
        {'author': 'Эмили Бронте', 'name': 'Грозовой перевал', 'genre': 'роман', 'pages': '1472'},
        {'author': 'Рэй Брэдбери', 'name': '451° по Фаренгейту', 'genre': 'роман', 'pages': '1492'},
        {'author': 'Владимир Набоков', 'name': 'Лолита', 'genre': 'роман', 'pages': '1774'},
        {'author': 'Артур Конан Дойл', 'name': 'Весь Шерлок Холмс', 'genre': 'роман', 'pages': '3031'},
        {'author': 'Габриэль Гарсиа Маркес', 'name': 'Недобрый час', 'genre': 'биография', 'pages': '3600'},
    ]
    return render_template('example.html', name=name, number=number, groupe=groupe, course=course, fruits=fruits, books=books)

@app.route('/lab2/s_class')
def s_class():
    return render_template('s_class.html')