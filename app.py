from bootcamp import get_bootcamps
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


# @app.route('/api/v1/bootcamps', methods=['GET'])
# def bootcamps():
#     bootcamps = Bootcamp.query.all()

#     if len(bootcamps) == 0:
#         abort(404)

#     bootcamps = [bootcamp.format_short() for bootcamp in bootcamps]

#     data = jsonify({
#         "success": True,
#         "data": bootcamps
#     })

#     return data, status.HTTP_200_OK
