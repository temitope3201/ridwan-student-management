import unittest
from .. import create_app
from ..config import config_dict
from ..utils import db
from..models import Admin
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

    def test_admin(self):

        # Register an admin
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

        headers = {
            "Authorization": f"Bearer {token}"
        }

        #Change Admin Password

        admin_change_password = {
            "old_password":"password",
            "new_password": "password"
        }

        response = self.client.post('/admin/change_password', json = admin_change_password, headers=headers)

        assert response.status_code == 200

        

