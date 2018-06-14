from flask import Blueprint, request, render_template, redirect, url_for, session

from App.models import db, User
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

        if User.query.filter_by(u_name=username):
            if User.query.filter_by(u_pass=password):
                user = User.query.filter_by(u_name=username).first()
                session['user_id'] = user.u_id
                return render_template('index.html')
            else:
                msg = '用户名或密码错误'
                return render_template('login.html', msg=msg)
        else:
            msg = '用户名或密码错误'
            return render_template('login.html', msg=msg)


@user_blueprint.route('/index/', methods=['GET', 'POST'])
@is_login
def index():
    if request.method == 'GET':

        return render_template('index.html')


@user_blueprint.route('/head/', methods=['GET', 'POST'])
def head():
    if request.method == 'GET':
        return render_template('head.html')


@user_blueprint.route('/left/', methods=['GET', 'POST'])
def left():
    if request.method == 'GET':
        return render_template('left.html')


@user_blueprint.route('/grade/', methods=['GET', 'POST'])
def grade():
    if request.method == 'GET':
        return render_template('grade.html')