from flask import Flask
from .config import Config
from flask_cors import CORS

def create_app(config_c=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from .models import db
    db.init_app(app)

    from app import auth, reftablesinit, actualtotalload, aggregatedgenerationpertype, dayaheadtotalloadforecast, \
        actualvsforecast
    app.register_blueprint(auth.bp)
    app.register_blueprint(reftablesinit.bp)
    app.register_blueprint(actualtotalload.bp)
    app.register_blueprint(aggregatedgenerationpertype.bp)
    app.register_blueprint(dayaheadtotalloadforecast.bp)
    app.register_blueprint(actualvsforecast.bp)
    CORS(app)
    return app
