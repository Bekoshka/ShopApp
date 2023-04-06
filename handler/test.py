import db_session
from model.user import User
from flask import request, Response, jsonify, make_response
from core import app


@app.post('/test')
def test():
    return \
        f"""
        <head>
        <h1>Миссия Колонизация Марса</h1></br>
        <img src="https://kartinkin.net/uploads/posts/2022-12/thumbs/1670342973_36-kartinkin-net-p-krasivie-kartinki-marsa-pinterest-40.jpg"
           alt="здесь должна была быть картинка, но не нашлась">
        <br>Вот она какая красная планета
        <title>Привет, Марс!</title>
        <head>
        """


