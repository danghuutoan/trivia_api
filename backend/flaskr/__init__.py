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
        try:
            categories = Category.query.all()
            categories_list = {}
            for category in categories:
                categories_list.update({category.id: category.type})
            return jsonify({
                "success": True,
                "categories": categories_list}
            )
        except:
            abort(422)

    @app.route('/categories', methods=['POST'])
    def create_category():
        request_json = request.get_json()
        app.logger.debug(request_json)
        if 'type' in request_json:
            try:
                category = Category(request_json['type'])
                category.insert()
            except:
                abort(422)
            return jsonify({
                'success': True,
                'category': category.format()
            })
        else:
            abort(400)

    @app.route('/categories/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if category:
            category.delete()
            return jsonify({
                'success': True,
                'category': category.format()
            })
        else:
            abort(404)

    @app.route('/categories/<int:category_id>', methods=['PATCH'])
    def update_category(category_id):
        request_json = request.get_json()
        if "type" in request_json:
            try:
                category = Category.query.filter(
                    Category.id == category_id).one_or_none()
                if category:
                    category.type = request_json['type']
                    category.update()
                    return jsonify({
                        'success': True,
                        'category': category.format()
                    })
                else:
                    abort(404)

            except:
                abort(422)
        else:
            abort(400)

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
        try:
            question = Question.query.get(question_id)
        except:
            abort(422)

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
        try:
            question = Question(request_json['question'], request_json['answer'],
                                request_json['category'], request_json['difficulty'])
            question.insert()
        except:
            abort(422)

        return jsonify({
            "success": True,
            "question": question.format()
        })

    @app.route('/questions/<int:question_id>', methods=['PUT'])
    def update_question(question_id):
        error = False
        request_json = request.get_json()

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
        except:
            abort(422)

        if question:
            question.question = request_json['question']
            question.answer = request_json['answer']
            question.category = request_json['category']
            question.difficulty = request_json['difficulty']
            try:
                question.update()
            except:
                abort(422)
        else:
            try:
                question = Question(request_json['question'], request_json['answer'],
                                    request_json['category'], request_json['difficulty'])
                question.id = question_id
                question.insert()
            except:
                abort(422)
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
        try:
            questions = Question.query.filter(Question.category == category_id)
            question_list = []
            for question in questions:
                question_list.append(question.format())
            return jsonify({
                "success": True,
                "questions": question_list
            })
        except:
            abort(422)
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
        category_id = request_json['quiz_category']['id']
        previous_questions = request_json['previous_questions']

        if category_id == 0:
            try:
                questions = Question.query.filter(
                    Question.category.notin_(previous_questions)).all()
            except:
                abort(422)
        else:
            try:
                category = Category.query.get(category_id)
            except:
                abort(422)

            if category == None:
                abort(404)
            else:
                try:
                    questions = Question.query.filter(Question.category.notin_(previous_questions),
                                                      Question.category == category_id).all()
                except:
                    abort(422)

        questions_num = len(questions)

        if questions_num:
            question_id = random.randint(1, questions_num)
            return jsonify({
                "success": True,
                "question": questions[question_id - 1].format()
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

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
    return app
