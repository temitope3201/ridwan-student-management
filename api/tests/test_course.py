import unittest
from .. import create_app
from ..config import config_dict
from ..utils import db
from..models import Admin, Student
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

        # get all students

        response = self.client.get('/student/all_students', headers = admin_headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "username": "teststudent",
            "first_name": "Test",
            "last_name": "Student",
            "matric_no": "SOE/STD/13/0001"
        }]

        student_change_password = {
            "old_password":"Student",
            "new_password": "password"
        }

        response = self.client.post('/student/change_password', json = student_change_password ,headers=student_headers)

        assert response.status_code == 200

        response = self.client.get('/student/1', headers = admin_headers)

        assert response.json == {
            "id": 1,
            "username": "teststudent",
            "first_name": "Test",
            "last_name": "Student",
            "matric_no": "SOE/STD/13/0001"
        }

        assert response.status_code == 200

        response = self.client.put('/student/1', json = student_signup_data ,headers = admin_headers)

        assert response.status_code == 202

        response = self.client.delete('/student/1', headers = admin_headers)

        assert response.status_code == 202


        