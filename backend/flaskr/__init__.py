import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)
    cors = CORS(app, resources={
                r"/*": {"origins": "*"}})
    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,DELETE,OPTIONS')
        return response
    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.all()
        categories_list = {}
        for category in categories:
            categories_list.update({category.id: category.type})
        return jsonify({"categories": categories_list})

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
    def retrieve_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        categories = Category.query.all()
        categories_list = {}
        for category in categories:
            categories_list.update({category.id: category.type})

        data = []
        for question in questions:
            data.append(question.format())
        return jsonify({"questions": data[start:end],
                        "total_questions": len(data),
                        "categories": categories_list
                        })
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question == None:
            abort(404)
        else:
            question.delete()
            return jsonify({
                "success": True,
                "question": question.format()
            })

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
    def add_question():
        request_json = request.get_json()

        question = Question(request_json['question'], request_json['answer'],
                            request_json['category'], request_json['difficulty'])
        question.insert()

        return jsonify({
            "success": True,
            "question": question.format()
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
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = "%{}%".format(request.get_json()['searchTerm'])
        questions = Question.query.filter(
            Question.question.ilike(search_term)).all()
        question_list = []
        for question in questions:
            question_list.append(question.format())

        return jsonify({
            "success": True,
            "questions": question_list
        })
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):
        app.logger.info(category_id)
        questions = Question.query.filter(Question.category == category_id)
        question_list = []
        for question in questions:
            question_list.append(question.format())
        return jsonify({
            "success": True,
            "questions": question_list
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
    @app.route('/quizzes', methods=['POST'])
    def play_quizz():
        request_json = request.get_json()
        category = request_json['quiz_category']['id']
        previous_questions = request_json['previous_questions']

        if category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == category).all()

        filtered_questions = list(filter(lambda q: (
            q.id not in previous_questions), questions))
        questions_num = len(filtered_questions)
        if questions_num:
            question_id = random.randint(1, questions_num)
            app.logger.info(filtered_questions)
            # category_id = category
            return jsonify({
                "success": True,
                "question": filtered_questions[question_id - 1].format()
            })
        else:
            return jsonify({
                "success": True
            })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    return app
