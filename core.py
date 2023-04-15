from flask import Flask
from flask_login import LoginManager

import db_session
from handler import auth, main
from model.user import User

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(auth.blueprint)
app.register_blueprint(main.blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_session.create_session().query(User).get(user_id)
