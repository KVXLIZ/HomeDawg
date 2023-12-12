from flask import Blueprint, render_template, redirect, url_for
import requests
import socket
from .models import Air, Cam, Dist

views = Blueprint('views', __name__)

@views.route('/')
def home():
    obj = Air.query.order_by(Air.id.desc()).first()
    #pic_ID = Cam.query.order_by(Cam.id.desc()).first().id
    #dt = Dist.query.order_by(Dist.id.desc()).first().dist
    return render_template("index.html")

@views.route('/button')
def button():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('192.168.1.30', '5001'))
    sock.sendall('4')
    return redirect(url_for('/'))
