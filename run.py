__author__ = 'shahryar_slg'

from app import app


# app.run()

app.run(host=app.config['HOST'], port=app.config['PORT'], debug=True)
