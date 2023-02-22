from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Potion, potion_schema, potions_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Skyrim': 'Awesomeness'}

@api.route('/potions', methods = ['POST'])
@token_required
def create_potion(current_user_token):
    name = request.json['name']
    potion_class = request.json['potion_class']
    description = request.json['description']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    potion = Potion(name, potion_class, description, user_token=user_token)

    db.session.add(potion)
    db.session.commit()

    response = potion_schema.dump(potion)
    return jsonify(response)

@api.route('/potions', methods = ['GET'])
@token_required
def get_potion(current_user_token):
    a_user = current_user_token.token
    contacts = Potion.query.filter_by(user_token = a_user).all()
    response = potions_schema.dump(contacts)
    return jsonify(response)

#optional
'''
@api.route('/potions/<id>', methods = ['GET'])
@token_required
def update_potion(current_user_token, id):
    a_user = current_user_token.token
    if a_user:
        potion = Potion.query.get(id)
        response = potion_schema.dump(potion)
        return jsonify(response)
    else:
        return jsonify({'message': "shit didnt work"}), 401
'''

#update potion
@api.route('/potions/<id>', methods = ['POST', 'PUT'])
@token_required
def update_potion(current_user_token, id):
    potion = Potion.query.get(id)
    potion.name = request.json['name']
    potion.potion_class = request.json['potion_class']
    potion.description = request.json['description']
    potion.user_token = current_user_token.token

    db.session.commit()
    reponse = potion_schema.dump(potion)
    return jsonify(reponse)

#delete potion
@api.route('/potions/<id>', methods = ['DELETE'])
@token_required
def delete_potion(current_user_token, id):
    potion = Potion.query.get(id)
    db.session.delete(potion)
    db.session.commit()
    response = potion_schema.dump(potion)
    return jsonify(response)