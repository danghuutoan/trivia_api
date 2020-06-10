# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

-   [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

-   [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

-   [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Error handling

Errors are returned as JSON objects in the following format

```
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

The API will return three types of error when requests fail

-   404 : Not found
-   422 : Unprocessable
-   400 : Bad request

## Endpoints

### GET /categories

-   General

    -   Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    -   Request Arguments: None
    -   Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

        ```json
        {
        	"categories": {
        		"1": "Science",
        		"2": "Art",
        		"3": "Geography",
        		"4": "History",
        		"5": "Entertainment",
        		"6": "Sports",
        		"7": "new_type",
        		"8": "new_type",
        		"9": "new_type",
        		"10": "new_type",
        		"11": "new_type"
        	},
        	"success": true
        }
        ```

    -   Test comand:
        ```
        curl http://127.0.0.1:5000/categories -X GET
        ```

### POST /categories

-   General:
    -   Create a new category with the given type
    -   Curl command
        ```bash
        curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type": "new_type"}'
        ```
    -   Return: An object similar to the on below
        ```json
        {
        	"category": {
        		"id": 11,
        		"type": "new_type"
        	},
        	"success": true
        }
        ```

### DELETE /categories/\<int:category_id\>

-   General:
    -   Delete a category with the given category id
-   Curl:
    ```
    curl http://127.0.0.1:5000/categories/12 -X DELETE
    ```
-   Response sample
    ```
    {
        "category":
        {
            "id": 12,
            "type": "new_type"
        },
        "success": true
    }
    ```

### PATCH /categories/\<int:category_id\>

-   General:

    -   Partly update a category with the given id

-   Curl:
    ```
    curl http://127.0.0.1:5000/categories/8 -X PATCH -H "Content-Type: application/json" -d '{"type": "new_type1"}'
    ```
-   Sample response
    ```
    {
        "category": {
            "id": 8,
            "type": "new_type1"
        },
        "success": true
    }
    ```

### GET /questions?page=\<page_number\>

-   General:
    -   Get paginated result of the available questions
-   Test
    ```
    curl 'http://127.0.0.1:5000/questions?page=1'
    ```
-   Sample response

    ```
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports",
        "8": "new_type1",
        "9": "new_type",
        "10": "new_type",
        "11": "new_type"
    },
    "questions": [
        {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
        },
        {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "total_questions": 13
    }

    ```

### POST /questions

-   General: create a new question
-   Test command:
    ```
    curl 'http://127.0.0.1:5000/questions' -X POST -H "Content-Type: application/json" -d '{"question":"question", "answer": "answer", "category": 1, "difficulty": 1}'
    ```
-   sample response:
    ```
    {
        "question": {
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "question"
        },
        "success": true
    }
    ```

### DELETE /questions/\<question_id\>

-   General: Delete a question with a given id
-   Test command:
    ```
    curl 'http://127.0.0.1:5000/questions/1 -X DELETE'
    ```
-   Sample response:
    ```
    {
        "question": {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        "success": true
    }
    ```

### PUT /questions/\<int:question_id\>

-   General: update a question
-   Test command:
    ```
    curl 'http://127.0.0.1:5000/questions/1' -X PUT -H "Content-Type: application/json" -d '{"question":"question", "answer": "answer", "category": 1, "difficulty": 1}'
    ```
-   sample response:
    ```JSON
    {
        "question": {
            "answer": "answer2",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "question"
        },
        "success": true
    }
    ```

### GET /categories/\<int:category_id\>/questions

-   General: get questions by category
-   Test command:
    ```
    curl http://127.0.0.1:5000/categories/1/questions
    ```
-   Sample response:
    ```
    {
        "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
            "id": 26,
            "question": "question"
        },
        {
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
            "id": 27,
            "question": "question"
        },
        {
            "answer": "answer",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": "question"
        },
        {
            "answer": "answer1",
            "category": 1,
            "difficulty": 1,
            "id": 29,
            "question": "question"
        },
        {
            "answer": "answer2",
            "category": 1,
            "difficulty": 1,
            "id": 30,
            "question": "question"
        },
        {
            "answer": "answer2",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "question"
        }
        ],
        "success": true
    }
    ```

### POST /questions/search

-   General: get questions based on a search term.
-   Test command:

    ```
    curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"penicillin"}'
    ```

-   Sample response:
    ```
    {
        "questions": [
            {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
            }
        ],
        "success": true
    }
    ```

### POST /quizzes

-   General:
    -   get questions to play the quiz.
    -   take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
-   Test command
    ```
    curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[21], "quiz_category": {"type": "invalid", "id": "1"}}'
    ```
-   sample response
    ```
    {
        "question": {
        "answer": "answer1",
        "category": 1,
        "difficulty": 1,
        "id": 29,
        "question": "question"
        },
        "success": true
    }
    ```
