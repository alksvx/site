from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/products')
def products():
    return render_template ('products.html')

@app.route('/contacts')
def contacts():
    return 'Контакты'

@app.route('/about')
def about():
    return 'О компании'

@app.route('/cart')
def cart():
    return render_template ('cart.html')

@app.route('/order', methods = ['GET', 'POST'])
def order():
    if request.method == 'POST':
        for key in request.form:
            if request.form[key] == '':
                return render_template('order.html', error = 'Не все поля заполнены')
            if key == 'email':
                if not re.match('\w+@\w+\.(ru|com)', request.form[key]):   #текст@текст.ru или com
                    return render_template('order.html', error='Неправильный формат почты')
            if key == 'phone_number':
                if not re.match('\+7\d{9}', request.form[key]):   #+7 и 9 цифр
                    return render_template('order.html', error='Неправильный формат телефона')
        return render_template('order_list.html', **request.form)
    return render_template ('order.html')

@app.route('/order_list')
def order_list():
    return render_template ('order_list.html')

if __name__ == '__main__':
    app.run()