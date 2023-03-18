from ..models import Course, Student, Grade
from flask_restx import Namespace, fields, Resource
from flask import request, abort
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..admin.views import admin_required
from ..utils import db
from ..students.views import student_model



course_namespace = Namespace('course', description = 'Namespace For all courses')


course_create_model = course_namespace.model(
    'CourseCreate',{
        'id': fields.Integer(description = 'The Course ID no.', readonly = True),
        'course_title': fields.String(description='add the course title', required = True),
        'course_code': fields.String(description = 'add the course code', required = True),
        'course_lecturer': fields.String(description= 'add the teacher for the course', required = True)
    }
)

course_update_model = course_namespace.model(
    'CourseUpdate',{
        'course_lecturer': fields.String(description= 'add the teacher for the course')
    }
)

course_add_model = course_namespace.model(
    'CourseAdd',{
        'course1': fields.String(description = 'add the course code for first course'),
        'course2': fields.String(description = 'add the course code for second course'),
        'course3': fields.String(description = 'add the course code for third course'),
        'course4': fields.String(description = 'add the course code for fourth course'),
        'course5': fields.String(description = 'add the course code for final course')
    }
)


course_delete_model = course_namespace.model(
    'CourseDelete',{
        'course': fields.String(description = 'add the course code for the course to delete')
    }
)

grade_add_model = course_namespace.model(
    'GradeAdd',{
        'id': fields.Integer(description = 'id of the Grade', readonly = True),
        'score': fields.Float(description = 'Add The Student Score For The Course'),
        'grade': fields.String(description = 'Add The Grade Weght Of The Score')
    }
)

grade_view_model = course_namespace.model(
    'GradeView', {
        'id': fields.Integer(description = 'id of the grade', readonly = True),
        'score': fields.Float(decription = 'The Score of The Student'),
        'grade_weight': fields.String(description = 'The Grade of The Student'),
        'course_identifier': fields.String(description = 'Id of The COurse'),
        'student_identifier': fields.String(description = 'Id of the student')
    }
)



@course_namespace.route('/courses')
class GetCreateCourses(Resource):

    @course_namespace.doc(description = 'Admin Creates A Course To The Institution')
    @jwt_required()
    @admin_required()
    @course_namespace.expect(course_create_model)
    @course_namespace.marshal_with(course_create_model)
    def post(self):

        """
            Create A Course For The Institution
        """

        data = request.get_json()

        course = Course(
            course_title = data.get('course_title'),
            course_code = data.get('course_code'),
            course_lecturer = data.get('course_lecturer')
        )

        course.save()


        return course, HTTPStatus.CREATED
    

    @course_namespace.doc(description = 'Get A List Of All The Courses In The Institution')
    @jwt_required()
    @course_namespace.marshal_list_with(course_create_model)
    def get(self):

        """ 
            Get A List Of All The Courses In The Institution
        """

        courses = Course.query.all()

        return courses, HTTPStatus.OK
    


@course_namespace.route('/course/<int:course_id>')
class GetUpdateDeleteCourse(Resource):

    @course_namespace.doc(
            description = 'Get The Details Of A Particular Course',
            params = {
                'course_id': 'ID of The Course'
            }
            )
    @jwt_required()
    @course_namespace.marshal_with(course_create_model)
    def get(self,course_id):

        """
            Get The Details Of A Particular Course
        """

        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK
    

    @course_namespace.doc(
            description = 'Delete A Course By The ID',
            params = {
                'course_id': 'ID of The Course'
            }
            )
    @jwt_required()
    @admin_required()
    def delete(self, course_id):

        """ 
            Delete A Particular Course
        """

        course_to_delete = Course.get_by_id(course_id)

        db.session.delete(course_to_delete)
        db.session.commit()

        return {'message': 'Course Deleted Successfully'}, HTTPStatus.OK


    @course_namespace.doc(
            description = 'Update The Details Of A Particular Course',
            params = {
                'course_id': 'ID of The Course'
            }
            )
    @jwt_required()
    @admin_required()
    @course_namespace.expect(course_update_model)
    @course_namespace.marshal_with(course_create_model)
    def put(self, course_id):

        """ 
            Update The Details For A Course
        """

        course_to_update = Course.get_by_id(course_id)

        data = request.get_json()

        course_to_update.course_lecturer = data.get('course_lecturer')


        db.session.commit()

        return course_to_update, HTTPStatus.ACCEPTED
    



