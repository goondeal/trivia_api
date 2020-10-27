# Full Stack Trivia API Backend

## Intoduction

Udacity is investing in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where this API project comes in! Trivia API helps them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch.

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

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Base URL
Till now, the API is hosted localy with a default port = 5000.
So, the base url is http://localhost:5000

### API Keys/Authentication
Niether keys nor Authentication permissions are needed for using this API. It's allready ready for usage.

## Errors
All error responses are formatted as json with almost the same keys and values differ upon the error message and status code.

For more info, See the error handelers which are decorated by "@app.errorhandler()" at the end of "flasker/__init__.py" file. 

### 404 - Not Found Error
Raised if a page or a search result was not found.
### 400 - Bad Request Error
Raised in case of POST requests if the request body is not supplied.
### 422 - Unprocessable Error
### 500 - Internal Server Error


## Resource Endpoint Library

### Endpoints
GET '/questions'
GET '/categories'
DELETE '/questions/<int: id>'
POST '/questions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

#### GET '/questions'
- Handles GET requests for questions, including pagination (every 10 questions), with a default page number = 1 . 
- Request Arguments: <int: page>
- Returns a list of questions, number of total questions, current category, categories.

- For example 'http://localhost:5000/questions?page=2' returns the second 10 questions as follows: 
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    .
    .
    .
  ],
  "success": true,
  "total_questions": 19
}
```

- If the requested page is beyond the scope and doesn't have questions, a not found error will be raised. For example, a GET request to 'http://localhost:5000/questions?page=9999' will get a response like that with a status code 404: 
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

### GET '/categories'
- Handle GET requests for all available categories.
This endpoint should return a dictionary of categories as key-value pairs of ids and types, number of total categories. Sample response as follows: 
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```
- Returns 404 error if no categories are exists.

### DELETE '/questions/<int: id>'
- Delete a particular question with this id from the database.
- Sending a DELETE request to 'http://localhost:5000/questions/9' , returns a json response with 200 status code if the request succeded as follows:
```
{
  "deleted": 9,
  "message": "Question was deleted successfuly",
  "success": true
}
```
OR, a 404 error if there is no question with this id, For example, Sending the same request 'http://localhost:5000/questions/9' will return an error response as follows beause the question was allready deleted and so, it doesn't exist in the database any more. 
```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

### POST '/questions'
- This Endpoint is responsable for 2 functions: creating a new Question, OR Searching for questions with a specific text. 
- The applied function depends on the request body as follows:  

#### Create a question
- Creates a new question, which will require the question and answer text, category, and difficulty score as json.
- For example a POST request to 'http://localhost:5000/questions' with body
```
{
"question": "Where are the Pyramids",
"answer": "Egypt",
"difficulty": 1,
"category": 3
}
```
returns a response:
```
{
'success': true,
'created': 27,
'questions': [...],
'total_questions': 27,
'current_category': null,
}
```
- If no request body was supplied a (400 - Bad Request) response will be returned.

#### Search for questions
- Get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
- For example a POST request to 'http://localhost:5000/questions' with body
```
{"searchTerm": "Where"}
```
returns a response:
```
{
   "current_category":3,
   "questions":[
      {
         "answer":"Egypt",
         "category":3,
         "difficulty":1,
         "id":24,
         "question":"Where are the pyramids ?"
      }
   ],
   "success":True,
   "total_questions":44
}
```
- If no request body was supplied a (400 - Bad Request) response will be returned.
- If no results found a (404 - Not Found Error) response will be returned.


### GET '/categories/<int:category_id>/questions'
- Get questions based on category.
- Request Arguments: <int:category_id> the id of the category.
- For example a request to 'http://localhost:5000/categories/3/questions' will return:

```
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```
- If no questions in this category a (404 - Not Found Error) response will be returned.

### POST '/quizzes'
- Get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

- Request Body: json like 
```
{
'previous_questions': [],
'quiz_category': {'id':1, 'type': 'Science'}
}
```
if no "quiz_category" value supplied or was empty the returned question will be from any category type.

- For example a POST request to 'http://localhost:5000/quizzes' with body
```
{
   "previous_questions":[1, 2, 3],
   "quiz_category":{
      "type":"History",
      "id":4
   }
}
```

 may return:
 ```
 {
   "success": true,
   "question":{
      "answer":"Scarab",
      "category":4,
      "difficulty":4,
      "id":23,
      "question":"Which dung beetle was worshipped by the ancient Egyptians?"
   }
}
 ```
- If no questions remained, the response will be 
```
{'success': True, 'question': null}
```
and the game will be ended for the user in the frontend. 

 - If no request body was supplied a (400 - Bad Request) response will be returned.


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```