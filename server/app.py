###########################################################
# Flask server
###########################################################
from flask import Flask, render_template


app = Flask(__name__.split('.')[0])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')
