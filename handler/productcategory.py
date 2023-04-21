from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import db_session
from admin import admin_required
from model.productcategory import ProductCategory

blueprint = Blueprint('productcategory', __name__)


class PostProductCategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@blueprint.route('/productcategory_add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = PostProductCategoryForm()

    if form.validate_on_submit():
        with db_session.create_session() as session:
            product_category = ProductCategory(
                name=request.form.get('name'),
                description=request.form.get('description'),
            )
            session.add(product_category)
            session.commit()
            return redirect(url_for('productcategory.get'))

    return render_template('productcategories_add.html', form=form)


@blueprint.route('/productcategories', methods=['GET'])
@login_required
@admin_required
def get():
    return render_template('productcategories.html')


@blueprint.route('/productcategories_del/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    try:
        with db_session.create_session() as session:
            session.query(ProductCategory).filter(ProductCategory.id == id).delete()
            session.commit()
    except IntegrityError:
        flash("Невозможно удалить категорию, если есть товары данной категории!")

    return redirect(url_for('productcategory.get'))
