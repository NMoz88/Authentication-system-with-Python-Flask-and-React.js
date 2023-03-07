"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Diccionario, Me_gusta
#from models import Person
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/diccionario', methods=['POST'])
def traductor(): 
    body = request.get_json()
    if "tipo_situacion" not in body:
        return "falta situacion"
    if "url_img" not in body:
        return "falta url"


    diccionariob = Diccionario.query.filter_by(tipo_situacion = body['tipo_situacion'],url_img=body['url_img']).first()
    if(diccionariob):
       
        #mensaje de estado
        return jsonify({
            "url": "se ingresaron los datos"
        })
    else:
        return "datos incorrectos"

@app.route('/diccionario', methods=['GET'])
def traductor2(): 
    url = get_jwt_identity()
    return identidad 

@app.route('/register', methods=['POST'])
def register():
    print("gdfjklghdfklfgjn")
    body = request.get_json()
    email = body['email']
    password = body['password']
    fullname = body['fullname']
    address1 = body['address1']
    address2 = body['address2']
    city = body['city']
    state = body['state']
    npostal = body['npostal']

    user2 = User(email = body['email'],password=body['password'], fullname=body['fullname'], address1=body['address1'], address2=body['address2'], city=body['city'], state=body['state'], npostal=body['npostal'])
    db.session.add(user2)
    db.session.commit()
    
    return jsonify({'email':email,'password':password, 'fullname':fullname, 'address1':address1, 'address2':address2, 'city':city, 'state':state, 'npostal':npostal})



@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if "email" not in body:
        return "falta email"
    if "password" not in body:
        return "falta password"


    user = User.query.filter_by(email = body['email'],password=body['password']).first()
    if(user):
        #otorgar permisos
        expira = datetime.timedelta(minutes=1)
        access = create_access_token(identity=body,
        expires_delta=expira)
        #mensaje de estado
        return jsonify({
            "token":access
        })
    else:
        return "datos incorrectos"

@app.route("/private", methods=['GET'])
@jwt_required()
def privada():
    identidad = get_jwt_identity()
    return identidad 



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
