from flask import Blueprint, render_template, redirect, url_for
import socket

views = Blueprint('views', __name__)

started = False

@views.route('/')
def home():
    global started
    return render_template("index.html", dawg=True)

