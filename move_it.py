from flask import Flask, render_template
import freight

app = Flask(__name__)



@app.route('/shipment/<string:username>/freights',methods=['GET'])
def get_freights(username):
    """
    this will return the freights made by user!
    :return: text/json
    """
    pass

@app.route('/shipment/<string:username>freights',methods=['POST'])
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
