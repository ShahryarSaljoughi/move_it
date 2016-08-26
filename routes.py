from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
import models
from forms import SignupForm


app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+ app.root_path+'\\database\\shipment.db'
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
db = SQLAlchemy(app)
app.secret_key = "development-key"



@app.route('/shipment/<string:username>/freights',methods=['GET'])
def get_freights(username):
    """
    this will return the freights made by user!
    :return: text/json
    """
    pass


@app.route('/shipment/<string:username>freights', methods=['POST'])
def create_freight(username):
    pass

@app.route('/signup',methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        form = SignupForm()
        return render_template('signup.html', form=form)
    elif request.method == 'POST':
        return "success"


@app.route('/salam',methods=['POST'])
def salam():
    a=request.form['name']
    return "got it"#str(a)


@app.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


@app.route('/')
def hello_world():
    return 'main_page'


if __name__ == '__main__':
    app.run()
