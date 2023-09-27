from flask import Flask, redirect, url_for, render_template 
app=Flask(__name__)

@app.route("/")
def slesh():
    return redirect('/menu', code=302)


@app.route("/index")
def start():
    return redirect('/menu', code=302)


@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Деменев Владислав Вячеславович, Лабораторная 1</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <div>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.         
        </div>

        <h1><a href="/menu" target="_blank">Меню</a></h1>
        <h2>Реализованные роуты</h2>

        <ul>
            <li><a href="/lab1/oak" target="_blank">/lab1/oak - Дуб</a></li>
            <li><a href="/lab1/student" target="_blank">/lab1/student - Студент</a></li>
            <li><a href="/lab1/python" target="_blank">/lab1/python - Питон</a></li>
            <li><a href="/lab1/lamba" target="_blank">/lab1/lamba - Ламборгини </a></li>
        </ul>
        <footer>
            &copy; Владислав Деменев, ФБИ-13, 3 курс, 2023
        </footer>
    </body>
</html>
'''

@app.route('/menu')
def menu():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
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
'''

@app.route('/lab1/oak')
def oak():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>   
    <body>
        <h1>Дуб</h1>
        <h1><a href="/menu" target="_blank">Меню</a></h1>  
        <div class='photo'><img src="''' + url_for('static', filename='oak.jpg') + '''">
        </div> 

        
    </body>
</html>    
'''

@app.route('/lab1/student')
def student():
    return '''
<!doctype html>
<html>
    <head>
        <title>Деменев Владислав Вячеславович</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h1>
           Деменев Владислав Вячеславович
        </h1>

        <h1><a href="/menu" target="_blank">Меню</a></h1>

        <div class='photo'><img src="''' + url_for('static', filename='ngtu.png') + '''">
    </body>
</html>
'''

@app.route('/lab1/python')
def python():
    return '''
<!doctype html>
<html>
    <head>
        <title>Деменев Владислав Вячеславович</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h2>
           Python в русском языке встречаются названия пито́н[24] или па́йтон) — высокоуровневый 
           язык программирования общего назначения с динамической строгой типизацией и автоматическим 
           управлением памятью, ориентированный на повышение производительности разработчика, 
           читаемости кода и его качества, а также на обеспечение переносимости написанных на нём программ.
            Язык является полностью объектно-ориентированным в том плане, что всё является объектами.
            Необычной особенностью языка является выделение блоков кода пробельными отступами. 
            Синтаксис ядра языка минималистичен, за счёт чего на практике редко возникает необходимость обращаться к документации.
            Сам же язык известен как интерпретируемый и используется в том числе для написания скриптов. 
            Недостатками языка являются зачастую более низкая скорость работы и более высокое потребление 
            памяти написанных на нём программ по сравнению с аналогичным кодом, написанным на компилируемых языках, таких как C или C++.
        </h2>
        <h2>
           Python является мультипарадигменным языком программирования, поддерживающим императивное, процедурное, структурное, 
           объектно-ориентированное программирование, метапрограммирование и функциональное программирование. Задачи 
           обобщённого программирования решаются за счёт динамической типизации. Аспектно-ориентированное программирование 
           частично поддерживается через декораторы, более полноценная поддержка обеспечивается дополнительными фреймворками.
            Такие методики как контрактное и логическое программирование можно реализовать с помощью библиотек или расширений. 
            Основные архитектурные черты — динамическая типизация, автоматическое управление памятью, полная интроспекция, механизм
            обработки исключений, поддержка многопоточных вычислений с глобальной блокировкой интерпретатора (GIL), высокоуровневые
            структуры данных. Поддерживается разбиение программ на модули, которые, в свою очередь, могут объединяться в пакеты.
        </h2>
        <h2>
           Эталонной реализацией Python является интерпретатор CPython, который поддерживает большинство активно используемых платформ и 
           являющийся стандартом де-факто языка. Он распространяется под свободной лицензией Python Software Foundation License, 
           позволяющей использовать его без ограничений в любых приложениях, включая проприетарные. CPython компилирует исходные тексты 
           в высокоуровневый байт-код, который исполняется в стековой виртуальной машине. К другим трём основным реализациям языка относятся Jython
             (для JVM), IronPython (для CLR/.NET) и PyPy. PyPy написан на подмножестве языка Python (RPython) и разрабатывался как альтернатива 
             CPython с целью повышения скорости исполнения программ, в том числе за счёт использования JIT-компиляции. Поддержка версии Python 2 
             закончилась в 2020 году. На текущий момент активно развивается версия языка Python 3. Разработка языка ведётся через предложения
               по расширению языка PEP (англ. Python Enhancement Proposal), в которых описываются нововведения, делаются корректировки согласно обратной
            связи от сообщества и документируются итоговые решения.
        </h2>
        <h1><a href="/menu" target="_blank">Меню</a></h1>
        <div class='photo'><img src="''' + url_for('static', filename='python.jpg') + '''">
    </body>
</html>
'''

@app.route('/lab1/lamba')
def lamba():
    return '''
<!doctype html>
<html>
    <head>
        <title>Деменев Владислав Вячеславович</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <h2>
           Automobili Lamborghini S.p.A. — итальянская компания, производитель дорогих спортивных автомобилей под маркой Lamborghini.
            Находится в коммуне Сант-Агата-Болоньезе, около Болоньи. Компания основана в 1963 году Ферруччо Ламборгини; на тот момент 
            он уже был владельцем крупной компании по производству тракторов.
        </h2>
        <h2>
           В начале 1960-х годов Ферруччо Ламборгини был владельцем нескольких компаний и мог себе позволить приобретать дорогие автомобили.
             В разное время у него были Mercedes 300SL, несколько Maserati 3500 GT, Jaguar E-type. Он также владел Ferrari 250 GT разных версий.
               Но в каждом автомобиле он находил некоторые недочёты.
        </h2>
        <h2>
           Существует несколько версий о причинах, по которым Ламборгини основал собственную фирму. Все эти версии сводятся к конфликту между
             Энцо Феррари (владельцем компании Ferrari) и Ферруччо Ламборгини. Наиболее популярная версия, рассказанная сыном Ферруччо Ламборгини, 
             гласит, что Ламборгини приехал на фабрику к Энцо Феррари пожаловаться на качество сцепления в своём автомобиле Ferrari 250 GT. Энцо 
             отправил Ламборгини обратно с пожеланием и дальше заниматься тракторами, потому что в автомобилях, а тем более спортивных, Ламборгини
            ничего не понимает. Ламборгини вернулся на фабрику, разобрал трансмиссию в своём Ferrari 250 GT и обнаружил, что производитель многих 
            деталей тот же, что и в тракторах Lamborghini. На своих складах он нашёл подходящую замену, и после сборки проблема была решена.
        </h2>
        <h1><a href="/menu" target="_blank">Меню</a></h1>
        <div class='photo'><img src="''' + url_for('static', filename='lamba.png') + '''">
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name='Владислав Деменев'
    number='2'
    groupe='ФБИ-13'
    course='3'
    return render_template('example.html', name=name, number=number, groupe=groupe, course=course)