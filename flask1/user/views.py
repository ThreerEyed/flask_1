import random

from flask import Blueprint, render_template, make_response, request, session, redirect, url_for
from flask_restful import Resource

from user.models import db, Student, Grade, Course, User

# from utils.functions import is_login
from utils.decorator import is_login
from utils.ext_init import api

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello, world'


@user_blueprint.route('/setcookie/')
def set_cookie():
    temp = render_template('cookies.html')
    # 服务端创建响应
    res = make_response(temp, 200)
    # 绑定cookie值 set_cookie(key, values, expire， max_age)
    res.set_cookie('ticket', '123123', max_age=10)

    return res


@user_blueprint.route('/delcookie/')
def del_cookie():
    temp = render_template('cookies.html')
    # 服务端创建响应
    res = make_response(temp, 200)
    # 绑定cookie值 set_cookie(key, values, expire， max_age)
    res.delete_cookie('ticket', '')

    return res


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login1.html')
    if request.method == 'POST':
        username = request.form.get('username')

        session['username'] = username
        return render_template('login1.html', username=username)


# @is_login
@user_blueprint.route('/scores/', methods=['GET'])
def stu_scores():
    # if request.method == 'GET':

    scores = [75, 84, 35, 96, 64, 86, 46]
    return render_template('scores.html', scores=scores)


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '数据库创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '数据库删除成功'


@user_blueprint.route('/create_stu/', methods=['GET'])
def create_stu():
    stu = Student()
    stu.s_name = '张三'
    stu.s_age = '17'

    db.session.add(stu)
    db.session.commit()

    return '创建学生成功'


@user_blueprint.route('/select_stu/', methods=['GET'])
def select_stu():
    stus = Student.query.filter(Student.s_name == '张三').all()
    # stus = Student.query.filter_by(s_name='张三').all()
    return render_template('students.html', stus=stus)


# 创建或者添加学生信息
@user_blueprint.route('/create_stus/')
def create_stus():

    stu_list = []
    for i in range(25):
        stu = Student()

        stu.s_name = '小哥%d' % random.randrange(100)
        if stu.s_name in stu_list:
            continue
        stu.s_age = random.randrange(20)
        stu_list.append(stu)

    db.session.add_all(stu_list)
    db.session.commit()

    return '创建学生成功'


# 删除学生信息
@user_blueprint.route('/delete_stu/', methods=['GET', 'POST'])
def delete_stu():

    s_id = request.args.get('id')

    stu = Student.query.filter_by(s_id=s_id).first()
    g_id = stu.grade.g_id

    db.session.delete(stu)
    db.session.commit()

    return redirect(url_for('user.stus_list', g_id=g_id))


# 学生列表
@user_blueprint.route('/stus_list/<int:id>/', methods=['GET', 'POST'])
@is_login
def stus_list(id):

    if request.method == 'GET':
        # g_id = request.args.get('g_id')
        # 方式一
        stus = Student.query.filter_by(grades=id)
        # 方式二
        # sql = 'select * from student'
        # stus = db.session.execute(sql)
        return render_template('stus_list.html', stus=stus)


# 修改学生信息
@user_blueprint.route('/edit_stu/', methods=['GET', 'POST'])
def edit_stu():
    if request.method == 'GET':
        s_id = request.args.get('id')
        stu = Student.query.filter_by(s_id=s_id).first()
        return render_template('edit_stu.html', stu=stu)

    if request.method == 'POST':

        stu_id = request.args.get('id')
        stu_name = request.form.get('stu_name')
        stu_age = request.form.get('stu_age')

        stu = Student.query.filter_by(s_id=stu_id).first()
        stu.s_name = stu_name
        stu.s_age = stu_age

        db.session.commit()

        return redirect(url_for('user.stus_list'))


# 查询数据
@user_blueprint.route('/select_stus/')
def select_stus():

    # stus = Student.query.filter(Student.s_id.in_([11, 12, 13, 14]))
    # stus = Student.query.filter(Student.s_age.__lt__(10))
    # stus = Student.query.filter(Student.s_name.contains('9')
    stus = Student.query.order_by('s_id').offset(4).limit(5)
    # paginate = Student.query.paginate(2, 4)
    # stus = paginate.items
    return render_template('stus_list.html', stus=stus)


# 创建班级并加数据
@user_blueprint.route('/create_grade/', methods=['GET', 'POST'])
def create_grade():

    if request.method == 'GET':
        return render_template('create_grade.html')

    if request.method == 'POST':

        grade = Grade()
        grade.g_name = request.form.get('grade_name')
        grade.g_des = request.form.get('grade_des')

        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('user.grade_all'))


