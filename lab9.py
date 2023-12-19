from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')

@lab9.app_errorhandler(404)
def not_found(e):
    return 'Нет такой страницы, вернуться обратно <a href="/menu">Меню</a> ❄️❄️❄️', 404


@lab9.route('/lab9/500')
def main1():
    return render_template('lab9/500.html'), 500
