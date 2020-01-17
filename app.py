import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from  models import setup_db, Actor, Movie
from  auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


## ROUTES

@app.route('/')
def hi():
    return "Hi!, this is only being used as a backeend API"

@app.route('/actors')
# creates the actors endpoint
def get_actors():
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]

        if len(formatted_actors) == 0:
            abort(404)
        # display results
        return jsonify({
        'success':True,
        'actors': formatted_actors
            })

@app.route('/movies')
# creates the movies endpoint
def get_movies():
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]

        if len(formatted_movies) == 0:
            abort(404)
        
        # display results
        return jsonify({
        'success':True,
        'movies': formatted_movies
            })

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
# creates the delete movies endpoint
def delete_movie(self, movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        # display results
        return jsonify({
        'success':True,
        'deleted': movie_id
            })
        
    except:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
# creates the delete actors endpoint
def delete_actor(self, actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()

        # display results
        return jsonify({
        'success':True,
        'deleted': actor_id
            })
        
    except:
        abort(422)

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def movies_patch(self, movie_id):
    body = request.get_json()
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        if 'title' in body:
            movie.title = body.get('title')
        if 'release_date' in body:
            movie.release_date = body.get('release_date')

        movie.update()

        return jsonify({
            "success": True
        })
    except:
        abort(422)

@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def actors_patch(self, actor_id):
    body = request.get_json()
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        if 'name' in body:
            actor.name = body.get('name')
        if 'age' in body:
            actor.age = body.get('age')
        if 'gender' in body:
            actor.gender = body.get('gender')

        actor.update()

        return jsonify({
            "success": True
        })
    except:
        abort(422)

@app.route('/movies_new', methods=['POST'])
@requires_auth('post:movies')
# create a new movie endpoint
def new_movie(self):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
        movie = Movie(title=new_title, release_date=new_release_date)
        movie.insert()

        # display results
        return jsonify({
        'success':True,
        'movie': movie.id
            }) 
    except:
        abort(422)

@app.route('/actors_new', methods=['POST'])
@requires_auth('post:actors')
# create a new actor endpoint
def new_actor(self):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    try:
        actor = Actor(name=new_name, age=new_age, gender=new_gender)
        actor.insert()

        # display results
        return jsonify({
        'success':True,
        'movie': actor.id
            }) 
    except:
        abort(422)

    # @app.route('/questions', methods=['POST'])
    # # search on questions with partial string search. Case-insensitive.
    # def search_questions():
    #     data = request.get_json()
    #     tag = data['searchTerm']
    #     search = "%{}%".format(tag)
    #     questions = Question.query.filter(Question.question.ilike(search)).order_by('id').all()
    #     formatted_questions = [question.format() for question in questions]
        
    #     if len(formatted_questions) == 0:
    #         abort(404)

    #     # display results
    #     return jsonify({
    #     'success':True,
    #     'questions': formatted_questions
    #         })

    # @app.route('/categories/<int:category_id>/questions')
    # # creates the sidebar in the list page endpoint
    # def get_specific_category(category_id):
    #         questions = Question.query.filter(Question.category == category_id).order_by('id').all()
    #         formatted_questions = [question.format() for question in questions]
    #         categories = Category.query.all()
    #         formatted_categories = [category.format() for category in categories]

    #         if len(formatted_questions) == 0:
    #             abort(404)

    #         if len(formatted_categories) == 0:
    #             abort(404)

    #         # display results
    #         return jsonify({
    #         'success':True,
    #         'questions': formatted_questions,
    #         'categories': formatted_categories,
    #         'total_questions': len(formatted_questions)
    #             })

    @app.route('/coolkids')
    def be_cool():
        return "Be cool Yony, be coooool! You're almost a FSND grad!"

#     return app

# app = create_app()

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=True)