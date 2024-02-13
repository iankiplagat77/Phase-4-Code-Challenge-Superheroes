#!/usr/bin/env python3

from flask import Flask, make_response, jsonify ,request
from flask_migrate import Migrate

from models import db, Hero,Power,Hero_Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'This is the home screen'
@app.route('/heroes' ,methods=['GET'])
def get():
    heroes=Hero.query.all()
    heroes_to_dict=[hero.to_dict() for hero in heroes]
    return make_response(jsonify(heroes_to_dict),200)

@app.route('/heroes/<int:id>')
def getByIdHeroes(id):
    hero=Hero.query.filter_by(id=id).first()
    if (hero == None):
        raise ValueError('Hero not found')
    hero_to_dict=hero.to_dict()
    return make_response(jsonify(hero_to_dict),200)
@app.route('/power',methods=['GET'])
def getPowers():
    powers=Power.query.all()
    powers_to_dict = [power.to_dict() for power in powers]
    return make_response(jsonify(powers_to_dict),200)

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def getByIdPowers(id):
    if request.method == 'GET':
        power = Power.query.filter_by(id=id).first()
        if (power == None):
            raise ValueError('Power not found')
        power_to_dict2=power.to_dict()
        response = jsonify(power_to_dict2)
        return make_response(response, 200) 
    elif request.method == 'PATCH':
        power=Power.query.filter_by(id=id).first()
        if (power == None):
            raise ValueError('Power not found')
        try:
            for attribute in request.json:
                setattr(power, attribute, request.json[attribute])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': [str(e)]}), 400)

        power_to_dict3 = power.to_dict()
        response = jsonify(power_to_dict3)
        return make_response(response, 200)

@app.route('/hero_powers', methods=['POST'])
def post():
    if request.method == 'POST':
        new_hero_power = Hero_Power(
            power_id=request.json.get("power_id"),
            hero_id=request.json.get('hero_id'),
            strength=request.json.get('strength')
            )
        try:
            db.session.add(new_hero_power)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'errors': [str(e)]}), 400)
        new_hero_power_to_dict = new_hero_power.to_dict()
        response = jsonify(new_hero_power_to_dict)
        return make_response(response, 200)



if __name__ == '__main__':

    app.run(port=5555)  
    