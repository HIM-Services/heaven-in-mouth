import os
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

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

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<User {self.name}>'

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

@app.route ('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/rest')
def rest():
    all_restaurants = Restaurant.query.all()
    restaurants_list = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'phone': restaurant.phone} 
                        for restaurant in all_restaurants]
    return {'restaurants': restaurants_list}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)  # This will print the form data to the console
        name = request.form.get('name')  
        email = request.form.get('email')
        phone = request.form.get('phone')
        plain_text_password = request.form.get('password')

        if not plain_text_password: 
            return "Password is required", 800

        hashed_password = generate_password_hash(plain_text_password)
        
        new_user = User(name=name, email=email, phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

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
if __name__ == "__main__":
   app.run(port=5001)
