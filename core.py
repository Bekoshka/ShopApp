from flask import Flask
from flask_login import LoginManager

import db_session
from handler import auth, main, productcategory, product, cart, order
from handler.cart import PostCartForm
from model.user import User, ProductCategory

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(auth.blueprint)
app.register_blueprint(main.blueprint)
app.register_blueprint(product.blueprint)
app.register_blueprint(productcategory.blueprint)
app.register_blueprint(cart.blueprint)
app.register_blueprint(order.blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.create_session().query(User).get(user_id)


@app.context_processor
def context_processor():
    with db_session.create_session() as session:
        return dict(global_product_categories=session.query(ProductCategory), global_add_to_cart=PostCartForm())