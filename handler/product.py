import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

import db_session
from config import UPLOAD_FOLDER

from model.product import Product
from admin import admin_required

blueprint = Blueprint('product', __name__)


class PostProductForm(FlaskForm):
    product_category_id = StringField('Категория', validators=[DataRequired()])
    image = FileField("Изображение", validators=[DataRequired()])
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    quantity = StringField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@blueprint.route('/product_add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = PostProductForm()

    if form.validate_on_submit():
        with db_session.create_session() as session:
            image = request.files['image']
            image_name = str(uuid.uuid4())
            product = Product(
                product_category_id=request.form.get('product_category_id'),
                image=image_name,
                name=request.form.get('name'),
                description=request.form.get('description'),
                price=request.form.get('price'),
                quantity=request.form.get('quantity')
            )
            session.add(product)
            session.commit()
            image.save(os.path.join(UPLOAD_FOLDER, image_name))
            return redirect(url_for('product.get'))

    return render_template('products_add.html', form=form)


@blueprint.route('/', methods=['GET'])
def get():
    with db_session.create_session() as session:
        if request.args.get('category'):
            category = request.args.get('category')
            products = session.query(Product).filter(Product.product_category_id == category)
        else:
            products = session.query(Product)
        return render_template('products.html', products=products)


@blueprint.route('/products_admin', methods=['GET'])
@login_required
@admin_required
def get_admin():
    with db_session.create_session() as session:
        products = session.query(Product)
        return render_template('products_admin.html', products=products)


@blueprint.route('/products_del/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    try:
        with db_session.create_session() as session:
            session.query(Product).filter(Product.id == id).delete()
            session.commit()
    except IntegrityError:
        flash("Невозможно удалить товар, если уже были покупки!")
    return redirect(url_for('product.get_admin'))