@course_namespace.route('/<int:student_id>/courses')
class StudentGetAddDeleteCourses(Resource):


    @course_namespace.doc(
            description = 'Student Adds Courses To Their CourseList Using The Course Code',
            params = {
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    @course_namespace.expect(course_add_model)
    def post(self, student_id):

        """ 
            Student Adds Courses To Their CourseList Using The Course Code
        """

        data = request.get_json()
        

        student = Student.get_by_id(student_id)

        username = get_jwt_identity()

        if student.username == username:

            for course in data:

                course_code = data[course]

                course = Course.query.filter_by(course_code=course_code).first()

                student.course_list.append(course)
            db.session.commit()

            return {'message': 'Courses Added Successfully'}, HTTPStatus.ACCEPTED
        
        else:
            return{'message': 'You Are Not Authorized To Make Changes To This Student Account'}, HTTPStatus.FORBIDDEN
        

    @course_namespace.doc(
            description = 'Get All Courses Registered By A Student',
            params = {
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    @course_namespace.marshal_list_with(course_create_model)
    def get(self, student_id):

        """ 
            Get All Courses Registered By A student
        """
        
        student = Student.get_by_id(student_id)

        username = get_jwt_identity()

        if username == student.username:

            student_courses = student.course_list

            return student_courses, HTTPStatus.OK
        
        else:
            abort('You Are Not Authorized To Make Changes To This Student Account', HTTPStatus.FORBIDDEN)
    
    @course_namespace.doc(
            description = 'Student Remove Course From Their List',
            params = {
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    @course_namespace.expect(course_delete_model)
    def delete(self, student_id):

        """
            Delete A Course From a Student's Course List
        """

        data = request.get_json()

        student = Student.get_by_id(student_id)

        username = get_jwt_identity()

        if username == student.username:

            course_to_delete = Course.query.filter_by(course_code = data.get('course')).first()

            student.course_list.remove(course_to_delete)

            db.session.commit()

            return {'message': 'Course Removed Successfully'}, HTTPStatus.OK

        else:
            abort('You Are Not Authorized To Make Changes To This Student Account', HTTPStatus.FORBIDDEN)


@course_namespace.route('/<int:course_id>/students')
class GetStudentsInACourse(Resource):


    @course_namespace.doc(
            description = 'Get Students Registered For A Course',
            params = {
                'course_id': 'ID of The Course'
            }
            )
    @jwt_required()
    @admin_required()
    @course_namespace.marshal_list_with(student_model)
    def get(self, course_id):

        """ 
            Get Students Registered For A Course
        """

        course = Course.get_by_id(course_id)

        students = course.pupils

        return students, HTTPStatus.OK
    

@course_namespace.doc(
            description = 'Add The Grade For A Student In A COurse',
            params = {
                'course_id': 'ID of the Course',
                'student_id': 'ID of The Student'
            }
            )
@course_namespace.route('/<int:course_id>/grade/<int:student_id>')
class StudentAddUpgradeGetGrade(Resource):

    @jwt_required()
    @admin_required()
    @course_namespace.expect(grade_add_model)
    def post(self, course_id, student_id):

        """ 
            Add The Grade For A Student In A Course
        """

        data = request.get_json()
        grade_check = Grade.query.filter_by(course_identifier = str(course_id), student_identifier = str(student_id)).first()
        if grade_check is None:
            grade = Grade(
                score = data.get('score'),
                grade_weight = data.get('grade'),
                course_identifier = str(course_id),
                student_identifier = str(student_id)
            )

            grade.save()

            return {'message': 'Grade Added Successfully'}, HTTPStatus.CREATED
        
        else:
            return {'message': 'Grade Already Exists'}, HTTPStatus.FORBIDDEN
    

    @course_namespace.doc(
            description = 'Get The Details For A Particular Grade',
            params = {
                'course_id': 'ID of the Course',
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    @admin_required()
    @course_namespace.marshal_with(grade_view_model)
    def get(self,course_id,student_id):

        """ 
            Get The details for a particular Grade
        """

        grade = Grade.query.filter_by(course_identifier = str(course_id), student_identifier = str(student_id)).first()

        return grade, HTTPStatus.OK
    

    @course_namespace.doc(
            description = 'Update A Particula Grade',
            params = {
                'course_id': 'ID of the Course',
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    @admin_required()
    @course_namespace.expect(grade_add_model)
    def put(self, course_id, student_id):

        """ 
            Update The Details for a particular Grade
        """

        data = request.get_json()

        grade = Grade.query.filter_by(course_identifier = str(course_id), student_identifier = str(student_id)).first()

        grade.score = data.get('score')
        grade.grade_weight = data.get('grade')

        db.session.commit()

        return {'message':'The Grade has been updated successfully'}, HTTPStatus.ACCEPTED
    


@course_namespace.route('/grades/<int:student_id>/student')
class GetStudentGrades(Resource):

    @course_namespace.doc(
            description = "Get All Of A Student's Grades",
            params = {
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    def get(self, student_id):

        """
            Get All Of A Students Grades
        """
        student = Student.get_by_id(student_id)
        student_name = student.username
        current_user = get_jwt_identity()

        if current_user == student_name:
    
            grades = Grade.query.filter_by(student_identifier = str(student_id))
            
            grade_list = []

            for grade in grades:
                
                grade_course = Course.get_by_id(int(grade.course_identifier))

                grade_info = {
                    'course': grade_course.course_code,
                    'score': grade.score,
                    'grade': grade.grade_weight
                }
                

                grade_list.append(grade_info)


            return{'grades_for': student.matric_no, 'grade_list':grade_list}, HTTPStatus.OK
        

        else:
            return{'message': 'You are not Authorized To View This'}, HTTPStatus.FORBIDDEN
        

@course_namespace.route('/grades/<int:course_id>/course')
class GetCourseGrades(Resource):

    @course_namespace.doc(
            description = 'Get All The Grades Obtained In A Course',
            params = {
                'course_id': 'ID of the Course'
            }
            )
    @jwt_required()
    @admin_required()
    def get(self, course_id):

        """ 
            Get The Grades Obtained In A Course
        """

        course = Course.get_by_id(course_id)

        course_code = course.course_code


        grades = Grade.query.filter_by(course_identifier = str(course_id))
        grade_list = []

        for grade in grades:

            grade_student = Student.get_by_id(int(grade.student_identifier))

            grade_info = {
                    'student': grade_student.matric_no,
                    'score': grade.score,
                    'grade': grade.grade_weight
                }
                

            grade_list.append(grade_info)

        return{'grades_for': course_code, 'grade_list': grade_list}, HTTPStatus.OK
    

@course_namespace.route('/student/<int:student_id>/gpa')
class GetStudentGPA(Resource):

    @course_namespace.doc(
            description = 'Get The GPA for a registered student',
            params = {
                'student_id': 'ID of The Student'
            }
            )
    @jwt_required()
    def get(self, student_id):

        """ 
            Get The GPA for a registered student
        """

        student = Student.get_by_id(student_id)

        grades = Grade.query.filter_by(student_identifier = str(student_id))

        current_user = get_jwt_identity()

        grade_weight_list = []

        if student.username == current_user:

            for grade in grades:

                grade_weight = grade.grade_weight

                grade_weight_list.append(grade_weight)

            grade_score_list = []
            for grade_score in grade_weight_list:

                if grade_score == "A":

                    grade_point = 4.00

                elif grade_score == "B":

                    grade_point = 3.00

                elif grade_score == "C":

                    grade_point = 2.00

                elif grade_score == "D":

                    grade_point = 1.00

                elif grade_score == "F":

                    grade_point = 0.00

                grade_score_list.append(grade_point)

            gp = 0.00

            for element in grade_score_list:

                gp += element

            gpa = gp/len(grade_score_list)

            return {'GPA Value': gpa}, HTTPStatus.OK
        

        else:

            return{'message': 'You are not permitted to view this student gpa'}, HTTPStatus.UNAUTHORIZED