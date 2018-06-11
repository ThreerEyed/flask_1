import os

from flask import Flask
from flask_session import Session

from user.stu_views import stu_blueprint
from user.user_views import user_blueprint


def create_app():
    # 指定静态目录和模板目录的文件位置
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    # 在初始化对象的时候，可以在参数中添加一些指定
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    # secret_key 秘钥
    # app.config['SECRET_KEY'] = 'secret_key'
    # # session 类型为redis
    # app.config['SESSION_TYPE'] = 'redis'
    # # 添加前缀
    # app.config['SESSION_KEY_PREFIX'] = 'flask'

    # 加载app的第一种方式
    # se = Session()
    # se.__init__(app=app)

    # 加载app的第二种方式
    # Session(app=app)
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=stu_blueprint, url_prefix='/stu')

    return app
