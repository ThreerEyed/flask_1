import os
from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_restful import Resource
from werkzeug.utils import secure_filename

from App.models import db, User, Grade, Student
from utils.common import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello,world'


# 创建表
@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '成功创建数据'


# 删除表
@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '数据删除成功'


# 注册界面
@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':

        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not all([username, password1, password2]):
            msg = '请填写完所有信息'
            return render_template('register.html', msg=msg)

        if User.query.filter_by(u_name=username).first():
            msg = '该用户已存在'
            return render_template('register.html', msg=msg)

        if password1 != password2:
            msg = '两次密码不一致'
            return render_template('register.html', msg=msg)

        user = User(u_name=username, u_pass=password2)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))


# 登录界面
@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            return render_template('login.html', msg='请输入用户名和密码')

        if User.query.filter_by(u_name=username).first():
            if User.query.filter_by(u_pass=password).first():
                user = User.query.filter_by(u_name=username).first()
                session['user_id'] = user.u_id
                session['username'] = user.u_name
                return redirect(url_for('user.index'), code=302)
            else:
                msg = '用户名或密码错误'
                return render_template('login.html', msg=msg)
        else:
            msg = '用户名或密码错误'
            return render_template('login.html', msg=msg)


# 退出登录
@user_blueprint.route('/logout/')
def logout():
    session['user_id'] = ''
    return redirect(url_for('user.login'))


# 修改密码
@user_blueprint.route('/changepwd/', methods=['GET', 'POST'])
def changepwd():
    if request.method == 'GET':
        username = session.get('username')
        return render_template('changepwd.html', username=username)


@user_blueprint.route('/index/', methods=['GET', 'POST'])
@is_login
def index():
    if request.method == 'GET':

        return render_template('index.html')


@user_blueprint.route('/head/', methods=['GET', 'POST'])
def head():
    if request.method == 'GET':
        username = session.get('username')
        return render_template('head.html', username=username)


# 左页面
@user_blueprint.route('/left/', methods=['GET', 'POST'])
def left():
    if request.method == 'GET':
        return render_template('left.html')


# 班级列表
@user_blueprint.route('/grade/', methods=['GET', 'POST'])
def grade():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('grade.html', grades=grades)


# 添加班级
@user_blueprint.route('/add_grade/', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'GET':
        return render_template('addgrade.html')

    if request.method == 'POST':
        grade_name = request.form.get('grade_name')

        grade = Grade()
        grade.g_name = grade_name

        db.session.add(grade)
        db.session.commit()

        return redirect(url_for('user.grade'))


# 学生列表
@user_blueprint.route('/student/', methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        students = Student.query.all()
        return render_template('student.html', students=students)


# 添加学生
@user_blueprint.route('/addstu/', methods=['GET', 'POST'])
def addstu():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html', grades=grades)

    if request.method == 'POST':
        student_name = request.form.get('s_name')
        student_sex = request.form.get('s_sex')
        student_s_birth = request.form.get('s_birth')
        student_s_img = request.files.get('s_img').filename
        student_grade_name = request.form.get('grade_name')

        student = Student()

        f = request.files['s_img']
        basepath = os.path.dirname(os.path.dirname(__file__))  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static\icons', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        student.s_name = student_name
        student.s_sex = int(student_sex)
        student.s_grade_name = student_grade_name
        student.s_img = student_s_img
        student.s_birth = student_s_birth
        grade = Grade.query.filter_by(g_name=student_grade_name).first()
        student.grade_id = grade.g_id

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('user.student'))


# 角色列表
@user_blueprint.route('/roles/', methods=['GET', 'POST'])
def roles():
    if request.method == 'GET':
        return render_template('roles.html')


# 添加角色
@user_blueprint.route('/addroles/', methods=['GET', 'POST'])
def addroles():
    if request.method == 'GET':
        return render_template('addroles.html')


# 权限列表
@user_blueprint.route('/permissions/', methods=['GET', 'POST'])
def permissions():
    if request.method == 'GET':
        return render_template('permissions.html')


# 添加权限
@user_blueprint.route('/addpermission/', methods=['GET', 'POST'])
def addpermission():
    if request.method == 'GET':
        return render_template('addpermission.html')


# 用户列表
@user_blueprint.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return render_template('users.html')


# 添加用户
@user_blueprint.route('/add_edit/', methods=['GET', 'POST'])
def add_edit():
    if request.method == 'GET':
        return render_template('add_edit.html')


@user_blueprint.route('/main/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        user_id = request.cookies.get('session')

        return render_template('main.html')


class Course(Resource):
    pass


# api.add_resource(CourseApi)

@user_blueprint.route('/upload/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(os.path.dirname(__file__))  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'media\icons',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('user.upload'))
    return render_template('upload.html')