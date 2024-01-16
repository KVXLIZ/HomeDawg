from flask import Blueprint, request, jsonify, render_template, template_rendered
from . import db
from .models import Lights, Devices
import nmap
import json

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def show_home():
    light_entries = db.session.query(Lights).all()
    light_entries = [{
            'status': item.status, 
            'color': tuple([int(item.color[i:i+2], 16) for i in (1, 3, 5)] + [item.brightness]),
        } for item in light_entries]
    device_entries = db.session.query(Devices).all()
    device_entries = [{
        'name': item.name,
        'ip': item.ip,
        'status': "Connected" if item.status else "Disconnected"
    } for item in device_entries]
    return render_template('home.html', lights = light_entries, devices = device_entries) 

@home.route('/lights/add', methods=['POST'])
def add_light():
    data = request.get_json()
    for light in data['data']:
        new_entry = Lights(status = bool(light['status']), color = light['color'], brightness = light['brightness'])
        db.session.add(new_entry)
        db.session.commit()
    return f'Index {new_entry.id} added'

@home.route('/lights/remove', methods=['GET'])
def remove_light():
    id = request.args['id']
    Lights.query.filter(Lights.id == int(id)).delete()
    db.session.commit()
    return f'Index {id} removed'

# TODO: update the function so that you can update as many arguments as you want as long as you supply thre id
@home.route('/lights/status', methods=['POST'])
def light_status():
    r = ''
    data = request.get_json()
    for light in data['data']:
        Lights.query.filter(Lights.id == light['id']).update({
            'status': light['status'],
            'color': light['color'],
            'brightness': light['brightness']
        })
        db.session.commit()
        r +=  f'Index {light["id"]} status changed to {light["status"]}, {light["color"]}, {light["brightness"]}'
    return r

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
    nm.scan('192.168.32.0/24', arguments='-sn')
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
    new_device = Devices(ip=request_data['ip'], name=request_data['name'], status=request_data['status'])
    db.session.add(new_device)
    db.session.commit()
    return '200'
# TODO: device remove and device update
@home.route('/device/update', methods=['POST'])
def update_device():
    request_data = request.get_json()
    db.session.query(Devices).filter(Devices.ip == request_data["ip"]).update({
        'status': request_data['status']
    })
    db.session.commit()
    return '200'
    