

# from datetime import datetime
#
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()


# class Student(db.Model):
#     s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     s_name = db.Column(db.String(16), unique=True)
#     s_age = db.Column(db.Integer, default=16)
#     grades = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    # __tablename__ = 'student'

    # def __init__(self, name, age):
    #     self.s_name = name
    #     self.s_age = age


# class Grade(db.Model):
#
#     g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     g_name = db.Column(db.String(16), unique=True, nullable=False)
#     g_desc = db.Column(db.String(30), nullable=True)
#     g_create_time = db.Column(db.DateTime, default=datetime.now)
#     students = db.relationship('Student', backref='grade', lazy=True)
#
#     __tablename__ = 'grade'


# Accompany。 2018/6/14 8:41:52

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 学生
class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16), unique=True)
    s_age = db.Column(db.Integer, default=16)
    grades = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    # __tablename__ = 'student'

    # def __init__(self, name, age):
    #     self.s_name = name
    #     self.s_age = age


# 班级
class Grade(db.Model):

    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(16), unique=True, nullable=False)
    g_desc = db.Column(db.String(30), nullable=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade', lazy=True)

    __tablename__ = 'grade'


sc = db.Table('sc',
              db.Column('s_id', db.Integer, db.ForeignKey('student.s_id'), primary_key=True),
              db.Column('c_id', db.Integer, db.ForeignKey('course.c_id'), primary_key=True),
              )


# 课程
class Course(db.Model):

    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 课程id
    c_name = db.Column(db.String(16), unique=True)
    c_create_time = db.Column(db.DateTime, default=datetime.now())
    students = db.relationship('Student',
                               secondary=sc,
                               backref='course')

    __tablename__ = 'course'


# 用户
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now())

    __tablename__ = 'user'

    def __init__(self, username, password):

        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit(self)


class Role(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True)
