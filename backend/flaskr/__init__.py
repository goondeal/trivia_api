import sys
sys.path.append('../')
from models import setup_db, Question, Category
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify, flash
import os
import random


# 1. Use Flask-CORS to enable cross-domain requests and set response headers. [Done]
# 2. Create an endpoint to handle GET requests for questions,
# including pagination (every 10 questions). This endpoint should
# return a list of questions, number of total questions, current category, categories. [Done]
# 3. Create an endpoint to handle GET requests for all available categories. [Done]
# 4. Create an endpoint to DELETE question using a question ID. [Done]
# 5. Create an endpoint to POST a new question, which will require the
# question and answer text, category, and difficulty score. [Done]
# 6. Create a POST endpoint to get questions based on category. [Done]
# 7. Create a POST endpoint to get questions based on a search term.
# It should return any questions for whom the search term is
# a substring of the question. [Done]
# 8. Create a POST endpoint to get questions to play the quiz.
# This endpoint should take category and previous question
# parameters and return a random questions within the given category,
# if provided, and that is not one of the previous questions. [Done]
# 9. Create error handlers for all expected errors including 400, 404, 422 and 500. [Done]


QUESTIONS_PER_PAGE = 10


# create and configure the app
app = Flask(__name__)
setup_db(app)


# Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    # select targeted questions.
    selected_questions = questions[start:end]
    # format selected questions.
    formated_questions = [question.format() for question in selected_questions]
    # returns a list of dictionaries.
    return formated_questions


'''
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
'''
@app.route('/questions')
def get_questions():
    # Get all questions.
    questions = Question.query.order_by(Question.id).all()
    # Get all categories.
    categories = Category.query.order_by(Category.id).all()
    # Select only the questions in the page range.
    selected_questions = paginate_questions(request, questions)

    if len(selected_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': selected_questions,  # list of dictionaries.
        'categories': {category.id: category.type for category in categories},
        'current_category': None,
        'total_questions': len(questions),
    })


# Create an endpoint to handle GET requests for all available categories.
@app.route('/categories')
def get_categories():
    # Get all categories.
    categories = Category.query.order_by(Category.id).all()
    # Abort "Not Found" error if there is no catedories.
    if len(categories) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories},
        'total_categories': len(categories),
    })


'''
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
'''


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    # Get the targeted question.
    question = Question.query.filter(
        Question.id == question_id).one_or_none()
    # Abort "Not Found Error" if not exists
    if question is None:
        abort(404)
    # Delete the question.
    question.delete()

    return jsonify({
        'success': True,
        'deleted': question_id,
        'message': 'Question was deleted successfuly',
    })


'''
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
'''
'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''

@app.route('/questions', methods=['POST'])
def create_question():
    # Get the body of the request as a json.
    body = request.get_json()
    # Abort bad request if no request body.
    if body is None:
        abort(400)
    # Get search term if exists.
    search = body.get('searchTerm', None)

    # with search term :
    if search:
        # get the matching questions.
        selection = Question.query.order_by(Question.id).filter(
            Question.question.ilike('%{}%'.format(search))).all()
        
        if len(selection) == 0:
          abort(404)    

        # Select only the questions in the page range.
        selected_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'questions': selected_questions,
            'total_questions': len(Question.query.all()),
            'current_category': None,
        })

    else:
        # Without search term (Create a new question) :
        # create question object properties (question, answer, category, difficulty).
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        # If the request body is empty.
        if question is None or answer is None or category is None or difficulty is None:
            abort(422)
        # Create a question object.
        new_question = Question(
            question=question, answer=answer, category=category, difficulty=difficulty)
        # Insert it into the Database.
        new_question.insert()

        # Get all questions and paginate them.
        selection = Question.query.order_by(Question.id).all()
        selected_questions = paginate_questions(request, selection)

        return jsonify({
            'success': True,
            'created': new_question.id,
            'questions': [new_question.format() for question in selected_questions],
            'total_questions': len(selection),
            'current_category': None,
        })


'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''


@app.route('/categories/<int:category_id>/questions')
def get_questions_by_category(category_id):
    # Get all questions in this category.
    questions = Question.query.filter(Question.category == category_id).all()
    # Abort "Not Found Error" if the category is empty.
    if len(questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'total_questions': len(Question.query.all()),
        'current_category': category_id,
    })


'''
@TODO: 
Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not. 
'''


@app.route('/quizzes', methods=['post'])
def new_quiz():
    # Get request body as a json.
    body = request.get_json()
    if body is None:
        abort(400)
    # Get body parameters.
    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', {})
    # Get all questions or Query questions by category if provided.  
    if quiz_category is None or quiz_category == {}:
        questions = Question.query.all()
    else:
        questions = Question.query.filter(
            Question.category == quiz_category['id']).all()

    # Exclude previous questions.
    questions_without_previous = list(
        filter(lambda question: question.id not in previous_questions, questions))
    # If questions remain, choose random one, else, return null and end the game.
    if len(questions_without_previous) > 0:
        random_question = random.choice(questions_without_previous)
        return(jsonify({
            'success': True,
            'question': random_question.format(),
        }))
    
    else:
        return(jsonify({
            'success': True,
            'question': None, # End the game in the front end.
        }))


# Create error handlers for all expected errors including 404 and 422.
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(500)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


if __name__ == "__main__":
    app.run()
