from flask import Flask, request, jsonify
from flask_cors import CORS
from models import setup_db


app = Flask(__name__)
setup_db(app)


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "success": True
    })
