from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "values.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'peterpiperpickedapickofpickledpeppers'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .cam import cam
    from .gas import gas
    from .lights import lights
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(cam, url_prefix='/surveilance')
    app.register_blueprint(gas, url_prefix='/')
    app.register_blueprint(lights, url_prefix='/lights')
    
    from .models import Air, Cam, Dist
    
    with app.app_context():
        db.create_all()
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
    
    