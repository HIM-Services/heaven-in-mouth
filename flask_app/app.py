import os
from flask import Flask, render_template, redirect, flash, url_for, session, make_response
from flask_wtf.csrf import generate_csrf
from flask import request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

#


#read database credentials from enviroment
def get_env_variable(name):
    try:
        return os.getenv(name)
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)

# dotenv is used to read the .env file and set the environment variables
load_dotenv()

SECRET_KEY = get_env_variable("SECRET_KEY")
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'


# SECRET KEY is used to sign the session cookie and other security related stuff #
app = Flask(__name__)
app.secret_key='secret_key'



app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<user {self.name}>'

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    dish_name = db.Column(db.String(255), nullable=False)  # Nazwa pola dish_name
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def __repr__(self):
        return f'<Menu {self.dish_name} - {self.price}>'

@app.route('/')
def home():
    return render_template('home.html')

@app.route ('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)
    
@app.route ('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('edit_user.html', user=user)


@app.route('/rest', methods=['GET'])
def rest():
    all_restaurants = Restaurant.query.all()
    restaurants_list = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'phone': restaurant.phone} 
                        for restaurant in all_restaurants]
    return {'restaurants': restaurants_list}

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        print(request.form)
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
        
        return redirect(url_for('users'))
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
        return redirect(url_for('menu_add', restaurant_id=new_restaurant.id))
    
    return render_template('rest_add.html')

feature/insert-restaurant-option
@app.route('/menu_add/<int:restaurant_id>', methods=['GET', 'POST'])
def menu_add(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()

    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        price = request.form.get('price')

        print(f"Received Data: dish_name={dish_name}, price={price}")

        if not dish_name or not price:
            print('All fields are required!')
            return redirect(request.url)
        
        try:
            price = float(price)
        except ValueError:
            print('Price must be a number!')
            return redirect(request.url)
        
        new_menu_item = Menu(restaurant_id=restaurant_id, dish_name=dish_name, price=price)
        db.session.add(new_menu_item)
        db.session.commit()
        print('Menu item added!')
        return redirect(url_for('menu_add', restaurant_id=restaurant_id))

    return render_template('menu_add.html', restaurant=restaurant)

@app.route('/menu', methods=['GET'])
def menu():
    all_menu_items = Menu.query.all()
    menu_list = [
        {'id': item.id, 'restaurant_id': item.restaurant_id, 'dish_name': item.dish_name, 'price': float(item.price)} 
        for item in all_menu_items
    ]
    return {'menu_items': menu_list}


# Logout works by deleting the cookie that stores the user login status
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('home')))
    response.set_cookie('login', '', expires=0)
    session.pop('csrf_token', None)
    return redirect(url_for('home'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return 'User not found'
        
        if not check_password_hash(user.password, password):
            return 'Incorrect password'
        
        session['csrf_token'] = generate_csrf()
        
        response = make_response(redirect(url_for('home')))
        response.set_cookie('login', 'true', httponly=True)
        
        return response
        
    return render_template('login.html')
main

# If you re not using docker please uncomment the line below 
if __name__ == "__main__":
   app.run(port=5001)
