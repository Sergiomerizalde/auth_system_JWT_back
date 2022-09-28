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
from models import db, User, Planets, People
#from models import Person
#importación JWT inicio
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "clavesecreta"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if current_user != user.email:
        return jsonify({"msg": "Bad email or password"}), 401
    return jsonify(user.serialize), 200


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets= Planets.query.all()

    results = list(map(lambda item: item.serialize(),planets))

    response_body = {
        "msg":"Todo creado con exito",
        "results": results
    }

    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    print(planet.serialize()) #<Planet 1>
    # results = list(map(lambda item: item.serialize(),planets))

    response_body = {
        "msg":"Todo creado con exito",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people= People.query.all()

    results = list(map(lambda item: item.serialize(),people))

    response_body = {
        "msg":"Todo creado con exito",
        "results": results
    }

    return jsonify(results), 200

# @app.route('/people/<int:planet_id>', methods=['GET'])
# def get_one_people(people_id):
#     people = People.query.filter_by(id=people_id).first()
#     print(people.serialize()) #<Planet 1>
#     # results = list(map(lambda item: item.serialize(),planets))

#     response_body = {
#         "msg":"Todo creado con exito",
#         "people": people.serialize()
#     }

#     return jsonify(response_body), 200

if __name__ == "__main__":
    app.run()

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)