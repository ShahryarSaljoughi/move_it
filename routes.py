from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
import models


app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
"""
app.config[
    'SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+ os.path.join(BASE_DIR, '/database/moveit_db.db')
"""
#app.root_path : contains the absolut path of project
#os.path.join(app.root_path,'database/moveit_db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/flask_example/move_it/database/moveit_db.db'
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
db = SQLAlchemy(app)


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

@app.route('/signup',methods=['POST','GET'])
def sign_up():
        if request.method=='POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']

            role = request.form['role']
            phonenumber = request.form['phonenumber']

            new_user = models.User(username,password,email,role,phonenumber)
            db.session.add(new_user)
            db.session.commit()

            return str(new_user)
        elif request.method=='GET':
            return "salam"


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
