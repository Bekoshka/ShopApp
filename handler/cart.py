import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField, FileField, \
    HiddenField
from wtforms.validators import DataRequired, EqualTo

import db_session
from model.user import Product, CartItem, Order, OrderItem, OrderStatus

blueprint = Blueprint('cart', __name__)


class PostCartForm(FlaskForm):
    product_id = HiddenField()
    quantity = StringField('Количество', validators=[DataRequired()])
    submit = SubmitField('В корзину')


@blueprint.route('/cart_add', methods=['POST'])
@login_required
def add():
    form = PostCartForm()

    if form.validate_on_submit():
        with db_session.create_session() as session:
            product_id = request.form.get('product_id')
            quantity = request.form.get('quantity')
            cart_item = session.query(CartItem).filter(CartItem.user_id == current_user.id,
                                                       CartItem.product_id == product_id).with_for_update().one_or_none()
            if cart_item:
                cart_item.quantity += int(quantity)
            else:
                cart_item = CartItem(
                    user_id=current_user.id,
                    product_id=product_id,
                    quantity=quantity,
                )
            session.add(cart_item)
            session.commit()
    return redirect(url_for('cart.get'))


@blueprint.route('/cart', methods=['GET'])
@login_required
def get():
    with db_session.create_session() as session:
        cart_items = session.query(CartItem).filter(CartItem.user_id == current_user.id)
        return render_template('cart.html', cart_items=cart_items)


@blueprint.route('/cart_del/<int:id>', methods=['POST'])
@login_required
def delete(id):
    with db_session.create_session() as session:
        session.query(CartItem).filter(CartItem.id == id).delete()
        session.commit()
        return redirect(url_for('cart.get'))


@blueprint.route('/submit', methods=['POST'])
@login_required
def submit():
    with db_session.create_session() as session:
        cart_items = session.query(CartItem).filter(CartItem.user_id == current_user.id).with_for_update().all()
        sum = 0
        order = Order(
            user_id=current_user.id,
            address=current_user.address,
            status=OrderStatus.new,
            sum=0
        )
        session.add(order)
        session.flush()
        session.refresh(order)
        for ci in cart_items:
            oi_sum = ci.quantity * ci.product.price
            sum += oi_sum
            order_item = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                sum=oi_sum
            )
            session.add(order_item)
            session.delete(ci)
        order.sum = sum
        session.add(order)
        session.commit()
    return redirect(url_for('order.get'))
