
from flask import render_template, make_response, jsonify, g
from app.main import main, appExceptions
from flask import request
from app import app
from app.main.views import  registration
from . import auth

@main.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


@main.before_request
def add_authorization_to_json():
    # I want to add some more information to request.json before it is processed in views
    # these extra information are used in validations!

    if request.is_json:
        try:
            g_has_user = registration.verify_password(request.authorization['username'],
                                                      request.authorization['password'])

        # in case request.authorization is None:
        except TypeError:
            g_has_user = registration.verify_password('', '')

        if g_has_user:
            request.json['user_type'] = g.user.role.title
            request.json['user_id'] = g.user.id


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


@app.errorhandler(appExceptions.AppException)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


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
