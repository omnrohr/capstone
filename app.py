import os
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
import json

from models import Movie, Actor, setup_db, db_drop_and_create_all, insert_demo_data
# from auth import AuthError, requires_auth


# def create_app(test_config=None):
app = Flask(__name__)
setup_db(app)

app.config.from_object('config')

db_drop_and_create_all()
insert_demo_data()


@app.route('/')
def home():
    return render_template("index.html", data=['name', 'hello'])


@app.route('/<name>')
def user_page(name='user'):
    return render_template("index.html", data=[name, 2, 3])


@app.route('/admin')
def admin():
    return redirect(url_for("user_page", name="Admin"))


@app.route('/page')
def page():
    return('hello! page')

    # return app


# app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
