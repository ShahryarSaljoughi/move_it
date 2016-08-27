from flask import Flask, render_template, request
from flask import abort
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
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)

    elif request.method == 'POST':

        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            if request.json:
                new_user=models.User(username=request.json['username'],
                                     email=request.json['email'],
                                     phonenumber=request.json['phonenumber'],
                                     role_id=request.json['role_id'] if request.json['role_id'] in [1, 2] else 1
                                     )
                db.session.add(new_user)
                db.session.commit()
                return "success :) %r created" % new_user
            else:
                abort(400)


@app.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


@app.route('/')
def hello_world():
    return 'main_page'


if __name__ == '__main__':
    app.run()
