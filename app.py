from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/beerDB"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/new')
def new():
    return render_template('pages/newpics.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('pages/page_not_found.html'), 404

@app.route('/test')
def test():
    mongo.db.users.insert({'name': 'Anna', 'password' : '12345'})
    return '<h1>Added a User!</h1>'