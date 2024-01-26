from flask import Blueprint, Response, request, render_template
from . import db
from .models import Cam
import numpy as np
from PIL import Image
from os import remove, mkdir
import cv2
from datetime import datetime
import glob
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

secret = hash(os.getenv('SECRET_CODE')) # Get the password from environment file and hash it

cam = Blueprint('cam', __name__)    
        
pic_ID = 0

@cam.route('/', methods = ['GET'])
def root():
    feed = 0
    if request.args.get('feed') is not None:
        feed = request.args.get('feed')
    elements = [{'id': item.id, 'date': item.date.strftime('%x %X')} for item in db.session.query(Cam).all()]
    return render_template('surveilance.html', rng=elements, feed_id=int(feed))

@cam.route('/data/get', methods=['GET'])
# Returns a folder of pictures as a byte stream.
def feed():
    if request.args.get('num') is not None:
        folder = request.args.get('num')
    else:
        folder = db.session.query(Cam).order_by(Cam.id.desc()).first().id
    def generate_frames():
        imgs = [cv2.imread(file) for file in glob.glob(f"website/static/cam{folder}/*.jpg")]
        imgs = [cv2.resize(img, (320, 240), fx = 0.5, fy = 0.5) for img in imgs]
        frames = [cv2.imencode('.jpg', img)[1].tobytes() for img in imgs]
        while True:
            for frame in frames :
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                sleep(1) 
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@cam.route('/newround', methods=['GET'])
# Starts a new feed and saves it's date.
def newround():
    global pic_ID
    pic_ID = 0
    element = Cam()
    db.session.add(element)
    db.session.commit()
    mkdir(f'website/static/cam{element.id}')
    return '200'


@cam.route('/data/add', methods=['POST'])
# Receive a picture in bytes, convert it to a jpg and save it.
def data():
    global pic_ID, secret
    if request.method == 'POST':
        folder = db.session.query(Cam).order_by(Cam.id.desc()).first().id
        width = 160
        height = 120
        buf = bytearray(2 * width * height)
        row = np.empty((width), int)
        buf = request.data
        filename = 'website/static/pics/pic.ppm'
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