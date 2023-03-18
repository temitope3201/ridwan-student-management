from flask import Flask
from flask_restx import Api
from .config import config_dict
from .utils import db
from flask_jwt_extended import JWTManager
from api.models import User, Admin, Student, Course, coursetable, Grade
from .admin.views import admin_namespace
from .courses.views import course_namespace
from .students.views import student_namespace
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound,MethodNotAllowed,Forbidden



def create_app(config = config_dict['dev']):

    app = Flask(__name__)
    authorizations ={
        "Bearer Auth":{
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description":"Add a JWT token to the Header with **Bearer&lt;JWT&gt token to authorize"
        }
    }
    
    api = Api(app,
        title="Student Management API", 
        description="A simple Student Management REST API service",
        version=1.0,
        authorizations= authorizations,
        security="Bearer Auth"
        )
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app,db)

    jwt = JWTManager(app)

    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(student_namespace, path='/student')

    @api.errorhandler(NotFound)
    def not_found(error):

        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):

        return {"error": "Method Not Allowed"}, 405

    @api.errorhandler(Forbidden)
    def forbidden(error):

        return {"error": "Forbidden"}, 403

    @app.shell_context_processor
    def make_shell_context():

        return{
            'db': db,
            'user': User,
            'admin': Admin,
            'student': Student,
            'course': Course,
            'coursetable': coursetable,
            'grade': Grade
        }

    return app
