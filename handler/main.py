from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

import db_session
from config import UPLOAD_FOLDER
from model.user import User

blueprint = Blueprint('main', __name__)


@blueprint.route('/uploads/<name>', methods=['GET'])
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)