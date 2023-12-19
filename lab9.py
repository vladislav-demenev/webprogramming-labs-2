from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')