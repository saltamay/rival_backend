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


@app.route('/api/v1/bootcamps/<int:id>/courses', methods=['GET'])
def get_bootcamp_courses(id):
    courses = get_all_courses(id)

    if courses is None:
        abort(404)

    courses = [course.format_long() for course in courses]

    data = jsonify({
        "success": True,
        "data": courses
    })
    return data, status.HTTP_200_OK


'''
    PUT /api/v1/bootcamps/<int:id>
        Returns status code 200 and
            json object { "success": True, "data": bootcamp}
            where bootcamp is the updated bootcamp with the id of id
            that is defined within the query string
        Access private
'''


@app.route('/api/v1/bootcamps/<int:id>', methods=['PUT'])
@requires_auth('update:bootcamps')
def update_bootcamp_by_id(payload, id):
    try:
        updated_bootcamp = update_bootcamp(request, id)

        data = jsonify({
            "success": True,
            "data": updated_bootcamp.format_long()
        })

        return data, status.HTTP_200_OK
    except Exception as ex:
        print(ex.__class__.__name__)
        if ex.__class__.__name__ == 'AttributeError':
            abort(404)
        else:
            abort(422)


@app.route('/api/v1/bootcamps/<int:id>', methods=['PATCH'])
@requires_auth('update:bootcamps')
def patch_bootcamp_by_id(id):
    try:
        updated_bootcamp = patch_bootcamp(request, id)
        data = jsonify({
            "success": True,
            "data": updated_bootcamp.format_long()
        })

        return data, status.HTTP_200_OK
    except Exception as ex:
        print(ex.__class__.__name__)
        if ex.__class__.__name__ == 'AttributeError':
            abort(404)
        else:
            abort(422)


'''
    DELETE /api/v1/bootcamps/<int:id>
        Returns status code 200 and json object { "success": True }

        Access private
'''


@app.route('/api/v1/bootcamps/<int:id>', methods=['DELETE'])
@requires_auth('delete:bootcamps')
def delete_bootcamp_by_id(payload, id):
    data = delete_bootcamp(id)

    if data is None:
        abort(404)

    return data, status.HTTP_200_OK


'''
    GET /api/v1/courses
        Returns status code 200 and
            json object { "success": True, "data": courses}
            where courses is the list of all courses
        Access public
'''


@app.route('/api/v1/courses', methods=['GET'])
def courses():
    courses = get_courses()

    if len(courses) == 0:
        abort(404)

    courses = [course.format_short() for course in courses]

    data = jsonify({
        "success": True,
        "data": courses
    })
    return data, status.HTTP_200_OK


'''
    POST /api/v1/courses
        Returns status code 201 and
            json object { "success": True, "data": course}
            where course is the newly create course
        Access Private
'''


@app.route('/api/v1/courses', methods=['POST'])
@requires_auth('add:courses')
def course(payload):
    try:
        new_course = add_course(request)

        data = jsonify({
            "success": True,
            "data": new_course.format_long()
        })
        return data, status.HTTP_201_CREATED
    except BaseException:
        abort(422)


'''
    GET /api/v1/courses/<int:id>
        Returns status code 200 and
            json object { "success": True, "data": course}
            where course is the course with the id of id
            that is defined within the query string
        Access public
'''


@app.route('/api/v1/courses/<int:id>', methods=['GET'])
@requires_auth('get:course-detail')
def get_course_by_id(payload, id):
    course = get_single_course(id)

    if course is None:
        abort(404)

    data = jsonify({
        "success": True,
        "data": course.format_long()
    })
    return data, status.HTTP_200_OK


'''
    PUT /api/v1/courses/<int:id>
        Returns status code 200 and
            json object { "success": True, "data": course}
            where course is the updated course with the id of id
            that is defined within the query string
        Access private
'''


@app.route('/api/v1/courses/<int:id>', methods=['PUT'])
@requires_auth('update:courses')
def update_course_by_id(payload, id):
    try:
        updated_course = update_course(request, id)

        data = jsonify({
            "success": True,
            "data": updated_course.format_long()
        })

        return data, status.HTTP_200_OK
    except Exception as ex:
        print(ex.__class__.__name__)
        if ex.__class__.__name__ == 'AttributeError':
            abort(404)
        else:
            abort(422)


@app.route('/api/v1/courses/<int:id>', methods=['PATCH'])
@requires_auth('update:courses')
def patch_course_by_id(id):
    try:
        updated_course = patch_course(request, id)
        data = jsonify({
            "success": True,
            "data": updated_course.format_long()
        })

        return data, status.HTTP_200_OK
    except Exception as ex:
        print(ex.__class__.__name__)
        if ex.__class__.__name__ == 'AttributeError':
            abort(404)
        else:
            abort(422)


'''
    DELETE /api/v1/courses/<int:id>
        Returns status code 200 and json object { "success": True }

        Access private
'''


@app.route('/api/v1/courses/<int:id>', methods=['DELETE'])
@requires_auth('delete:courses')
def delete_course_by_id(payload, id):
    data = delete_course(id)

    if data is None:
        abort(404)

    return data, status.HTTP_200_OK


# Default port:
if __name__ == '__main__':
    app.run()


# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(auth_error):
    print(auth_error.error)
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error['message']
    }), auth_error.status_code
