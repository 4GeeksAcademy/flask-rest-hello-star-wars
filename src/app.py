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
from models import db, User, Personajes, Planetas, Favoritos
#from models import Person

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


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email} for u in users]), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    personajes = Personajes.query.all()
    return jsonify([p.serialize() for p in personajes]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    personaje = Personajes.query.get(people_id)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200

@app.route('/planeta', methods=['GET'])
def get_all_planetas():
    planetas = Planetas.query.all()
    return jsonify([p.serialize() for p in planetas]), 200

@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_one_planets(planetas_id):
    planetas = Planetas.query.get(planetas_id)
    if not planetas:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(planetas.serialize()), 200

@app.route('/users/favoritos', methods=['GET'])
def get_user_favoritos():
    user = User.query.first()  
    favoritos = Favoritos.query.filter_by(user_id=user.id).all()
    return jsonify([f.serialize() for f in favoritos]), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
