import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#read database credentials from enviroment
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)
    
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from datetime import datetime

#this is a class made only for testing purposes
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/users')
def users():
    return render_template('users.html')

#this is a route made only for testing purposes
#add new id and show id list
@app.route('/test_add')
def test_add():
    restaurant1 = Restaurant(name='First Restaurant', description='test1')

    db.session.add(restaurant1)
    db.session.commit()

    restaurants = Restaurant.query.all()
    for restaurant in restaurants:
        print(restaurant.id)

    return 'Check console for details'

#this is a route made only for testing purposes
#deletes by id and show list of id's left
@app.route('/test_del/<id>')
def test_del(id):
    task_to_delete = Restaurant.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        restaurants = Restaurant.query.all()
        for restaurant in restaurants:
            print(restaurant.id)
        return 'Check console for details'
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    app.run()