
from flask import render_template, make_response, jsonify
from app.main import main



@main.route('/author')
def see_author():
    return render_template('aboutAuthor.html')


# the below method is just for fun and can be deleted:
@main.route('/')
def hello_world():
    return render_template('main_page.html')


@main.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


# if __name__ == '__main__':
#    app.run()
