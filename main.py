from flask import Flask, render_template, request, redirect, url_for
import re
from datetime import datetime, timedelta
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
app = Flask(__name__)

app.config.update(SECRET_KEY = 'WOW')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __int__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(login):
    if login == 'admin':
        return User(login)


@login_required
@app.route('/')
def index():
    return render_template ('index.html')


@login_required
@app.route('/products')
def products():
    return render_template ('products.html')


@login_required
@app.route('/contacts')
def contacts():
    return render_template ('contacts.html')


@login_required
@app.route('/about')
def about():
    return render_template ('about.html')


@login_required
@app.route('/cart')
def cart():
    return render_template ('cart.html')


@login_required
@app.route('/product1')
def product1():
    d = datetime.strptime('2022.12.08', "%Y.%m.%d")
    end_date = d - datetime.now()
    return render_template ('product1.html', action_name = 'Новогодние скидки!', end_date=end_date)


@login_required
@app.route('/product2')
def product2():
    d = datetime.strptime('2022.12.08', "%Y.%m.%d")
    end_date = d - datetime.now()
    return render_template ('product2.html', end_date=end_date)


@login_required
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


@login_required
@app.route('/order_list')
def order_list():
    return render_template ('order_list.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = 'admin'
    password = 'admin'
    if request.method == 'POST':
        if request.form['login'] == login and request.form['password'] == password:
            return redirect(url_for('index'))
            login_user(User(login))
        else:
            return render_template ('login.html', error='Неправильный логин или пароль')
    return render_template ('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Пока'

if __name__ == '__main__':
    app.run()