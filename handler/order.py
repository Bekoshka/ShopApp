from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired

import db_session
from admin import admin_required
from model.order import Order, OrderStatus
from model.orderitem import OrderItem

blueprint = Blueprint('order', __name__)


class PostOrderStatusForm(FlaskForm):
    order_id = HiddenField()
    status = StringField('Статус', validators=[DataRequired()])
    submit = SubmitField('Изменить')


@blueprint.route('/orders', methods=['GET'])
@login_required
def get():
    with db_session.create_session() as session:
        orders = session.query(Order).filter(Order.user_id == current_user.id).order_by(Order.time.desc())
        return render_template('orders.html', orders=orders)


@blueprint.route('/orders/<int:id>', methods=['GET'])
@login_required
def details(id):
    with db_session.create_session() as session:
        order_items = session.query(OrderItem).filter(OrderItem.order_id == id)
        order = session.query(Order).filter(Order.id == id).one()
        return render_template('order_items.html', order_items=order_items, order=order)


@blueprint.route('/orders_admin', methods=['GET'])
@login_required
@admin_required
def get_admin():
    with db_session.create_session() as session:
        orders = session.query(Order).order_by(Order.time.desc())
        return render_template('orders_admin.html', orders=orders, form=PostOrderStatusForm())


@blueprint.route('/orders_status', methods=['POST'])
@login_required
@admin_required
def status():
    form = PostOrderStatusForm()

    if form.validate_on_submit():
        with db_session.create_session() as db:
            id = request.form.get('order_id')
            status = request.form.get('status')
            order = db.query(Order).filter(Order.id == id).one()
            order.status = OrderStatus(int(status))
            db.add(order)
            db.commit()
    with db_session.create_session() as session:
        orders = session.query(Order).order_by(Order.time.desc())
    return render_template('orders_admin.html', orders=orders, form=form)