@user_blueprint.route('/grade_all/', methods=['GET', 'POST'])
def grade_all():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('create_grade.html', grades=grades)

    if request.method == 'POST':
        grade = Grade()
        grade.g_name = request.form.get('grade_name')
        grade.g_desc = request.form.get('grade_des')

        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('user.grade_all'))


# 添加学生通过班级
@user_blueprint.route('/create_stu_by_grade/', methods=['GET', 'POST'])
def create_stu_by_grade():

    if request.method == 'GET':
        g_id = request.args.get('g_id')
        return render_template('edit_stu.html', g_id=g_id)

    if request.method == 'POST':
        stu = Student()
        stu.s_name = request.form.get('stu_name')
        stu.s_age = request.form.get('stu_age')
        stu.grades = request.args.get('g_id')

        db.session.add(stu)
        db.session.commit()

        return render_template('edit_stu.html')


# 添加学生的课程
@user_blueprint.route('/add_course/<int:id>/', methods=['GET', 'POST'])
def add_course(id):

    if request.method == 'GET':
        courses = Course.query.all()
        # s_id = request.args.get(id)
        stu = Student.query.filter_by(s_id=id).first()
        s_courses = stu.course
        # s_courses = Course.query.filter_by(c_id=)
        return render_template('course.html', courses=courses, s_courses=s_courses, s_id=id)

    if request.method == 'POST':
        s_id = request.args.get('s_id')
        course_id = request.form.get('course_id')

        student = Student.query.get(s_id)
        g_id = student.grade.g_id
        course = Course.query.get(course_id)
        course.students.append(student)

        db.session.add(course)
        db.session.commit()

        return redirect(url_for('user.stus_list', g_id=g_id))


# 删除学生的课程
@user_blueprint.route('/delete_course/', methods=['GET', 'POST'])
def delete_course():
    if request.method == 'GET':
        s_id = request.args.get('s_id')
        c_id = request.args.get('c_id')

        # courses = Course.query.all()
        stu = Student.query.get(s_id)
        g_id = stu.grade.g_id
        s_courses = stu.course
        course = Course.query.filter_by(c_id=c_id).first()

        s_courses.remove(course)
        db.session.commit()
        return redirect(url_for('user.stus_list', g_id=g_id))


# 分页
@user_blueprint.route('/paginate/', methods=['GET', 'POST'])
def stu_paginate():
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = 5
        paginate = Student.query.order_by('s_id').paginate(page, page_num)
        stus = paginate.items
        return render_template('stu_paginate.html', stus=stus, paginate=paginate)


# 注册
@user_blueprint.route('/user_register/', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':

        username = request.form.get('user_name')
        pwd = request.form.get('pwd')
        cpwd = request.form.get('cpwd')
        email = request.form.get('email')

        if not all([username, pwd, cpwd, email]):
            msg = '请填写完整的注册信息'
            return render_template('register.html', msg=msg)

        if User.query.filter_by(username=username).first():
            msg = '该用户已经存在'
            return render_template('register.html', msg=msg)
        user = User(username, pwd)
        user.username = username
        user.password = cpwd
        user.email = email

        db.session.add(user)
        db.session.commit()
        return redirect('/user/user_login/')


# 登录
@user_blueprint.route('/user_login/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')

        if User.query.filter_by(username=username).first():
            if User.query.filter_by(password=pwd).first():
                user = User.query.filter_by(password=pwd).all()[0]
                session['user_id'] = user.id
                myres = redirect(url_for('user.stu_scores'))
                res = make_response(myres, 302)
                ticket = ''
                s = '1234567890qwertyuiopasdfgjuklzxcvbnm'
                for i in range(28):
                    a = random.choice(s)
                    ticket += a
                res.set_cookie('ticket', ticket, max_age=10)
                return res

            else:
                msg = '用户名或密码错误'
                return render_template('login.html', msg=msg)
        else:
            msg = '该用户没有注册，请前去注册'
            return render_template('login.html', msg=msg)


class CreateCourse(Resource):

    def get(self, id):
        courses = Course.query.all()
        # s_id = request.args.get(id)
        stu = Student.query.filter_by(s_id=id).first()
        s_courses = stu.course
        # s_courses = Course.query.filter_by(c_id=)
        # return render_template('course.html', courses=courses, s_courses=s_courses, s_id=id)
        return {
            'courses': [course.to_dict() for course in courses],
            's_courses': [s_course.to_dict() for s_course in s_courses]
        }

    def post(self):
        s_id = request.args.get('s_id')
        course_id = request.form.get('course_id')

        student = Student.query.get(s_id)
        g_id = student.grade.g_id
        course = Course.query.get(course_id)
        course.students.append(student)

        db.session.add(course)
        db.session.commit()

        # return redirect(url_for('user.stus_list', g_id=g_id))
        return {
            'g_id': g_id
        }

    def delete(self):
        pass


api.add_resource(CreateCourse, '/api/add_course/<int:id>/')
