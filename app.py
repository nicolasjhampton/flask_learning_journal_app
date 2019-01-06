from flask import Flask

import models

app = Flask(__name__)

DEBUG = True
PORT = 3000
HOST = "0.0.0.0"

# / /entries /entries/<slug> /entries/edit/<slug> /entries/delete/<slug> /entry

@app.route("/")
def index():
    pass

@app.route("/entries")
def list_entries():
    pass

@app.route("/entries/<str:slug>")
def details():
    pass

@app.route("/entries/edit/<str:slug>")
def edit():
    pass

@app.route("/entries/delete/<str:slug>")
def delete():
    pass

@app.route("/entry")
def add():
    pass

app.run(debug=DEBUG, port=PORT, host=HOST)