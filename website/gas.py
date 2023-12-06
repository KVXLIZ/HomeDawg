from flask import Blueprint, request, flash
from .models import Air, Dist
from . import db

gas = Blueprint('gas', __name__)

@gas.route('/gas_sense', methods=['GET'])
def gas_sense():
    if request.method == 'GET':
        if request.args.get('aq') == None:
            entry = db.session.query(Air).order_by(Air.id.desc()).first()
        if request.args.get('tag') == '1':
            return entry.tag;
        if request.args.get('qual') == '1':
            return str(entry.quality);
        air_quality = int(request.args.get('aq'))
        if air_quality>5500:
            air_quality_name = 'HAZARDOUS'
        elif air_quality>3300:
            air_quality_name = 'EXTREMELY UNHEALTHY'
        elif air_quality>2200:
            air_quality_name = 'VERY UNHEALTHY'
        elif air_quality>1430:
            air_quality_name = 'UNHEALTHY'
        elif air_quality>660:
            air_quality_name = 'BAD'
        elif air_quality>220:
            air_quality_name = 'MODERATE'
        else:
            air_quality_name = 'GOOD'
        new_data = Air(quality=air_quality, tag=air_quality_name)
        db.session.add(new_data)
        db.session.commit()
        flash(f'Data sent: {air_quality}', category='success')
        return '200'
    
@gas.route('/proximity', methods=['GET'])
def proximity():
    if request.method == 'GET':
        new_data = Dist(dist = int(request.args.get('dt')))
        db.session.add(new_data)
        db.session.commit()
    return request.args.get('dt')
        
