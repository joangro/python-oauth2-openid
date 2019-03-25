from flask import current_app, Flask
from flask_bootstrap import Bootstrap
import os

def create_app():
    app = Flask(__name__)
    
    Bootstrap(app)

    app.secret_key = os.environ('APP_SECRET_ID')
    
    from .oauth import bp
    app.register_blueprint(bp)

    return app
