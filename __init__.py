from flask import Flask
from config import Config
from models import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

    return app
