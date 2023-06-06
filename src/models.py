from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorite_planets = db.relationship('FavPlanets', backref='user')
    favorite_people = db.relationship('FavPeople', backref='user')

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    gender = db.Column(db.String(6), nullable = False)

    def __repr__(self):
        return f'<People {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
        }
    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    population = db.Column(db.String(20))

    def __repr__(self):
        return f'<Planets {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }
    

    
class FavPeople(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey(People.id), nullable=False)

    def __repr__(self):
        return f'<FavPeople {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
        }
    
class FavPlanets(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id), nullable=False)

    def __repr__(self):
        return f'<FavPlanets {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

