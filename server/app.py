###########################################################
# Flask server
###########################################################
from flask import Flask, render_template


app = Flask(__name__.split('.')[0])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/textfield')
def textfield():
    return render_template('textfield.html')
