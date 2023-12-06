from flask import Blueprint, Response, request, jsonify
from . import db
from .models import Cam
import numpy as np
from PIL import Image
from os import remove
import cv2
import glob
from time import sleep

cam = Blueprint('cam', __name__)    
        

@cam.route('/')
def surveilance():
    def generate_frames():
        imgs = [cv2.imread(file) for file in glob.glob("HomeDawg/website/static/pics/*.jpg")]
        imgs = [cv2.resize(img, (320, 240), fx = 0.5, fy = 0.5) for img in imgs]
        frames = [cv2.imencode('.jpg', img)[1].tobytes() for img in imgs]
        while True:
            for frame in frames :
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                sleep(1) 
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@cam.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        element = Cam()
        db.session.add(element)
        db.session.commit()
        pic_ID = element.id
        width = 160
        height = 120
        buf = bytearray(2 * width * height)
        row = np.empty((width), int)
        buf = request.data
        filename = 'HomeDawg/website/static/pics/pic{}.ppm'.format(pic_ID)
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
        
        im = Image.open(f'HomeDawg/website/static/pics/pic{pic_ID}.ppm')
        remove(f'HomeDawg/website/static/pics/pic{pic_ID}.ppm')
        im.save(f'HomeDawg/website/static/pics/pic{pic_ID}.jpg')
        return '200'
    elif request.method == 'GET':
        if request.args.get('secret') == 'balls':
            Cam.query.delete()
            db.session.commit()
        return request.args.get('secret')