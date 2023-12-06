from flask import Blueprint, render_template
from .models import Air, Cam, Dist

views = Blueprint('views', __name__)

@views.route('/')
def home():
    obj = Air.query.order_by(Air.id.desc()).first()
    #pic_ID = Cam.query.order_by(Cam.id.desc()).first().id
    #dt = Dist.query.order_by(Dist.id.desc()).first().dist
    return render_template("index.html")
