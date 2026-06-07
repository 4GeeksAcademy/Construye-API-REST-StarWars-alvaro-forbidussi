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
from models import db, Usuario, Personaje, Planeta, Favorito
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

# ==============================
# ENPOINTS DE PERSONAJES (PEOPLE)
# ==============================

@app.route('/people', methods=['GET'])
def get_people():
    personajes = Personaje.query.all()
    personajes_serializados = [personaje.serialize() for personaje in personajes]
    return jsonify(personajes_serializados), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personaje.query.get(people_id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200

@app.route('/people', methods=['POST'])
def create_personaje():
    body = request.json
    if not body or 'nombre' not in body:
        return jsonify({"msg": "El campo 'nombre' es requerido"}), 400
    
    nuevo_personaje = Personaje(
        nombre=body.get('nombre'),
        ano_de_nacimiento=body.get('ano_de_nacimiento'),
        genero=body.get('genero'),
        altura=body.get('altura'),
        color_de_cabello=body.get('color_de_cabello'),
        color_de_ojos=body.get('color_de_ojos')
    )
    db.session.add(nuevo_personaje)
    db.session.commit()
    return jsonify(nuevo_personaje.serialize()), 201

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_personaje(people_id):
    personaje = Personaje.query.get(people_id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    
    body = request.json
    if 'nombre' in body:
        personaje.nombre = body['nombre']
    if 'ano_de_nacimiento' in body:
        personaje.ano_de_nacimiento = body['ano_de_nacimiento']
    if 'genero' in body:
        personaje.genero = body['genero']
    if 'altura' in body:
        personaje.altura = body['altura']
    if 'color_de_cabello' in body:
        personaje.color_de_cabello = body['color_de_cabello']
    if 'color_de_ojos' in body:
        personaje.color_de_ojos = body['color_de_ojos']
        
    db.session.commit()
    return jsonify(personaje.serialize()), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_personaje(people_id):
    personaje = Personaje.query.get(people_id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    
    # Eliminar favoritos asociados primero
    Favorito.query.filter_by(personaje_id=people_id).delete()
    
    db.session.delete(personaje)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado con éxito"}), 200

# ==============================
# ENPOINTS DE PLANETAS (PLANETS)
# ==============================

@app.route('/planets', methods=['GET'])
def get_planets():
    planetas = Planeta.query.all()
    planetas_serializados = [planeta.serialize() for planeta in planetas]
    return jsonify(planetas_serializados), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200

@app.route('/planets', methods=['POST'])
def create_planeta():
    body = request.json
    if not body or 'nombre' not in body:
        return jsonify({"msg": "El campo 'nombre' es requerido"}), 400
    
    nuevo_planeta = Planeta(
        nombre=body.get('nombre'),
        clima=body.get('clima'),
        poblacion=body.get('poblacion'),
        periodo_orbital=body.get('periodo_orbital'),
        periodo_de_rotacion=body.get('periodo_de_rotacion'),
        diametro=body.get('diametro')
    )
    db.session.add(nuevo_planeta)
    db.session.commit()
    return jsonify(nuevo_planeta.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planeta(planet_id):
    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    
    body = request.json
    if 'nombre' in body:
        planeta.nombre = body['nombre']
    if 'clima' in body:
        planeta.clima = body['clima']
    if 'poblacion' in body:
        planeta.poblacion = body['poblacion']
    if 'periodo_orbital' in body:
        planeta.periodo_orbital = body['periodo_orbital']
    if 'periodo_de_rotacion' in body:
        planeta.periodo_de_rotacion = body['periodo_de_rotacion']
    if 'diametro' in body:
        planeta.diametro = body['diametro']
        
    db.session.commit()
    return jsonify(planeta.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planeta(planet_id):
    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    
    # Eliminar favoritos asociados
    Favorito.query.filter_by(planeta_id=planet_id).delete()
    
    db.session.delete(planeta)
    db.session.commit()
    return jsonify({"msg": "Planeta eliminado con éxito"}), 200

# ==============================
# ENPOINTS DE USUARIOS
# ==============================

@app.route('/users', methods=['GET'])
def get_users():
    usuarios = Usuario.query.all()
    usuarios_serializados = [usuario.serialize() for usuario in usuarios]
    return jsonify(usuarios_serializados), 200

# ==============================
# ENPOINTS DE FAVORITOS
# ==============================

# Obtenemos el ID del usuario actual de manera estática ya que no hay autenticación
CURRENT_USER_ID = 1

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Comprobar si el usuario existe
    usuario = Usuario.query.get(CURRENT_USER_ID)
    if not usuario:
        return jsonify({"msg": "Usuario actual no encontrado (ID: 1). Por favor, crea uno en el admin."}), 404
        
    favoritos = Favorito.query.filter_by(usuario_id=CURRENT_USER_ID).all()
    favoritos_serializados = [favorito.serialize() for favorito in favoritos]
    return jsonify(favoritos_serializados), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no encontrado"}), 404
        
    usuario = Usuario.query.get(CURRENT_USER_ID)
    if not usuario:
        return jsonify({"msg": "Usuario actual no encontrado (ID: 1). Por favor, crea uno en el admin."}), 404
        
    # Validar que no exista ya
    favorito_existente = Favorito.query.filter_by(usuario_id=CURRENT_USER_ID, planeta_id=planet_id).first()
    if favorito_existente:
        return jsonify({"msg": "El planeta ya está en favoritos"}), 400
        
    nuevo_favorito = Favorito(usuario_id=CURRENT_USER_ID, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify(nuevo_favorito.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    personaje = Personaje.query.get(people_id)
    if not personaje:
        return jsonify({"msg": "Personaje no encontrado"}), 404
        
    usuario = Usuario.query.get(CURRENT_USER_ID)
    if not usuario:
        return jsonify({"msg": "Usuario actual no encontrado (ID: 1). Por favor, crea uno en el admin."}), 404
        
    # Validar que no exista ya
    favorito_existente = Favorito.query.filter_by(usuario_id=CURRENT_USER_ID, personaje_id=people_id).first()
    if favorito_existente:
        return jsonify({"msg": "El personaje ya está en favoritos"}), 400
        
    nuevo_favorito = Favorito(usuario_id=CURRENT_USER_ID, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify(nuevo_favorito.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorito = Favorito.query.filter_by(usuario_id=CURRENT_USER_ID, planeta_id=planet_id).first()
    if not favorito:
        return jsonify({"msg": "Planeta favorito no encontrado para este usuario"}), 404
        
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Planeta favorito eliminado con éxito"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorito = Favorito.query.filter_by(usuario_id=CURRENT_USER_ID, personaje_id=people_id).first()
    if not favorito:
        return jsonify({"msg": "Personaje favorito no encontrado para este usuario"}), 404
        
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"msg": "Personaje favorito eliminado con éxito"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
