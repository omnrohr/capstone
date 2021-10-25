import os
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Movie, Actor, setup_db, db_drop_and_create_all, insert_demo_data, db
from auth import AuthError, requires_auth
from secrets import *


def create_app():
    app = Flask(__name__)
    setup_db(app)
    app.secret_key = "secret key"
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object('config')

    db_drop_and_create_all()
    insert_demo_data()

    @app.route('/')
    def home():
        return render_template("index.html", data=['name', 'hello'])

    @app.route('/movies', methods=['GET'])
    @requires_auth('read:all_data')
    def get_movies(payload):
        result = Movie.query.all()
        all_movies = [mov.format() for mov in result]
        return jsonify({
            "success": True,
            "movies": all_movies,
            "total movies": len(result)
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('edit:all_data')
    def add_movie(payload):
        body = request.get_json()
        print(body)
        if not body:
            abort(400)

        title = body.get('title')
        release_date = body.get('release_date')
        description = body.get('description')
        print(title)
        if not title:
            abort(400)
        try:
            new_movie = Movie(
                title=title, release_date=release_date, description=description)
            new_movie.insert()
            print("suceess")
            added_movie = new_movie.format()
            print(added_movie)

        except:
            db.session.rollback()
            abort(422)
        return jsonify({
            'success': True,
            'added movie': added_movie
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:all_data')
    def update_movies(payload, movie_id):
        body = request.get_json()
        print(body)
        result = Movie.query.filter(Movie.id == movie_id).one_or_none()
        print(result)
        if not result:
            abort(404)

        try:
            title = body.get('title')
            release_date = body.get('release_date')
            description = body.get('description')
            print(title)

            if title:
                result.title = title

            if description:
                result.description = description

            if release_date:
                result.release_date = release_date

            result.update()
        except BaseException:
            db.session.rollback()
            abort(400)

        return jsonify({'success': True, 'Movies': [result.format()]}), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('edit:all_data')
    def delete_movies(payload, movie_id):
        result = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not result:
            abort(404)

        try:
            result.delete()
        except BaseException:
            db.session.rollback()
            abort(400)

        return jsonify({'success': True, 'delete': movie_id}), 200

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('read:all_data')
    def get_movie_by_id(payload, movie_id):
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
    @requires_auth('read:all_data')
    def get_actors_by_movie_id(payload, movie_id):
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
    @requires_auth('read:all_data')
    def get_actors(payload):
        result = Actor.query.all()
        all_actors = [act.format() for act in result]
        return jsonify({
            "success": True,
            "actors": all_actors,
            "total actors": len(result)
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:all_data')
    def patch_actors(payload, actor_id):
        body = request.get_json()
        if not body:
            abort(400)

        result = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if result is None:
            abort(404)
        try:
            if 'name' in body:
                result.name = body.get('name')
            data = [result.format()]
            return jsonify({
                'success': True,
                'actors': data
            })

        except:
            db.session.rollback()
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('read:all_data')
    def get_actor_by_id(payload, actor_id):
        result = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not result:
            abort(400)
        else:
            data = [result.format()]
            return jsonify({
                'success': True,
                'actor data': data
            })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('edit:all_data')
    def delete_actors(payload, actor_id):
        result = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if result is None:
            abort(404)
        try:
            data = [result.format()]
            result.delete()
            return jsonify({
                'success': True,
                'deleted': data
            })

        except:
            db.session.rollback()
            abort(400)

    #----------------------------------------------------------------------------#
    # ERRORS.
    #----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error["code"],
        }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
