
from flask_restful import Api
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension

from App.models import db

toolbar = DebugToolbarExtension()
# api = Api()


def ext_init(app):

    app.debug = True
    db.init_app(app=app)
    Session(app)
    toolbar.init_app(app=app)
    # api.init_app(app=app)
