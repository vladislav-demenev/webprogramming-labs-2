from flask import Blueprint, render_template, request, redirect, session, abort

# Создание Flask Blueprint с именем 'lab7'
lab7 = Blueprint('lab7', __name__)

# Роут для отображения главной страницы
@lab7.route('/lab7/')
def main():
   return render_template('lab7/index.html')

# Роут для отображения страницы выбора напитка
@lab7.route('/lab7/drink')
def drink():
   return render_template('lab7/drink.html')

# Роут API для обработки POST-запросов
@lab7.route('/lab7/api', methods=['POST'])
def api():
   data = request.json

   # Обработка запроса 'get-price'
   if data['method'] == 'get-price':
       return get_price(data['params'])

   # Обработка запроса 'pay'/
   if data['method'] == 'pay':
       return pay(data['params'])

   # Если метод не определен или неверен, вернуть ошибку 400
   abort(400)

# Функция для получения цены напитка
def get_price(params):
   return {"result": calculate_price(params), "errors": None}

# Функция для расчета цены напитка на основе параметров
def calculate_price(params):
   drink = params['drink']
   milk = params['milk']
   sugar = params['sugar']

   # Определение цены в зависимости от выбранного напитка
   if drink == 'coffee':
       price = 120
   elif drink == 'black-tea':
       price = 80
   else:
       price = 70

   # Добавление цены за молоко и сахар, если выбраны
   if milk:
       price += 30
   if sugar:
       price += 10

   return price

# Функция для обработки платежа
def pay(params):
   card_num = params['card_num']

   # Проверка формата номера карты
   if len(card_num) != 16 or not card_num.isdigit():
       return {"result": None, "error": "Неверный номер карты"}

   cvv = params['cvv']

   # Проверка формата CVV
   if len(cvv) != 3 or not cvv.isdigit():
       return {"result": None, "error": "Неверный номер CVV/CVC"}

   # Расчет цены и возврат результата платежа
   price = calculate_price(params)
   return {"result": f'С карты {card_num} списано {price} руб', "error": None}

# Роут для обработки запросов на возврат
@lab7.route('/lab7/refund', methods=['POST'])
def refund():
   data = request.json

   # Извлечение данных о карте, напитке, молоке и сахаре из запроса
   card_num = data['params']['card_num']
   cvv = data['params']['cvv']
   drink = data['params']['drink']
   milk = data['params']['milk']
   sugar = data['params']['sugar']

   # Проверка валидности номера карты
   if not is_valid_card(card_num):
       return {"result": None, "error": "Неверный номер карты"}

   # Проверка валидности CVV
   if not is_valid_cvv(cvv):
       return {"result": None, "error": "Неверный номер CVV/CVC"}

   # Расчет суммы возврата и возврат результата
   refund_amount = calculate_price(data['params'])
   return {"result": f'Деньги вернулись на карту: {refund_amount} руб', "error": None}

# Функция для проверки валидности номера карты
def is_valid_card(card_num):
   return len(card_num) == 16 and card_num.isdigit()

# Функция для проверки валидности CVV
def is_valid_cvv(cvv):
   return len(cvv) == 3 and cvv.isdigit()