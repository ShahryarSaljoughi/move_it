
from flask import render_template, make_response, jsonify
from app.main import main
from flask import request
from app import app
from . import auth

@main.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


# the below method is just for fun and can be deleted:
@main.route('/')
def hello_world():
    return render_template('main_page.html')


@app.errorhandler(404)
def not_found(exception):
    return make_response(jsonify({'error': 'Not found -404'}), 404)


@app.errorhandler(401)
def unauthorized_access(error):
    return jsonify("unauthorized access")


####################################
# @auth.error_handler
# def auth_error():
#     """
#     this function will response to client, regarding the fact that the client is not authenticated!
#     :return:
#     """
#     # following if else blocks , indicate which view function caused error
#     if "{}/testy".format(app.config['PORT']) in request.url and "GET" == request.method:
#         pass
####################################


# if __name__ == '__main__':
#    app.run()
