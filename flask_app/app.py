import os
from flask import Flask, render_template, redirect, flash, url_for, session, make_response
from flask_wtf.csrf import generate_csrf
from flask import request
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import validate_email, validate_phone
# this noqa F403 says for flake8 to ignore the error that is raised when importing models
from models import *  # noqa F403


# read database credentials from enviroment


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


DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'  # noqa F405


# SECRET KEY is used to sign the session cookie and other security related stuff #
app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db is initialized in models.py file and imported using *
db.init_app(app)  # noqa F405


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    # using the session to get the current user id for admin permissions
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    all_users = Users.query.all()
    if session.get('admin') == False:
        return render_template('home.html')
    return render_template('users.html', users=all_users, current_user=current_user)


@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    # using the session to get the current user and for deleting stuff, all of the session data is getting cleared when on current user
    current_user_id = request.session.get('user_id')
    current_user = Users.query.get(current_user_id)
    user = Users.query.get(user_id)
    if user is current_user:
        response = make_response(redirect(url_for('home')))
        session.clear()
        session.pop('csrf_token', None)
        db.session.delete(current_user)
        db.session.commit()
        return response
    else:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('users'))


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
# Edit user function
def edit_user(user_id):
    user = Users.query.get(user_id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.admin = request.form.get('admin') == 'true'
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('edit_user.html', user=user)


@app.route('/rest', methods=['GET'])
def rest():
    all_restaurants = Restaurants.query.all()
    json_restaurants = [restaurant.to_json() for restaurant in all_restaurants]
    return {'restaurants': json_restaurants}


@app.route('/rest_del/<int:restaurant_id>', methods=['POST', 'GET'])
# Delete restaurant function using session to get the current user for permissions
def rest_del(restaurant_id):
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    rest_to_delete = Restaurants.query.filter_by(
        restaurant_id=restaurant_id).first()
    if rest_to_delete:
        # Delete all menu items associated with the restaurant
        Menu.query.filter_by(restaurant_id=restaurant_id).delete()
        db.session.delete(rest_to_delete)
        db.session.commit()
        flash('Restaurant deleted')
    else:
        flash('Restaurant not found')
    return redirect(url_for('rest', current_user=current_user))


@app.route('/rest_edit/<int:restaurant_id>', methods=['POST', 'GET'])
# Edit restaurant function using session to get the current user for permissions
def rest_edit(restaurant_id):
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    rest_to_edit = Restaurants.query.filter_by(
        restaurant_id=restaurant_id).first()
    if rest_to_edit:
        if request.method == 'POST':
            rest_to_edit.name = request.form.get('name')
            rest_to_edit.address = request.form.get('address')
            rest_to_edit.phone = request.form.get('phone')

            if not validate_phone(rest_to_edit.phone):
                flash('Invalid phone number')
                return redirect(url_for('rest_edit', restaurant_id=restaurant_id))

            db.session.commit()
            return redirect(url_for('rest'))
        return render_template('rest_edit.html', restaurant=rest_to_edit, current_user=current_user)
    else:
        flash('Restaurant not found')
    return redirect(url_for('rest'))


@app.route('/register', methods=['GET', 'POST'])
# Changed the cookies with session to store the user login status and data more secured not vissble to user secured doubling the email
def register():
    if request.method == 'POST':
        print(request.form)
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if not validate_email(email):
            flash('Invalid email')
            return redirect(url_for('register'))

        if not validate_phone(phone):
            flash('Invalid phone number')
            return redirect(url_for('register'))

        plain_text_password = request.form.get('password')

        if not plain_text_password:
            return "Password is required", 800

        hashed_password = generate_password_hash(plain_text_password)
        if request.form.get('email') == 'admin@admin.admin':
            try:
                new_user = Users(name=name, email=email, phone=phone,
                                 password=hashed_password, admin=True)
                db.session.add(new_user)
                db.session.commit()
            except Exception as i:
                print(i)
                return "Email already exists", 800
        else:
            try:
                new_user = Users(name=name, email=email,
                                 phone=phone, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
            except Exception as i:
                print(i)
                return "Email already exists", 800

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/rest_add', methods=['GET', 'POST'])
# Add restaurant function using session to get the current user for permissions
def rest_add():
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        if not validate_phone(phone):
            flash('Invalid phone number')
            return redirect(url_for('rest_add'))

        new_restaurant = Restaurants(name=name, address=address, phone=phone)
        db.session.add(new_restaurant)
        db.session.commit()

        print('Restaurant added!')

    return render_template('rest_add.html', current_user=current_user)


# Logout works by deleting the cookies and session data that stores the user login status and data
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect(url_for('home')))
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    session.clear()
    session.pop('csrf_token', None)
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()

        if not user:
            return 'User not found'

        if not check_password_hash(user.password, password):
            return 'Incorrect password'
        # Now login create session instead of cookies becouse it is more secure and not visible to user
        session['csrf_token'] = generate_csrf()
        session['user_id'] = user.user_id
        session['admin'] = user.admin
        session['email'] = user.email
        response = make_response(redirect(url_for('home')))

        return response

    return render_template('login.html', current_user=current_user)


@app.route('/menu_add/<int:restaurant_id>', methods=['GET', 'POST'])
def menu_add(restaurant_id):
    # using the session to get the current user for permissions
    current_user_id = session.get('user_id')
    current_user = Users.query.get(current_user_id)
    restaurant = Restaurants.query.filter_by(
        restaurant_id=restaurant_id).first()
    if request.method == 'POST':
        menu_name = request.form.get('menu_name')
        price = request.form.get('price')

        print(f"Received Data: menu_name={menu_name}, price={price}")

        if not menu_name or not price:
            print('All fields are required!')
            return redirect(request.url)

        try:
            price = float(price)
        except ValueError:
            print('Price must be a number!')
            return redirect(request.url)

        new_menu_item = Menu(restaurant_id=restaurant_id,
                             menu_name=menu_name, price=price)
        db.session.add(new_menu_item)
        db.session.commit()
        print('Menu item added!')
        return redirect(url_for('menu_add', restaurant_id=restaurant_id))

    return render_template('menu_add.html', restaurant=restaurant, current_user=current_user)


@app.route('/menu', methods=['GET'])
def menu():
    all_menu_items = Menu.query.all()
    json_menus = [menu.to_json() for menu in all_menu_items]
    return {'menu_items': json_menus}


# If you re not using docker please uncomment the line below
if __name__ == "__main__":
    app.run(port=5001)
