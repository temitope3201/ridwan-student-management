import unittest
from .. import create_app
from ..config import config_dict
from ..utils import db
from..models import Admin, Student, Course
from flask_jwt_extended import create_access_token, create_refresh_token

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config = config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_student(self):

        # Sign Up An Admin

        admin_signup_data = {
            "email": "testadmin@gmail.com",
            "username": "testadmin",
            "first_name": "Test",
            "last_name": "Admin",
            "password": "password",
            "designation": "admin"
        }

        response = self.client.post('/admin/signup', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        assert admin.first_name == "Test"

        assert admin.last_name == "Admin"

        assert response.status_code == 201

        # Sign an admin in
        admin_login_data = {
            "username":"testadmin",
            "password": "password"
        }
        response = self.client.post('/admin/login', json=admin_login_data)

        assert response.status_code == 201

        token = create_access_token(identity=admin.username, additional_claims={'is_administrator':True})

        admin_headers = {
            "Authorization": f"Bearer {token}"
        }

        # Create A Sutdent Account

        student_signup_data = {
            "username": "teststudent",
            "first_name": "Test",
            "last_name": "Student",
            "email": "teststudent@gmail.com",
        }

        response = self.client.post('/student/signup', json = student_signup_data, headers=admin_headers)

        student = Student.query.filter_by(email='teststudent@gmail.com').first()

        assert student.first_name == "Test"

        assert student.matric_no == "SOE/STD/13/0001"

        assert response.status_code == 201

        #login a student

        student_login_data = {
            "email":"teststudent@gmail.com",
            "password": "Student"
        }

        response = self.client.post('/student/login', json = student_login_data)

        assert response.status_code == 201

        student_token = create_access_token(identity=student.username)

        student_headers = {
            "Authorization": f"Bearer {student_token}"
        }
        # create a course
        course_create_data = {
        
        'course_title': "test course",
        'course_code': "tst 101",
        'course_lecturer': "dr. test"
        }

        response = self.client.post('course/courses', json = course_create_data, headers = admin_headers)

        assert response.status_code == 201

        assert response.json == {
        'id':1,
        'course_title': "test course",
        'course_code': "tst 101",
        'course_lecturer': "dr. test"
        }
        # get all courses
        response = self.client.get('course/courses', headers = admin_headers)

        assert response.status_code == 200

        assert response.json == [{
        'id':1,
        'course_title': "test course",
        'course_code': "tst 101",
        'course_lecturer': "dr. test"
        }]

        #  get info for a course
        response = self.client.get('/course/course/1', headers = admin_headers)

        assert response.status_code == 200
        assert response.json == {
        'id':1,
        'course_title': "test course",
        'course_code': "tst 101",
        'course_lecturer': "dr. test"
        }
        # delete a course
        response = self.client.delete('/course/course/1', headers = admin_headers)

        assert response.status_code == 200

        # update a course
        response = self.client.post('course/courses', json = course_create_data, headers = admin_headers)

        assert response.status_code == 201

        course_update_data = {"course_lecturer" : "dr. test"}


        response = self.client.put('/course/course/1', json = course_update_data, headers = admin_headers)

        assert response.status_code == 202
        assert response.json == {
        'id':1,
        'course_title': "test course",
        'course_code': "tst 101",
        'course_lecturer': "dr. test"
        }

        # sudent course registration

        course_register_data = {
            'course1': 'tst 101'
        }

        response = self.client.post('/course/1/courses', json = course_register_data ,headers = student_headers)

        assert response.status_code == 202

        # get all courses for a student

        response = self.client.get('course/1/courses', headers = student_headers)

        assert response.status_code == 200




