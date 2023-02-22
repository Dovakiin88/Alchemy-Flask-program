from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

#set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#This calls for for people to create accounts
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default = '')
    #the 150 is the number of characters
    last_name = db.Column(db.String(150), nullable=True, default = '')
    email = db.Column(db.String(200), nullable=False)
    #nullable false means that they must have an email
    password = db.Column(db.String, nullable=True,default='')
    g_auth_verify = db.Column(db.Boolean, default= False)
    token = db.Column(db.String,default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

    def __init__(self, email, first_name= "", last_name= "", password= "", token="", g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created'

class Potion(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    potion_class = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, potion_class, description, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.potion_class = potion_class
        self.decription = description
        self.user_token =  user_token

    def __repr__(self):
        return f'{self.name} has been added to the database'

    def set_id(self):
        return (secrets.token_urlsafe())

class PotionSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'potion_class', 'description']

potion_schema = PotionSchema()
potions_schema = PotionSchema(many=True)