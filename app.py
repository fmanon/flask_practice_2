# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]

# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:nFqmtMPS2ndjg466@cluster0.qkcvq.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index', methods=['GET','POST'])

def index():
    if request.method=="POST":
        return render_template('index.html')
    else:
        return redirect('/add')


# CONNECT TO DB, ADD DATA

@app.route('/add', methods=['GET', 'POST'])

def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        item_date = request.form['date']
        item_name = request.form['name']
        item_price = request.form['price']
        item_bar_code = request.form['bar_code']

        # connect to the database
        events = mongo.db.events
        # insert new data
        events.insert({'date':item_date, 'item':item_name, 'price':item_price, 'bar_code':item_bar_code})
        # return a message to the user
        return redirect('/inventory')



@app.route('/inventory')

def inventory():
    collection = mongo.db.events
    events = collection.find({}).sort('date', 1)

    return render_template('inventory.html', events = events)
