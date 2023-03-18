from ..models import Student
from flask_restx import Namespace, fields, Resource
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from ..admin.views import admin_required
from ..utils import db

student_namespace = Namespace('student', description = 'Namespace For all Student Authentication')

signup_model = student_namespace.model(
    'StudentSignup',{
        'email': fields.String( description = 'Add Email Address',required = True),
        'username': fields.String( description = 'Add Username',required = True),
        'first_name': fields.String( description = 'add first name',required = True),
        'last_name': fields.String(description = 'Add last name',required = True)
    }
)

password_refresh_model = student_namespace.model(
    'PasswordRefresh', {
        'old_password': fields.String(description = 'Add Old Password', required = True),
        'new_password': fields.String(description = ' Add The New Password', required = True)
    }
)


student_model = student_namespace.model(
    'Student', {
        'id': fields.Integer(description = 'The Course ID no.', readonly = True),
        'username': fields.String( description = 'Student Username',required = True),
        'first_name': fields.String( description = 'Student first name',required = True),
        'last_name': fields.String( description = 'Student Last Name',required = True),
        'matric_no': fields.String(description = 'Student Matric No.', required = True )
    }
)

login_model = student_namespace.model(
    'StudentLogin', {
        'email': fields.String(description = 'Student Email', required = True),
        'password': fields.String(description = 'Student Password', required = True)
    }
)


@student_namespace.route('/signup')
class StudentSignup(Resource):

    @admin_required()
    @jwt_required()
    @student_namespace.expect(signup_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(description ='Admin Create Student Account')
    def post(self):
        
        """
            Admin Create Student Account
        """

        num = str(len(Student.query.all())+1)
        str_num = num.zfill(4)

        data = request.get_json()

        student = Student(
            email = data.get('email'),
            username = data.get('username'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            password_hash = generate_password_hash(data.get('last_name')),
            matric_no = 'SOE/STD/13/'+str_num,
        )

        student.save()

        return student, HTTPStatus.CREATED
    


@student_namespace.route('/login')
class StudentLogin(Resource):

    @student_namespace.expect(login_model)
    @student_namespace.doc(description ='Student Login Route')
    def post(self):

        """
            Student Login 
        """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email = email).first()

        if student and check_password_hash(student.password_hash, password):

            access_token = create_access_token(identity=student.username)
            refresh_token = create_refresh_token(identity=student.username)

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED
        
        else:
            return{"message": "Username Or Password Incorrect"}, HTTPStatus.BAD_REQUEST
        

@student_namespace.route('/refresh')
class RefreshStudentToken(Resource):

    @jwt_required(refresh=True)
    @student_namespace.doc(description ='Generate Refresh Token')
    def post(self):

        """
            Generate Refresh Token
        """

        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'username': username,'access_token': access_token}, HTTPStatus.OK
    

@student_namespace.route('/all_students')
class GetAllStudents(Resource):

    @admin_required()
    @jwt_required()
    @student_namespace.marshal_list_with(student_model)
    @student_namespace.doc(description ='Get All The Students')
    def get(self):

        """
        Get All The Students
        """


        students = Student.query.all()

        return students, HTTPStatus.OK



@student_namespace.route('/change_password')
class StudentPasswordChange(Resource):

    @jwt_required()
    @student_namespace.expect(password_refresh_model)
    @student_namespace.doc(description ='Students password Change')
    def post(self):

        """
            Students password Change
        """

        username = get_jwt_identity()
        data = request.get_json()

        student = Student.query.filter_by(username = username).first()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if check_password_hash(student.password_hash, old_password):

            student.password_hash = generate_password_hash(new_password)

            db.session.commit()

            return {'message': 'Password Changed Successfully'}, HTTPStatus.OK
        
        else:

            
            return{"message": "Password Mismatch"}, HTTPStatus.BAD_REQUEST



@student_namespace.route('/<int:student_id>')
class GetUpdateDeleteStudent(Resource):

    @jwt_required()
    @admin_required()
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = 'Get The Detail For A Student By ID',
        params = {
            'student_id': 'The ID of The Student'
        }
    )
    def get(self, student_id):
        
        """ 
            Get The Detail For A Student By ID
        """


        student = Student.get_by_id(student_id)

        return student, HTTPStatus.OK
    
    @jwt_required()
    @admin_required()
    @student_namespace.expect(signup_model)
    @student_namespace.doc(
        description = 'Update The Details For A Student',
        params ={
            'student_id': 'The ID of The Student'
        }
    )
    def put(self, student_id):

        """ 
            Update The Details For A Student
        """
        data = request.get_json()

        student = Student.get_by_id(student_id)

        student.email = data.get('email')
        student.username = data.get('username')
        student.first_name = data.get('first_name')
        student.last_name = data.get('last_name')

        db.session.commit()

        return {'message': 'student details updated successfully'}, HTTPStatus.ACCEPTED
    
    @jwt_required()
    @admin_required()
    @student_namespace.doc(
        description = 'Delete A student by ID',
        params ={
            'student_id': 'The ID of The Student'
        }
    )
    def delete(self, student_id):

        """ 
         Delete A student by ID
        """

        student = Student.get_by_id(student_id)

        db.session.delete(student)
        db.session.commit()

        return {'message': 'student deleted successfully'}, HTTPStatus.ACCEPTED