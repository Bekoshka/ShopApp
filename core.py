from flask import Flask, render_template, request, redirect

from templates.loginform import LoginForm

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
@app.route('/index')
def index():
    user = "Пользователь 1"
    return render_template('index.html', title='Домашняя страница',
                           username=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('register.html', title='Регистрация', form=form)

