from flask import Blueprint,render_template, request, redirect, session, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/drink')
def drink():
    return render_template('lab7/drink.html')

@lab7.route('/lab7/api', methods = ['POST'])
def api():
    data = request.json

    if data['method'] == 'get-price':
        return get_price(data['params'])
    
    if data['method'] == 'pay':
        return pay(data['params'])
    
    abort(400)

def get_price(params):
    return {"result": calculate_price(params), "errors": None}

def calculate_price(params):
    drink = params['drink']
    milk = params['milk']
    sugar = params['sugar']

    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if milk:
        price += 30
    if sugar:
        price += 10

    return price

def pay(params):
    card_num = params['card_num']
    if len(card_num) != 16 or not card_num.isdigit():
        return{"result":None, "error": "Неверный номер карты"}
    
    cvv = params['cvv']
    if len(cvv) != 3 or not cvv.isdigit():
        return{"result":None, "error": "Неверный номер CVV/CVC"}
    
    price = calculate_price(params)
    return{"result": f'С карты {card_num} списано {price} руб', "error": None}


@lab7.route('/lab7/refund', methods=['POST'])
def refund():
    data = request.json

    card_num = data['params']['card_num']
    cvv = data['params']['cvv']
    drink = data['params']['drink']
    milk = data['params']['milk']
    sugar = data['params']['sugar']

    if not is_valid_card(card_num):
        return {"result": None, "error": "Неверный номер карты"}

    if not is_valid_cvv(cvv):
        return {"result": None, "error": "Неверный номер CVV/CVC"}

    refund_amount = calculate_price(data['params'])
    return {"result": f'Деньги вернулись на карту: {refund_amount} руб', "error": None}

def is_valid_card(card_num):
    return len(card_num) == 16 and card_num.isdigit()

def is_valid_cvv(cvv):
    return len(cvv) == 3 and cvv.isdigit()