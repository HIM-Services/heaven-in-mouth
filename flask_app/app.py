import os
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

app = Flask(__name__)

#read database credentials from enviroment
def get_env_variable(name):
    try:
        return os.getenv(name)
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)

# dotenv is used to read the .env file and set the environment variables
load_dotenv()

POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rest')
def rest():
    all_restaurants = Restaurant.query.all()
    return render_template('rest.html', restaurants=all_restaurants)

@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/rest_add', methods=['GET', 'POST'])
def rest_add():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        if not name or not address or not phone:
            print('All fields are required!')
            return redirect(request.url)
        
        if len(phone) < 9:
            print('Insert correct phone number')
            return redirect(request.url)
        
        new_restaurant = Restaurant(name=name, address=address, phone=phone)
        db.session.add(new_restaurant)
        db.session.commit()
        print('Restaurant added!')
    
    return render_template('rest_add.html')

# If you re not using docker please uncomment the line below 
#if __name__ == "__main__":
#    app.run(port=5001)
