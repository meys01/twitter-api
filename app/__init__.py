from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/hello')
    def hello():
        return "Goodbye World!"

    from .apis.tweets import api as tweets
    from .apis.users import api as users
    api = Api()
    api.add_namespace(tweets, path='/tweets')
    api.add_namespace(users, path='/users')
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
