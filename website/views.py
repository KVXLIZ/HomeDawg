from flask import Blueprint, render_template, redirect, url_for
import socket

views = Blueprint('views', __name__)

started = False

@views.route('/')
def home():
    global started
    return render_template("index.html", btn_started=started)

@views.route('/button')
def button():
    global started
    if not started:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('192.168.1.30', 5001))
        sock.sendall(b'start')
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('192.168.1.30', 5001))
        sock.sendall(b'finis')
    started = not started
    return redirect(url_for('views.home'))
