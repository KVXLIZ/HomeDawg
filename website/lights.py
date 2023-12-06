from flask import Blueprint, render_template

lights = Blueprint('lights', __name__)

@lights.route('/', methods=['GET'])
def light():
    return render_template('lights.html')
