from flask import Blueprint, request, jsonify, render_template, template_rendered
from . import db
from .models import Lights, Devices
import nmap

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def show_home():
    entries = db.session.query(Lights).all()[-2::]
    return render_template('home.html', first_light = entries[0], second_light=entries[1]) 

@home.route('lights/status', methods=['POST'])
def light():
    print("Yes")
    if request.method == 'POST':
        data = request.get_json(force=True)
        for light in data :
            new_entry = Lights(status = bool(light['status']), color = light['color'], brightness = light['brightness'])
            db.session.add(new_entry)
            db.session.commit()
    return '200'     

@home.route('lights/data', methods=['GET'])
def get_data():
    data = db.session.query(Lights).all()
    result = [{'status':item.status, 'color': item.color, 'brightness': item.brightness} for item in data[-4::]]
    return jsonify(result)  

@home.route('/distance', methods=['POST'])
def distance():
    request_data = request.get_json()
    nm = nmap.PortScanner()
    nm.scan('192.168.1.0/24', arguments='-sn')
    hosts = nm.all_hosts()
    devices = request_data['devices']
    response = []
    for dev in devices:
        if dev in hosts:
            response.append(1)
        else:
            response.append(0)
    return jsonify(response)

@home.route('/connected', methods=['GET'])
def connected_devices():
    devices = db.session.query(Devices).all()
    devices = [(item.ip, item.name) for item in devices]
    nm = nmap.PortScanner()
    nm.scan('192.168.1.0/24', arguments='-sn')
    on = []
    off = []
    hosts = nm.all_hosts()
    for d in devices:
        if d[0] in hosts:
            on.append(d)
        else:
            off.append(d)
    return jsonify(up=on, down=off)

@home.route('/device/add', methods=['POST'])
def add_device():
    request_data = request.get_json()
    if request_data['secret'] == 'dawginhere':
        new_device = Devices(ip=request_data['ip'], name=request_data['name'])
        db.session.add(new_device)
        db.session.commit()
        return '200'
    return '500'
    