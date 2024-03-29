from . import db
from sqlalchemy.sql import func

class Air(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.Integer)
    tag = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Cam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Lights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    color = db.Column(db.String(7))
    brightness = db.Column(db.Float)
    
class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Boolean)