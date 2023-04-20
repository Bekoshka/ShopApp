from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo

import db_session
from model.user import ProductCategory

blueprint = Blueprint('productcategory', __name__)


class PostProductCategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@blueprint.route('/productcategory_add', methods=['GET', 'POST'])
@login_required
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
def get():
    return render_template('productcategories.html')


@blueprint.route('/productcategories_del/<int:id>', methods=['POST'])
@login_required
def delete(id):
    with db_session.create_session() as session:
        session.query(ProductCategory).filter(ProductCategory.id == id).delete()
        session.commit()
        return redirect(url_for('productcategory.get'))