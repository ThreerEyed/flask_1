from flask_restful import Api
from flask_session import Session

from user.models import db

api = Api()


def ext_init(app):

    se = Session()
    se.init_app(app=app)
    db.init_app(app=app)
    api.init_app(app)
