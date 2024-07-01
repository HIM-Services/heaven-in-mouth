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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/users')
def users():
    return render_template('users.html')


#this is a class made only for testing purposes
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Entry {self.name}>'

#this is a route made only for testing purposes
#add new id and show id list
@app.route('/test_add')
def test_add():
    entry_to_add = Entry(name='Test entry')

    db.session.add(entry_to_add)
    db.session.commit()

    entries = Entry.query.all()
    for entry in entries:
        print(entry.id)

    return 'Added, check console for details'

#this is a route made only for testing purposes
#deletes by id and show list of id's left
@app.route('/test_del/<int:id>')
def test_del(id):
    entry_to_delete = db.session.get(Entry, id)

    if entry_to_delete is None:
        return 'Entry not found', 404

    try:
        db.session.delete(entry_to_delete)
        db.session.commit()

        entries = Entry.query.all()
        for entry in entries:
            print(entry.id)

        return 'Deleted, Check console for details'
    except Exception as e:
        print(str(e))
        return 'There was a problem deleting that entry', 500

if __name__ == "__main__":
    app.run(port=5001)