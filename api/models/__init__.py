from ..utils import db
from enum import Enum

class Role(Enum):
    admin = 'admin'
    student = 'student'
    



coursetable = db.Table('coursetable',
                       db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key = True),
                       db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key = True)
                       )



class User(db.Model):

    __abstract__ = True


    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(), nullable = False, unique = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    first_name = db.Column(db.String(60), nullable = False)
    last_name = db.Column(db.String(60), nullable = False)
    password_hash = db.Column(db.String(), nullable = False)
    designation = db.Column(db.Enum(Role), default = Role.student)
    password_reset_token = db.Column(db.String())
    type = db.Column(db.String())

class Student(User):

    

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    
    matric_no = db.Column(db.String(20), nullable = False, unique =True)
    course_list = db.relationship('Course', secondary = coursetable, lazy = 'subquery', backref = db.backref('pupils', lazy = True))
    
    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)


class Course(db.Model):

   

    id = db.Column(db.Integer, primary_key = True)
    course_title = db.Column(db.String(), nullable = False)
    course_code = db.Column(db.String(), nullable = False, unique = True)
    course_lecturer = db.Column(db.String(), nullable = False)
    
    

    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)



class Admin(User):

    __tablename__ = 'admins'

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)




class Grade(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Float(), nullable = False)
    grade_weight = db.Column(db.String(), nullable = False)
    course_identifier = db.Column(db.String(), nullable = False)
    student_identifier = db.Column(db.String(), nullable = False)


    def save(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):

        return cls.query.get_or_404(id)
