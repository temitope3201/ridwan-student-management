from functools import wraps
from ..models import Admin
from flask_restx import Namespace, fields, Resource, abort
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, verify_jwt_in_request, get_jwt
from ..models import Role
from ..utils import db


admin_namespace = Namespace('admin', description = 'Namespace For all Admin Authentication')

signup_model = admin_namespace.model(
    'AdminSignup',{
        'email': fields.String( description = 'Add Email Address',required = True),
        'username': fields.String( description = 'Add Username',required = True),
        'first_name': fields.String( description = 'add first name',required = True),
        'last_name': fields.String(description = 'Add last name',required = True),
        'password': fields.String( description = 'Add Password', required = True),
        'designation': fields.String(description = 'Add The Role of the user', required = True, enum=['admin', 'student'])
    }
)

admin_model = admin_namespace.model(
    'Admin',{
        'username': fields.String( description = 'Add Username',required = True),
        'first_name': fields.String( description = 'add first name',required = True),
        'last_name': fields.String( description = 'Add Last Name',required = True)
    }
)

login_model = admin_namespace.model(
    'Login', {
        'username': fields.String(description = 'Add Username', required = True ),
        'password': fields.String(description ='Add Password', required = True)
    }
)

password_refresh_model = admin_namespace.model(
    'PasswordRefresh', {
        'old_password': fields.String(description = 'Add Old Password', required = True),
        'new_password': fields.String(description = ' Add The New Password', required = True)
    }
)


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Only Admins are allowed access, kindly contact your admin"), 403

        return decorator

    return wrapper



@admin_namespace.route('/signup')
class AdminSignup(Resource):

    

    @admin_namespace.expect(signup_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description ='Create an Admin Account')
    def post(self):

        """
            Create an Admin Account
        """

        data = request.get_json()

        admin_acc = Admin(
            email = data.get('email'),
            username = data.get('username'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            password_hash = generate_password_hash(data.get('password')),
            designation = data.get('designation')
        )

        if len(Admin.query.all()) == 0:

            admin_acc.save()

            return admin_acc, HTTPStatus.CREATED

        else:

            abort(400, 'Only Existing Admin can Add a New Admin Account')
        

@admin_namespace.route('/add_account')
class AdminAddNewAccount(Resource):

    @jwt_required()
    @admin_required()
    @admin_namespace.expect(signup_model)
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(description ='Admin adds new Admins')
    def post(self):
        
        """
        Admin adds new accounts to the database
        """

        data = request.get_json()

        admin_add = Admin(
            email = data.get('email'),
            username = data.get('username'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            password_hash = generate_password_hash(data.get('last_name')),
            designation = data.get('designation')
        )

        

        admin_add.save()

        return admin_add, HTTPStatus.CREATED
    

@admin_namespace.route('/login')
class AdminLogin(Resource):

    @admin_namespace.expect(login_model)
    @admin_namespace.doc(description ='Generate Admin Token')
    def post(self):

        """
            Generate Admin Token
        """

        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        admin = Admin.query.filter_by(username = username).first()

        if admin and check_password_hash(admin.password_hash, password) and admin.designation == Role.admin:

            access_token = create_access_token(identity=admin.username, additional_claims={'is_administrator': True})
            refresh_token = create_refresh_token(identity = admin.username, additional_claims={'is_administrator': True})

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED
        
        else:
            abort(400, 'username and password mismatch')
        

@admin_namespace.route('/refresh')
class RefreshAdminToken(Resource):

    @admin_namespace.doc(description ='Generate Refresh Token')
    @jwt_required(refresh=True)
    def post(self):

        """
            Generate Refresh Token
        """

        username = get_jwt_identity()

        access_token = create_access_token(identity=username, additional_claims={'is_administrator': True})

        return {'username': username,'access_token': access_token}, HTTPStatus.OK
    

@admin_namespace.route('/change_password')
class AdminPasswordChange(Resource):

    @jwt_required()
    @admin_namespace.expect(password_refresh_model)
    @admin_namespace.doc(description ='Admin password Change')
    def post(self):

        """
            Admin password Change
        """

        username = get_jwt_identity()
        data = request.get_json()

        admin = Admin.query.filter_by(username = username).first()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if check_password_hash(admin.password_hash, old_password):

            admin.password_hash = generate_password_hash(new_password)

            db.session.commit()

            return {'message': 'Password Changed Successfully'}, HTTPStatus.OK
        
        else:

            abort(400, 'passwords do not match')
