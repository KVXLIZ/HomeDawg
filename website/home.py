from flask import Blueprint, request, jsonify, render_template, url_for, current_app
from . import db
from .models import Lights, Devices
from dotenv import load_dotenv
import os
import nmap

load_dotenv()

secret = hash(os.getenv('SECRET_CODE'))

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def show_home():
    light_entries = db.session.query(Lights).all()
    light_entries = [{
            'status': item.status, 
            'color': tuple([int(item.color[i:i+2], 16) for i in (1, 3, 5)] + [item.brightness]),
        } for item in light_entries] # Query all the lights from the database and extract their status and color

    return render_template('home.html', lights = light_entries)


@home.route('/lights/add', methods=['POST'])
def add_light(): # Add a light to the database, works in json format, takes an array of light objects as an input. The light object contains: status, color, brightness
    ids = []
    data = request.get_json()
    for light in data['data']:
        new_entry = Lights(status = bool(light['status']), color = light['color'], brightness = light['brightness'])
        db.session.add(new_entry)
        db.session.commit()
        ids.append(new_entry.id)
    return f'Index {ids} added'

@home.route('/lights/remove', methods=['GET'])
# Remove a light from the database with a specified id
def remove_light(): 
    id = request.args['id']
    Lights.query.filter(Lights.id == int(id)).delete()
    db.session.commit()
    return f'Index {id} removed'

# TODO: update the function so that you can update as many arguments as you want as long as you supply thre id
@home.route('/lights/status', methods=['POST'])
# Update the status of the light. Takes an array of JSON format request. Array contains light objects, with light id, status, color and brightness.
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
        r +=  f'Index {light["id"]} status changed to {light["status"]}, {light["color"]}, {light["brightness"]}\n'
    return r

@home.route('/distance', methods=['POST'])
# Takes as input IP addresses of devices, for each IP address returns 1 if it is on the network, 0 otherwise.
def distance():
    request_data = request.get_json()
    nm = nmap.PortScanner()
    nm.scan('192.168.32.0/24', arguments='-sn')
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
# Returns 2 arrays containing up and down devices IPs and names that are registered in the database.
def connected_devices():
    devices = db.session.query(Devices).all()
    devices = [(item.ip, item.name) for item in devices]
    nm = nmap.PortScanner()
    nm.scan('192.168.0.0/24', arguments='-sn')
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
# Adds a device, as input takes a form that contains IP address of device as well as it's name and a secret.
def add_device():
    global secret
    request_data = request.form
    if hash(request_data['secret']) == secret:         
        new_device = Devices(ip=request_data['ip'], name=request_data['name'], status=False)
        db.session.add(new_device)
        db.session.commit()
        print("success")
    return show_home()

@home.route('/device/update', methods=['POST'])
# Updates the status of the device with specified IP address.
def update_device():
    request_data = request.get_json()
    db.session.query(Devices).filter(Devices.ip == request_data["ip"]).update({
        'status': request_data['status']
    })
    db.session.commit()
    return '200'

@home.route('/device/remove', methods = ['POST'])
# Removes the device with specified IP address.
def remove_device():
    global secret
    request_data = request.form
    if hash(request_data['secret']) == secret:
        db.session.query(Devices).filter(Devices.ip == request_data['ip']).delete()
        db.session.commit()
    return show_home()
    