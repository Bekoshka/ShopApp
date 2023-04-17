from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo

import db_session
from model.user import User, Product

blueprint = Blueprint('product', __name__)


class PostProductForm(FlaskForm):
    product_category_id = StringField('Категория', validators=[DataRequired()])
    image = FileField("Изображение", validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    quantity = StringField('Цена', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@blueprint.route('/product_add', methods=['GET', 'POST'])
@login_required
def add():
    form = PostProductForm()

    if form.validate_on_submit():
        with db_session.create_session() as session:
            product = Product(
                product_category_id=request.form.get('product_category_id'),
                image=request.form.get('image'),
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=request.form.get('price'),
                quantity=request.form.get('quantity')
            )
            session.add(product)
            session.commit()
            return redirect(url_for('product.get'))

    return render_template('products_add.html', form=form)


@blueprint.route('/products', methods=['GET'])
@login_required
def get():
    with db_session.create_session() as session:
        ps = session.query(Product)
        return render_template('products.html', pcs=ps)