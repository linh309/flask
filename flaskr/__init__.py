import os

from flask import Flask

"""
    1. Create Flask application object
    2. Load configuration
    3. Make sure the instance folder is existed
"""

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqllite')
    )

    if test_config is None:
        #load instance config from file
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config from arguments
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize application's database 
    from . import db
    db.init_app_db(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route("/hello")
    def hello():
        return "Hello FLASK"

    return app