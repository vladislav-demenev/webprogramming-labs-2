from flask import Blueprint, redirect, url_for, render_template, request
lab3 = Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    return render_template('lab3.html')


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Введите возвраст!'
    sex = request.args.get('sex')
    return render_template('form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0

    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10    

    return render_template('pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    return render_template('success.html')


@lab3.route('/lab3/train_ticket')
def trail_ticket():
    return render_template('train_ticket.html')

@lab3.route('/lab3/ticket')
def ticket():
    passenger_name = request.args.get('passenger_name')
    passenger_type = request.args.get('passenger_type')
    berth_type = request.args.get('berth_type')
    luggage = request.args.get('luggage')
    passenger_age = request.args.get('passenger_age')
    departure_point = request.args.get('departure_point')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')
    return render_template('ticket.html',passenger_name=passenger_name,passenger_type=passenger_type,berth_type=berth_type,luggage=luggage,passenger_age=passenger_age,departure_point=departure_point,destination=destination,travel_date=travel_date)