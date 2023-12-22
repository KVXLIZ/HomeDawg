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

class Dist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dist = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Lights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    
class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15))
    name = db.Column(db.String(20))