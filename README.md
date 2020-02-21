# Rival App Backend

Rival App project is a website for people that are looking to upgrade their education through non-traditional channels such as Onleine/Offline Bootcamps, online courses, massive open online courses, online self study platforms etc. Users are able to search through the directory to find bootamps and courses, see detailed information about them such as course tuition and duration, upvote, and review them.

Rival App Backend is RESTful api for Rival App. It is deployed on Hereko server and can be reached with the following link:

[Rival App API](https://rivalapp.herokuapp.com/)

All backend code follows PEP8 style

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is recommended working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform using 'pipenv' package can be found in the [python docs](https://pipenv-fork.readthedocs.io/en/latest/)

#### PIP Dependencies

Install pipenv:

```bash
$ pip install --user pipenv
```

Install dependencies by naviging to the root directory of the project repository:

```bash
$ cd rival_backend
```

```bash
$ pip install -r requirements.txt
```

Next, activate the Pipenv shell:

```bash
$ pipenv shell
$ python --version
```

This will install all of the required packages we selected within the `Pipfile`.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [python-jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
$ FLASK_APP=app.py;
$ FLASK_ENV=development
```

To run the server, execute:

```bash
flask run
```

These commands put the application in development and directs our application to use the app.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.

Base URL: At present this app is hosted on Heroku server at https://rivalapp.herokuapp.com/. It can also be run locally. Locally, the backend app is hosted at the default, http://127.0.0.1:5000/.

Authentication: Application requires authentication to be able to carry out certain tasks.

## Roles and Permissions

Permissions:

- `add:bootcamps`
- `get:bootcamp-detail`
- `update:bootcamps`
- `delete:bootcamps`
- `add:courses`
- `get:course-detail`
- `update:courses`
- `delete:courses`

Roles:

- Public

  - can

    - `get:bootcamps`
    - `get:courses`

- User

  - can
    - `get:bootcamps`
    - `get:bootcamp-detail`
    - `get:courses`
    - `get:course-detail`

- Admin

  - can

    - `get:bootcamps`
    - `add:bootcamps`
    - `get:bootcamp-detail`
    - `update:bootcamps`
    - `delete:bootcamps`
    - `get:courses`
    - `add:courses`
    - `get:course-detail`
    - `update:courses`
    - `delete:courses`

  - Register 2 users - assign the Barista role to one and Manager role to the other.
  - Sign into each account and make note of the JWT.
  - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
  - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
  - Run the collection and correct any errors.
  - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## Tests

### Endpoints

Test your endpoints with [Postman](https://getpostman.com). Import the postman collection `/rivalapp-endpoint-tests.postman_collection.json`

The collection is intended to make testing the endpoints easier by providing the information needed such as token, request body and headers. Run tests in the order they are listed one by one.

If the JWT tokens are expired, refer to `.env` folder located at the root folder of this project. Tokens will be refreshed every 24 hours for testing.

![Example]('/assets/collection_example.png)

### Unit Tests

Ther are two different set of test files for each model, Bootcamp and Course. In order to run tests navigate to the root folder and run the following commands:

To run the tests first run:

```bash
psql -U postgres
createdb rival_test
```

Then, to run tests for bootcamps:

```bash
$ pipenv run python test_bootcamp.py
```

To run tests for courses:

```bash
$ pipenv run python test_course.py
```

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal server error

It will also return the following error types if authorization or authentication fails:

- 401: Authorization header is expected.
- 401: Authorization header must start with "Bearer".
- 401: Token not found.
- 401: Authorization header must be bearer token.
- 401: Permissions not included in JWT.
- 401: Permission not found.
- 401: Token expired.
- 401: Incorrect claims. Please, check the audience and issuer.
- 401: Unable to parse authentication token.
- 401: Unable to find the appropriate key.

## Endpoint Library

### GET '/bootcamps'

General:

- Returns status code 200 and json object { "success": True, "data": bootcamps}
  where bootcamps is the list of all bootcamp
- Request Arguments: None
- Access public

Returns:

- An object with success, and data keys.
- 'data' key contains a short format of bootcamp object that contains the following key:value pairs:
  - id:integer,
  - name:string,
  - address:string,
  - careers:Array,
  - img_url:string,
  - upvotes:integer

```
# Sample Response

{
  "data": [
    {
      "address": "233 Bay State Rd Boston MA 02215",
      "careers": [
      "Web Development",
      "UI/UX",
      "Business"
      ],
      "id": 2,
      "img_url": "img-9.jpg",
      "name": "Devworks Bootcamp",
      "upvotes": 57
    }
  ],
  "success": true
}
```

### POST '/bootcamps'

General:

- Returns status code 201 and json object { "success": True, "data": bootcamp}
  where bootcamp is the newly create bootcamp
- Request Parameters: None
- Request Arguments:
  - name:string,
  - description:string,
  - website:string,
  - phone:string,
  - email:string,
  - address:string
  - careers:Array,
  - jobAssistance:boolean,
- Access Private (Admin Only)

Returns:

- An object with success, and data keys.
- 'data' key contains a short long format of bootcamp object that contains the following key:value pairs:
  - id:integer,
  - name:string,
  - description:string,
  - website:string,
  - phone:string,
  - email:string,
  - address:string
  - careers:Array,
  - job_assistance:boolean,
  - img_url:string,
  - upvotes:integer

```
# Sample Response

{
    "data": {
        "address": "158 St George St, Toronto, ON M5S 2V8",
        "careers": [
            "Coding",
            "Data Analytics",
            "Cybersecurity",
            "UX/UI",
            "FinTech"
        ],
        "description": "University of Toronto School of Continuing Studies (UofT SCS) Boot Camps equip you with essential skills to help guide your path to success. With strategically engineered curricula, face-to-face interaction and expert instructors, we provide an educational experience that will shape the future of your career.",
        "email": "bootcamp@trilogyed.com",
        "id": 3,
        "img_url": "img-5.jpg",
        "job_assistance": true,
        "name": "UofT SCS BootCamps",
        "phone": "(647) 245-1020",
        "upvotes": 49,
        "website": "bootcamp.learn.utoronto.ca"
    },
    "success": true
}
```

## GET /api/v1/bootcamps/<int:id>

General:

- Returns status code 200 and json object { "success": True, "data": bootcamp}
  where bootcamp is the bootcamp with the id of id that is defined within the query string
- Request Parameters: id
- Access private (User and Admin Only)

Returns:

- An object with success, and data keys.
- 'data' key contains a long format of bootcamp object that contains the following key:value pairs:
  - id:integer,
  - name:string,
  - description:string,
  - website:string,
  - phone:string,
  - email:string,
  - address:string
  - careers:Array,
  - job_assistance:boolean,
  - img_url:string,
  - upvotes:integer

```
# Sample Response

{
    "data": {
        "address": "158 St George St, Toronto, ON M5S 2V8",
        "careers": [
            "Coding",
            "Data Analytics",
            "Cybersecurity",
            "UX/UI",
            "FinTech"
        ],
        "description": "University of Toronto School of Continuing Studies (UofT SCS) Boot Camps equip you with essential skills to help guide your path to success. With strategically engineered curricula, face-to-face interaction and expert instructors, we provide an educational experience that will shape the future of your career.",
        "email": "bootcamp@trilogyed.com",
        "id": 3,
        "img_url": "img-5.jpg",
        "job_assistance": true,
        "name": "UofT SCS BootCamps",
        "phone": "(647) 245-1020",
        "upvotes": 49,
        "website": "bootcamp.learn.utoronto.ca"
    },
    "success": true
}
```

### PUT /api/v1/bootcamps/<int:id>

General:

- Returns status code 200 and json object { "success": True, "data": bootcamp} where bootcamp is
  the updated bootcamp with the id of id that is defined within the query string
- Request Parameters: id
- Request Arguments:
  - name:string,
  - description:string,
  - website:string,
  - phone:string,
  - email:string,
  - address:string
  - careers:Array,
  - jobAssistance:boolean,
  - img_url:string,
  - upvotes:integer
- Access private (Only Admin)

Returns:

- An object with success, and data keys.
- 'data' key contains a long format of bootcamp object that contains the following key:value pairs:
  - id:integer,
  - name:string,
  - description:string,
  - website:string,
  - phone:string,
  - email:string,
  - address:string
  - careers:Array,
  - job_assistance:boolean,
  - img_url:string,
  - upvotes:integer

```
# Sample Response

{
    "data": {
        "address": "158 St George St, Toronto, ON M5S 2V8",
        "careers": [
            "Coding",
            "Data Analytics",
            "Cybersecurity",
            "UX/UI",
            "FinTech"
        ],
        "description": "University of Toronto School of Continuing Studies (UofT SCS) Boot Camps equip you with essential skills to help guide your path to success. With strategically engineered curricula, face-to-face interaction and expert instructors, we provide an educational experience that will shape the future of your career.",
        "email": "bootcamp@trilogyed.com",
        "id": 3,
        "img_url": "img-5.jpg",
        "job_assistance": true,
        "name": "UofT SCS BootCamps",
        "phone": "(647) 245-1020",
        "upvotes": 85, // Updated
        "website": "bootcamp.learn.utoronto.ca"
    },
    "success": true
}
```

### DELETE /api/v1/bootcamps/<int:id>

General:

- Returns status code 200 and json object { "success": True }
- Request Parameter: id
- Request Arguments: None
- Access private (Only Admin)

Returns:

- An object with success set to 'true' or 'false'

```
# Sample Response

{
  "success": true
}
```

### GET /api/v1/courses

General:

- Returns status code 200 and json object { "success": True, "data": courses}
  where courses is the list of all courses objects
- Request Arguments: None
- Access public

Returns:

- An object with success, and data keys.
- 'data' key contains a list of all the bootcamp objects that contains the following key:value pairs:
  - id:integer,
  - title:string,
  - upvotes:integer

```
# Sample Response

{
  "data": [
    {
      "bootcamp_id": 3,
      "id": 4,
      "title": "Front End Web Development",
      "upvotes": 74
    }
  ],
  "success": true
}
```

### POST /api/v1/courses

General:

- Returns status code 201 and json object { "success": True, "data": course}
  where course is the newly create course
- Request Parameters: None
- Request Arguments:
  - bootcampId:int,
  - title:string,
  - description:string,
  - duration:string,
  - tuition:string,
  - email:string,
  - minimumSkill:string
  - scholarshipsAvailable:boolean,
- Access Private (Only Admin)

Returns:

- An object with success, and data keys.
- 'data' key contains a long format of course object that contains the following key:value pairs:
  - id:integer,
  - bootcamp_id:int,
  - title:string,
  - description:string,
  - duration:string,
  - tuition:string,
  - email:string,
  - minimum_skill:string
  - scholarships_available:boolean,
  - upvotes:integer

```
# Sample Response

{
  "data": {
    "bootcamp_id": 1,
    "description": "This course will provide you with all of the essentials to become a successful frontend web developer. You will learn to master HTML, CSS and front end JavaScript, along with tools like Git, VSCode and front end frameworks like Vue",
    "duration": 8,
    "id": 2,
    "minimum_skill": "beginner",
    "scholarships_available": true,
    "title": "Front End Web Development",
    "tuition": 8000,
    "upvotes": 52
  },
  "success": true
}
```

### PUT /api/v1/courses/<int:id>

General:

- Returns status code 200 and json object { "success": True, "data": course}
  where course is the updated course with the id provided within the query string
- Request Parameters: id
- Request Arguments:
  - title:string
  - description:string,
  - duration:integer,
  - minimumSkill:string
  - scholarshipsAvailable:boolean,
  - tuition:integer
  - upvotes:integer
- Access private (Only Admins)

Returns:

- An object with success, and data keys.
- 'data' key contains a long format of course object that contains the following key:value pairs:
  - id:integer,
  - bootcamp_id:int,
  - title:string,
  - description:string,
  - duration:string,
  - tuition:string,
  - email:string,
  - minimum_skill:string
  - scholarships_available:boolean,
  - upvotes:integer

```
# Sample Response

{
  "data": {
    "bootcamp_id": 3,
    "description": "This course will provide you with all of the essentials to become a successful frontend web developer. You will learn to master HTML, CSS and front end JavaScript, along with tools like Git, VSCode and front end frameworks like Vue",
    "duration": 8,
    "id": 4,
    "minimum_skill": "beginner",
    "scholarships_available": false,
    "title": "Front End Web Development",
    "tuition": 10000,
    "upvotes": 100
  },
  "success": true
}
```

### DELETE /api/v1/courses/<int:id>

- Returns status code 200 and json object { "success": True }
- Request Parameter: id
- Request Arguments: None
- Access private (Only Admin)

Returns:

- An object with success set to 'true' or 'false'

```
# Sample Response

{
  "success": true
}
```
