from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_api import status

from models import setup_db, Bootcamp, Course
from bootcamp import get_bootcamps


app = Flask(__name__)
setup_db(app)


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "success": True
    })


'''
    GET /api/v1/bootcamps
        Returns status code 200 and
            json object { "success": True, "data": bootcamps}
            where bootcamps is the list of all bootcamps
        Access public
'''


@app.route('/api/v1/bootcamps', methods=['GET'])
def bootcamps():
    bootcamps = Bootcamp.query.all()

    if len(bootcamps) == 0:
        abort(404)

    bootcamps = [bootcamp.format_short() for bootcamp in bootcamps]

    data = jsonify({
        "success": True,
        "data": bootcamps
    })

    return data, status.HTTP_200_OK
