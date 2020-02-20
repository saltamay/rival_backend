from flask import Flask, request, jsonify
from flask_sqlalchemy import sqlalchemy
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "success": True
    })
