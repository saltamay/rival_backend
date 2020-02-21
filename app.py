from bootcamp import *
from course import *
from auth import AuthError, requires_auth
from models import setup_db, Bootcamp, Course
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_api import status
import os
from dotenv import load_dotenv

# load dotenv in the base root
# refers to application_top
basedir = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
setup_db(app)


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "success": True
    })


@app.route('/test')
def get_greeting():
    excited = os.getenv('EXCITED')
    greeting = "Hello"
    if excited == 'true':
        greeting = greeting + "!!!!!"
    return greeting


'''
    GET /api/v1/bootcamps
        Returns status code 200 and
            json object { "success": True, "data": bootcamps}
            where bootcamps is the list of all bootcamps
        Access public
'''


@app.route('/api/v1/bootcamps', methods=['GET'])
def bootcamps():
    bootcamps = get_bootcamps()

    if len(bootcamps) == 0:
        abort(404)

    bootcamps = [bootcamp.format_short() for bootcamp in bootcamps]

    data = jsonify({
        "success": True,
        "data": bootcamps
    })

    return data, status.HTTP_200_OK

    '''
    POST /api/v1/bootcamps
        Returns status code 201 and
            json object { "success": True, "data": bootcamp}
            where bootcamp is the newly create bootcamp
        Access Private
'''


@app.route('/api/v1/bootcamps', methods=['POST'])
@requires_auth('add:bootcamps')
def bootcamp(payload):
    try:
        new_bootcamp = add_bootcamp(request)

        data = jsonify({
            "success": True,
            "data": new_bootcamp.format_long()
        })
        return data, status.HTTP_201_CREATED
    except BaseException:
        abort(422)


'''
    GET /api/v1/bootcamps/<int:id>
        Returns status code 200 and
            json object { "success": True, "data": bootcamp}
            where bootcamp is the bootcamp with the id of id
            that is defined within the query string
        Access public
'''


@app.route('/api/v1/bootcamps/<int:id>', methods=['GET'])
@requires_auth('get:bootcamp-detail')
def get_bootcamp_by_id(payload, id):
    bootcamp = get_single_bootcamp(id)

    if bootcamp is None:
        abort(404)

    data = jsonify({
        "success": True,
        "data": bootcamp.format_long()
    })
    return data, status.HTTP_200_OK
