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


@app.route('/movies', methods=['GET'])
def movies():
    result = Movie.query.all()
    all_movies = [mov.format() for mov in result]
    return jsonify({
        "success": True,
        "movies": all_movies,
        "total movies": len(result)
    })


@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_data()
    print(body)
    if not body:
        abort(400)
    else:
        title = body.get('title')
        release_date = body.get('release_date')
        description = body.get('description')
        try:
            new_movie = Movie(
                title=title, release_date=release_date, description=description)
            new_movie.insert()

            added_movie = new_movie.format()
            return json({
                'success': True,
                'added movie': added_movie
            })
        except:
            abort(422)


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    result = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if not result:
        abort(400)
    else:
        data = [result.format()]
        return jsonify({
            'success': True,
            'movie data': data
        })


@app.route('/movies/<int:movie_id>/actors', methods=['GET'])
def get_actors_by_movie_id(movie_id):
    result = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if not result:
        abort(400)
    else:
        data = [act.format() for act in result.actors]
        return jsonify({
            "success": True,
            "actors": data
        })


@app.route('/actors', methods=['GET'])
def actors():
    result = Actor.query.all()
    all_actors = [act.format() for act in result]
    return jsonify({
        "success": True,
        "movies": all_actors,
        "total actors": len(result)
    })


@app.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    result = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if not result:
        abort(400)
    else:
        data = [result.format()]
        return jsonify({
            'success': True,
            'actor data': data
        })

    # return app


# app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
