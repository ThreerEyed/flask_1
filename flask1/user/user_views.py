
from flask import render_template, Blueprint, request, make_response, redirect, url_for

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello_word():
    # 3/0
    return 'GOOD'


@user_blueprint.route('/hellohtml/')
def hello_html():
    return render_template('hello.html')


# 可以指定url参数，string 可以加也可以不加默认有string
@user_blueprint.route('/helloname/<string:name>/')
def hello_person(name):
    return render_template('hello.html', name=name)


# 指定后面的路径
@user_blueprint.route('/hellopath/<path:path>/')
def hello_path(path):
    return render_template('hello.html', path=path)


# 可以指定参数的类型
@user_blueprint.route('/helloint/<int:id>/')
def hello_int(id):
    return render_template('hello.html', id=id)


# 可以产生一个随机的字符串，有唯一性，类似于ticket
@user_blueprint.route('/hellouuid/<uuid:uuid>')
def hello_uuid(uuid):
    return render_template('hello.html', uuid=uuid)


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('hello.html')
    if request.method == 'POST':
        username = request.form.get('username')
        return username


@user_blueprint.route('user_res', methods=['GET', 'POST'])
def get_user_response():
    res = make_response('<h2>大大萌妹</h2>', 200)
    return res


# 重定向
@user_blueprint.route('redirect')
def user_redirect():
    # return redirect('/user/login/')
    return redirect(url_for('user.hello_word'))
