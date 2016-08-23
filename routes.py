from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config[
    'SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///'+ os.path.join(BASE_DIR, '/database/moveit_db.db')
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


@app.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


@app.route('/')
def hello_world():
    return 'main_page'


if __name__ == '__main__':
    app.run()
