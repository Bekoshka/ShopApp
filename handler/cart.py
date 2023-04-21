from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired

import db_session
from model.cartitem import CartItem
from model.order import OrderStatus, Order
from model.orderitem import OrderItem
from model.product import Product

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
        if not cart_items:
            return redirect(url_for('cart.get'))
        sum = 0
        order = Order(
            user_id=current_user.id,
            address=current_user.address,
            phone=current_user.phone,
            email=current_user.email,
            status=OrderStatus.new,
            sum=0
        )
        session.add(order)
        session.flush()
        session.refresh(order)
        for ci in cart_items:
            product = session.query(Product).filter(Product.id == ci.product_id).with_for_update().one()
            if product.quantity - ci.quantity < 0:
                flash("Не достаточно товара в наличии: " + product.name)
                session.rollback()
                cart_items = session.query(CartItem).filter(CartItem.user_id == current_user.id)
                return render_template('cart.html', cart_items=cart_items)
            product.quantity -= ci.quantity
            oi_sum = ci.quantity * product.price
            sum += oi_sum
            order_item = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                sum=oi_sum
            )
            session.add(product)
            session.add(order_item)
            session.delete(ci)
        order.sum = sum
        session.add(order)
        session.commit()
    return redirect(url_for('order.get'))
