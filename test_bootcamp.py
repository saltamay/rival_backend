from app import app
from test_db import setup_db
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import json
import unittest

USER_AUTH_TOKEN = os.getenv('USER_AUTH_TOKEN')
ADMIN_AUTH_TOKEN = os.getenv('ADMIN_AUTH_TOKEN')


class BootcampsTestCase(unittest.TestCase):
    '''This class represents the bootcamp report test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = app
        # propagate the exceptions to the test client
        self.app.testing = True
        self.client = self.app.test_client
        setup_db(self.app)

        self.user_auth_header = {
            "Authorization": f"Bearer {USER_AUTH_TOKEN}"
        }

        self.admin_auth_header = {
            "Authorization": f"Bearer {ADMIN_AUTH_TOKEN}"
        }

        self.new_bootcamp = {
            "name": "UofT SCS BootCamps",
            "description": "University of Toronto School of" +
            "Continuing Studies (UofT SCS) Boot Camps equip you" +
            "with essential skills to help guide your path to success." +
            "With strategically engineered curricula, face-to-face" +
            "interaction, and expert instructors, we provide an educational" +
            "experience that will shape the future of your career.",
            "website": "bootcamp.learn.utoronto.ca",
            "phone": "(647) 245-1020",
            "email": "bootcamp@trilogyed.com",
            "address": "158 St George St, Toronto, ON M5S 2V8",
            "careers": ["Coding", "Data Analytics",
                        "Cybersecurity", "UX/UI", "FinTech"],
            "jobAssistance": True
        }

        self.dublicate_bootcamp = {
            "name": "Devworks Bootcamp",
            "description": "Devworks is a full stack JavaScript Bootcamp" +
            "located in the heart of Boston that focuses on the technologies" +
            "you need to get a high paying job as a web developer",
            "website": "https://devworks.com",
            "phone": "(111) 111-1111",
            "email": "enroll@devworks.com",
            "address": "233 Bay State Rd Boston MA 02215",
            "careers": ["Web Development", "UI/UX", "Business"],
            "job_assistance": False,
            "upvotes": 89,
            "img_url": "/img-2.jpg"
        }

        self.updated_bootcamp = {
            "name": "Devworks Bootcamp",
            "description": "Devworks is a full stack JavaScript Bootcamp" +
            "located in the heart of Boston that focuses on the technologies" +
            "you need to get a high paying job as a web developer",
            "website": "https://devworks.com",
            "phone": "(555) 555-555",  # Update phone number
            "email": "enroll@devworks.com",
            "address": "233 Bay State Rd Boston MA 02215",
            "careers": ["Web Development", "UI/UX", "Business"],
            "jobAssistance": True,  # Update job assistance
            "upvotes": 89,
            "img_url": "/img-2.jpg"
        }

        self.updated_bootcamp_malformed = {
            "name": "Devworks Bootcamp",
            "description": "Devworks is a full stack JavaScript Bootcamp" +
            "located in the heart of Boston that focuses on the technologies" +
            "you need to get a high paying job as a web developer",
            "website: https // devworks.com"
            "phone": "(111) 111-111",
            "email": "enroll@devworks.com",
            "address": "233 Bay State Rd Boston MA 02215",
            "careers": ["Web Development", "UI/UX", "Business"],
            "job_assistance": False,
            "upvotes": 89,
            "img_url": "/img-2.jpg"
        }

    def tearDown(self):
        '''Executed after each test'''
        pass

    def test_add_bootcamp(self):
        res = self.client().post('/api/v1/bootcamps',
                                 headers=self.admin_auth_header,
                                 json=self.new_bootcamp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        self.assertTrue(len(data['data']))

    def test_get_all_bootcamps(self):
        res = self.client().get('/api/v1/bootcamps')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))

    def test_get_bootcamp_by_id(self):
        res = self.client().get('/api/v1/bootcamps/1',
                                headers=self.user_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        self.assertTrue(len(data['data']))

    def test_update_bootcamp_by_id(self):
        res = self.client().put('/api/v1/bootcamps/1',
                                headers=self.admin_auth_header,
                                json=self.updated_bootcamp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])
        self.assertTrue(len(data['data']))

    def test_delete_bootcamp_by_id(self):
        self.client().delete('/api/v1/courses/1',
                             headers=self.admin_auth_header)
        res = self.client().delete('/api/v1/bootcamps/1',
                                   headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_when_bootcamps_empty(self):
        '''Remove the element from the db'''
        self.client().delete('/api/v1/courses/1',
                             headers=self.admin_auth_header)
        self.client().delete('/api/v1/bootcamps/1',
                             headers=self.admin_auth_header)

        res = self.client().get('/api/v1/bootcamps')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_422_if_add_bootcamp_fails(self):
        res = self.client().post('/api/v1/bootcamps',
                                 headers=self.admin_auth_header,
                                 json=self.dublicate_bootcamp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_404_if_bootcamp_does_not_exist(self):
        res = self.client().get('/api/v1/bootcamps/1000',
                                headers=self.user_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_404_if_update_bootcamp_fails(self):
        res = self.client().put('/api/v1/bootcamps/1000',
                                headers=self.admin_auth_header,
                                json=self.updated_bootcamp)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_422_if_update_bootcamp_fails(self):
        res = self.client().put('/api/v1/bootcamps/1',
                                headers=self.admin_auth_header,
                                json=self.updated_bootcamp_malformed)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_404_if_delete_bootcamp_fails(self):
        res = self.client().delete('/api/v1/bootcamps/1000',
                                   headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_401_if_user_auth_missing(self):
        res = self.client().get('/api/v1/bootcamps/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_401_if_admin_auth_missing(self):
        res = self.client().delete('/api/v1/bootcamps/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')


'''Make the tests executable'''
if __name__ == "__main__":
    unittest.main()
