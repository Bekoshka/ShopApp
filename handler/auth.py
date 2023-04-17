from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError, StopValidation

import db_session
from model.user import User

blueprint = Blueprint('auth', __name__)


class SignUpForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_confirm = PasswordField('Повторите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message="Пароль должен совпадать")])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('запомнить')
    submit = SubmitField('Войти')



@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = request.form.get('login')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        with db_session.create_session() as session:
            user = session.query(User).filter_by(login=login).first()
            if not user or user.password != password:
                flash(f"Проверьте правильность логина и пароля")
                return render_template('login.html', form=form)

            login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    return render_template('login.html', form=form)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        login = request.form.get('login')
        password = request.form.get('password')
        with db_session.create_session() as session:
            user = session.query(User).filter_by(login=login).first()
            if user:
                flash(f"Логин {login} уже занят. Попробуйте другой")
                return render_template('signup.html', form=form)

            session.add(User(login=login, password=password))
            session.commit()
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))