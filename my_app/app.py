from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/users')
def users():
    return render_template('users.html')

if __name__ == "__main__":
    app.run()