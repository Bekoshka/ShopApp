import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField, FileField, \
    HiddenField
from wtforms.validators import DataRequired, EqualTo

import db_session
from model.user import Product, CartItem, OrderItem, Order

blueprint = Blueprint('order', __name__)


@blueprint.route('/orders', methods=['GET'])
@login_required
def get():
    with db_session.create_session() as session:
        orders = session.query(Order).filter(Order.user_id == current_user.id)
        return render_template('orders.html', orders=orders)


@blueprint.route('/orders/<int:id>', methods=['GET'])
@login_required
def details(id):
    with db_session.create_session() as session:
        order_items = session.query(OrderItem).filter(OrderItem.order_id == id)
        order = session.query(Order).filter(Order.id == id).one()
        return render_template('order_items.html', order_items=order_items, order=order)
