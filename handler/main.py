from flask import Blueprint, send_from_directory
from config import UPLOAD_FOLDER

blueprint = Blueprint('main', __name__)


@blueprint.route('/uploads/<name>', methods=['GET'])
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)
