from abc import ABCMeta, abstractmethod


class AppException(Exception):
    __metaclass__ = ABCMeta


class MailingError(AppException):
    """
    this exception is raised in case sending confirmation mail fails
    """
    status_code = 501

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ValidationError(AppException):
    """
    this exception rill be raised if the json received to server-side is not valid
    """
    status_code = 400

    def __init__(self, errors, message='bad request, json validation error occurred', status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.errors = errors

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['errors'] = self.errors  # errors is a dict itself!
        return rv

    # todo: take polymorphism in consideration! there can be a BaseException class
    # todo: that others inherit! and there can be only one error handler for Base Exception!


class NoJSONError(AppException):

    def __init__(self, message='bad request. This api is json based but no json received',
                 status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        print "no json occurred"

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
