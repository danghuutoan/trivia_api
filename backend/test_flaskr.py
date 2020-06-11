import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'test question',
            'answer': "test answer",
            'category': 1,
            'difficulty': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions_valid_page(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_404_sent_if_get_paginated_questions_invalid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': "What boxer's "})

        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['questions'][0]['id'], 9)

    def test_get_question_by_valid_category(self):
        res = self.client().get('/categories/2/questions')

        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['questions'][0]['category'], 2)

    def test_get_question_by_invalid_category(self):
        res = self.client().get('/categories/100/question')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_valid_question(self):
        deleted_question = Question.query.first()
        res = self.client().delete('/questions/' + str(deleted_question.id))

        data = json.loads(res.data)
        question = Question.query.filter(
            Question.id == deleted_question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data['question']['id'], deleted_question.id)

    def test_404_sent_if_delele_invalid_question(self):
        res = self.client().delete('/questions/100')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_delete_category(self):
        deleted_category = Category.query.first()
        res = self.client().delete('/categories/' + str(deleted_category.id))

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        checked_category = Category.query.filter(
            Category.id == deleted_category.id).one_or_none()

        self.assertEqual(checked_category, None)

    def test_404_sent_if_delete_invalid_category(self):
        res = self.client().delete('/categories/100')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_create_category(self):
        res = self.client().post('/categories', json={"type": "new type"})
        data = json.loads(res.data)
        category_id = data['category']['id']
        category = Category.query.get(category_id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(category)

    def test_play_quiz_valid_category(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [21], 'quiz_category': {'type': 'Science', 'id': '2'}})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)
        self.assertNotEqual(data['question']['id'], 21)

    def test_play_quiz_invalid_category(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [21], 'quiz_category': {'type': 'invalid', 'id': '25'}})

        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
