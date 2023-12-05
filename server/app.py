# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def find_earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    response_body = {"message":f"Earthquake {id} not found."}
    response_code = 404
    if quake: 
        response_body = {
            "id": id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        response_code = 200
    return make_response(response_body, response_code)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def find_earthquake_magnitude(magnitude):
    quakes = []
    for quake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        quakes.append({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        })
    body = {
        "count": len(quakes),
        "quakes": quakes
    }
    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
