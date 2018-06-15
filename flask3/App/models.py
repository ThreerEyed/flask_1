from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(20), unique=True)
    u_pass = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.now())

    __tablename__ = 'user'

    def __init__(self, u_name, u_pass):
        self.u_name = u_name
        self.u_pass = u_pass


ur = db.Table('ur',
              db.Column('u_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
              db.Column('r_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True))


class Role(db.Model):

    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_name = db.Column(db.String(20), unique=True)
    users = db.relationship('User',
                            secondary=ur,
                            backref='role')

    __tablename__ = 'role'

    def __init__(self, r_name):
        self.r_name = r_name


rp = db.Table('rp',
              db.Column('r_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
              db.Column('p_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True))


class Permission(db.Model):

    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_name = db.Column(db.String(20), unique=True)
    p_english = db.Column(db.String(50),unique=True)
    roles = db.relationship('Role', secondary=rp, backref='permission')

    __tablename__ = 'permission'

    def __init__(self, p_name, p_english):
        self.p_name = p_name
        self.p_english = p_english


class Grade(db.Model):

    g_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name = db.Column(db.String(20), unique=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now())
    students = db.relationship('Student', backref='student', lazy=True)

    __tablename__ = 'grade'


class Student(db.Model):

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(20), unique=True)
    s_create_time = db.Column(db.DateTime, default=datetime.now())
    s_img = db.Column(db.String(300))
    s_birth = db.Column(db.Date)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    __tablename__ = 'student'



