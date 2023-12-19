from flask import Blueprint, request, flash, jsonify, render_template
from . import db
from .models import Lights
import requests

lights = Blueprint('lights', __name__)

@lights.route('/', methods=['GET'])
def show_lights():
    data = db.session.query(Lights).all()[-1::]
    return render_template('lights.html', on_off=str(data[0].status)) 

@lights.route('/status', methods=['GET'])
def light():
    status = request.args.get('status')
    new_data = Lights(status = status)
    db.session.add(new_data)
    db.session.commit()
    return '200'

@lights.route('/data', methods=['GET'])
def get_data():
    data = db.session.query(Lights).all()
    result = [{'id': str(item.id), 'status': str(item.status)} for item in data[-5::]]
    return jsonify(result) 