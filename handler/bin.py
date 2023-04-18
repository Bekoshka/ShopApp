from flask import Blueprint, render_template

blueprint = Blueprint('bin', __name__)


@blueprint.route('/bin')
def bin():
    return render_template('bin.html')
