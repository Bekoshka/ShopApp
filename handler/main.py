from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

import db_session
from config import UPLOAD_FOLDER
from model.user import User

blueprint = Blueprint('main', __name__)


# @blueprint.route('/')
# def index():
#     return render_template('index.html')


class ProfileForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль')
    fname = StringField('Имя')
    lname = StringField('Фамилия')
    phone = StringField('Телефон')
    email = EmailField('Email')
    address = TextAreaField('Адрес')
    submit = SubmitField('Сохранить')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Станый пароль', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_confirm = PasswordField('Повторите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message="Пароль должен совпадать")])
    submit = SubmitField('Изменить')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    if form.validate_on_submit():
        with db_session.create_session() as db:
            user = db.query(User).filter_by(login=current_user.login).first()
            if request.form.get('fname'):
                user.fname = request.form.get('fname')
            if request.form.get('lname'):
                user.lname = request.form.get('lname')
            if request.form.get('sex'):
                user.sex = request.form.get('sex') == 'm'
            if request.form.get('phone'):
                user.phone = request.form.get('phone')
            if request.form.get('email'):
                user.email = request.form.get('email')
            if request.form.get('address'):
                user.address = request.form.get('address')
            db.add(user)
            db.commit()
            return render_template('profile.html', user=user, form=form)

    with db_session.create_session() as session:
        user = session.query(User).filter_by(login=current_user.login).first()
    return render_template('profile.html', user=user, form=form)


@blueprint.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        with db_session.create_session() as db:
            user = db.query(User).filter_by(login=current_user.login).first()
            if not request.form.get('password') or not user or user.password != request.form.get('old_password'):
                flash(f"Проверьте правильность пароля")
            else:
                user.password = request.form.get('password')
                db.add(user)
                db.commit()
    with db_session.create_session() as session:
        user = session.query(User).filter_by(login=current_user.login).first()
    return render_template('change_password.html', user=user, form=form)


@blueprint.route('/uploads/<name>', methods=['GET'])
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)