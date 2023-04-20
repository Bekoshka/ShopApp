from flask import request, render_template, Blueprint
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SubmitField

import db_session
from model.user import User

blueprint = Blueprint('profile', __name__)


class ProfileForm(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль')
    fname = StringField('Имя')
    lname = StringField('Фамилия')
    phone = StringField('Телефон')
    email = EmailField('Email')
    address = TextAreaField('Адрес')
    submit = SubmitField('Сохранить')


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
