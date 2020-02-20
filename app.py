from flask import Flask, request, jsonify
from flask_sqlalchemy import sqlalchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
# ...

# load dotenv in the base root
# refers to application_top
basedir = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DEV_DATABASE_URI'] = os.getenv('DEV_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "success": True,
    })
