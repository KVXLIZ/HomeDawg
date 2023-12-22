from flask import Blueprint, Response, request, render_template
from . import db
from .models import Cam
import numpy as np
from PIL import Image
from os import remove, mkdir
import cv2
import glob
from time import sleep

cam = Blueprint('cam', __name__)    
        
pic_ID = 0

@cam.route('/', methods = ['GET'])
def root():
    if request.args.get('feed') is not None:
        feed = request.args.get('feed')
    else:
        elements = db.session.query(Cam).all()
        if elements == None:
            feed = 0
        else:
            feed = len(elements)
            print(len(elements))
    return render_template('surveilance.html', rng=int(feed))

@cam.route('/data/get', methods=['GET'])
def feed():
    if request.args.get('num') is not None:
        folder = request.args.get('num')
    else:
        folder = db.session.query(Cam).order_by(Cam.id.desc()).first().id
    def generate_frames():
        imgs = [cv2.imread(file) for file in glob.glob(f"/home/pi/HomeDawg/website/static/cam{folder}/*.jpg")]
        imgs = [cv2.resize(img, (320, 240), fx = 0.5, fy = 0.5) for img in imgs]
        frames = [cv2.imencode('.jpg', img)[1].tobytes() for img in imgs]
        while True:
            for frame in frames :
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                sleep(1) 
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@cam.route('/newround', methods=['GET'])
def newround():
    global pic_ID
    pic_ID = 0
    element = Cam()
    db.session.add(element)
    db.session.commit()
    mkdir(f'/home/pi/HomeDawg/website/static/cam{element.id}')
    return '200'


@cam.route('/data/add', methods=['GET', 'POST'])
def data():
    global pic_ID
    if request.method == 'POST':
        folder = db.session.query(Cam).order_by(Cam.id.desc()).first().id
        width = 160
        height = 120
        buf = bytearray(2 * width * height)
        row = np.empty((width), int)
        buf = request.data
        filename = '/home/pi/HomeDawg/website/static/pics/pic.ppm'
        file = open(filename, 'w')
        file.write(f'P3 {width} {height} 255\n')
        file.close()
        
        with open(filename, 'a') as f:
            for j in range(height):
                for i in range(width):
                    row[i] = int(buf[2*(width*j+i)])
                    row[i] = (row[i] -255)*-1
                for e in row:
                    f.write(str(e)+' ')
                    f.write(str(e)+' ')
                    f.write(str(e)+'\n')
        
        im = Image.open('/home/pi/HomeDawg/website/static/pics/pic.ppm')
        remove('/home/pi/HomeDawg/website/static/pics/pic.ppm')
        im.save(f'/home/pi/HomeDawg/website/static/cam{folder}/pic{pic_ID}.jpg')
        pic_ID+=1
        return '200'
    elif request.method == 'GET':
        if request.args.get('secret') == 'balls':
            Cam.query.delete()
            db.session.commit()
        return request.args.get('secret')