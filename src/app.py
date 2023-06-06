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
from models import db, User, People, Planets, FavPlanets, FavPeople
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


# /////////////////////////////////  ENDPOINTS. GET /////////////////////////////////////////////////
@app.route('/people', methods=['GET'])
def getPeople():

    people = People.query.all()
    if not people:
        return "ERROR"
    
    people = list(map(lambda x: x.serialize(), people))
    response = people
    return jsonify(response)


@app.route('/planets', methods=['GET'])
def getPlanets():

    planets = Planets.query.all()
    if not planets:
        return "ERROR"
    
    planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(planets)


@app.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    if not users:
        return "ERROR"

    users = list(map(lambda user : user.serialize(), users))

    response_body = {
        "data": users
    }

    return jsonify(response_body)


@app.route('/favorite/planet', methods=['GET'])
def getFavPlanets():
    getFav = FavPlanets.query.all()

    getFav = list(map(lambda x : x.serialize(), getFav))

    response_body = {
        "data": getFav
    }

    return jsonify(response_body)

@app.route('/favorite/people', methods=['GET'])
def getFavPeople():
    getFav = FavPeople.query.all()

    getFav = list(map(lambda x : x.serialize(), getFav))

    response_body = {
        "data": getFav
    }

    return jsonify(response_body)

@app.route('/users/favorites', methods=['GET'])
def getFav():
    favoritePeople = []
    favoritePlanet = []

    #getFav = User.query.all()
    getPeople = FavPeople.query.all()
    getPlanets = FavPlanets.query.all()
    print(getFav)

    for character in getPeople:
        favoritePeople.append(character.serialize())

    for planet in getPlanets:
        favoritePlanet.append(planet.serialize())

    #getFav = list(map(lambda x : x.serialize(), getFav))
    #getPeople = list(map(lambda x : x.serialize(), getPeople))
    #getPlanets = list(map(lambda x : x.serialize(), getPlanets))

    response_body = {

        "Favorite_People": favoritePeople,
        "Favorite_Planets": favoritePlanet
    }

    return jsonify(response_body)





# ////////////////////// Consultas a 1 único item ////////////////////////////

@app.route('/people/<int:people_id>', methods=['GET'])
def getPerson(people_id):
    person = People.query.filter_by(id = people_id).first()

    response_body = {
        "data": person.serialize()
    }

    return jsonify(response_body)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    planet = Planets.query.filter_by(id = planet_id).first()

    response_body = {
        "data": planet.serialize()
    }

    return jsonify(response_body)


@app.route('/users/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = User.query.filter_by(id = user_id).first()

    response_body = {
        "data": user.serialize()
    }

    return jsonify(response_body)

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def getUserFavorites(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    favorite_people = FavPeople.query.filter_by(user_id=user_id).all()
    favorite_planets = FavPlanets.query.filter_by(user_id=user_id).all()

    serialized_people = []
    for person in favorite_people:
        serialized_people.append(person.serialize())

    serialized_planets = []
    for planet in favorite_planets:
        serialized_planets.append(planet.serialize())

    response_body = {
        "user_id": user_id,
        "favorite_people": serialized_people,
        "favorite_planets": serialized_planets
    }

    return jsonify({"message": response_body}), 200





@app.route('/favorite/planet/<int:planet_id>', methods=['GET'])
def getOnePlanet(planet_id):
    favPlanet = FavPlanets.query.filter_by(id = planet_id).first()

    response_body = {
        "data": favPlanet.serialize()
    }

    return jsonify(response_body)

@app.route('/favorite/people/<int:people_id>', methods=['GET'])
def getOnePeople(people_id):
    favPeople = FavPeople.query.filter_by(id = people_id).first()

    response_body = {
        "data": favPeople.serialize()
    }

    return jsonify({"message": response_body})






# ///////////////////////////// POST /////////////////////////////////////
@app.route('/users', methods=['POST'])
def addUser():

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Completa los campos requeridos"}), 400
    
    saving_user = User(email=email, password=password, is_active=True)
    db.session.add(saving_user)
    db.session.commit()
    
    return jsonify("Usuario creado con éxito"), 201


@app.route('/favorite/planet', methods=['POST'])
def favPlanet():
    data = request.json
    userID = data.get('user_id')
    planetID = data.get('planet_id')
    
    if not userID or not planetID:
        return jsonify({"message": "Completa los campos requeridos."}), 400
    
    addFav = FavPlanets(user_id=userID, planet_id=planetID)
    db.session.add(addFav)
    db.session.commit()

    return jsonify({"message": "Planeta agregado a favoritos con éxito."}), 201


@app.route('/favorite/people', methods=['POST'])
def favPeople():
    data = request.json
    userID = data.get('user_id')
    peopleID = data.get('people_id')

    if not userID or not peopleID:
        return jsonify({"message": "Completa los campos requeridos."}), 400
    
    addFav = FavPeople(user_id = userID, people_id = peopleID)
    db.session.add(addFav)
    db.session.commit()

    return jsonify({"message": "Personaje agregado a favoritos con éxito."})



# ///////////////////////////   DELETE  ////////////////////////////////
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def deletePeople(people_id):

    delete_people = FavPeople.query.get(people_id)
   
    if delete_people is None:
        return jsonify("No existe"), 404
    
    db.session.delete(delete_people)
    db.session.commit()

    return jsonify("The planet has been deleted successfully"), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id):

    delete_planet = FavPlanets.query.get(planet_id)

    if delete_planet is None:
        return jsonify("No existe"), 404
    
    db.session.delete(delete_planet)
    db.session.commit()

    return jsonify("The planet has been deleted successfully"), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
