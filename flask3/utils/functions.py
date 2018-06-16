import os

import redis
from flask import Flask

from App.views import user_blueprint
from utils.ext_init import ext_init


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir,
                )
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SECRET_KEY'] = '\x03\xe8\x97\xdb\x17<\xb7n\x94\xee\xdb\xa4\xfa\xeb\x93'  # os.urandom(20)
    app.config['SESSION_SECRET_KEY'] = 'secret'
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    ext_init(app)
    return app


