__author__ = 'shahryar_saljoughi'

from flask import request, jsonify
from datetime import datetime
from pytz import timezone
from app.main import main
from app.models import Freight
from . import auth

tehran = timezone('Asia/Tehran')

# currently I'm just gonna implement searching by date. later other features will be added.
@main.route('/search_frights')
def search_freights():

    result = Freight.query.all()
    # any iteration of the below loop will eliminate some records form result!

    search_fields = request.json['by']
    for search_field in search_fields:
        if search_field == 'date':

            # the main search algorithm is done in another method. called search_by_date()
            # here I will just get\validate requires datas and send them to that method.

            if 'date' not in request.json:
                return jsonify({'status': 'failure',
                                'message': 'BAD REQUEST : "date" must be sent if you want to search by date '}), 400

            dates = request.json['date']
            start = None if "start" not in dates else dates["start"]
            if start is None:
                return jsonify({
                    'status': "failure",
                    'message': "'BAD REQUEST' : beginning of the period is not defined"
                }), 400

            # needed keys for start time
            needed_keys = ['year', 'month', 'day']
            for item in needed_keys:
                # CHECK IF ALL NEEDED KEYS ARE SENT
                if item not in start:
                    return jsonify({
                        'status': "failure",
                        'message': "BAD REQUEST: {} must be sent".format(item)
                    })
                # TYPE VALIDATION
                if not isinstance(start[item], int):
                    return jsonify({'status': 'failure',
                                    'message': 'BAD REQUEST: all values of start key must be of type integer!'})

            # default value of hour,minute and second is zero!
            start = datetime(
                year=start['year'],
                month=start['month'],
                day=start['day'],
                hour=start["hour"] if "hour" in start and isinstance(start["hour"], int) else 0,
                minute=start["hour"] if "minute" in start and isinstance(start["minute"], int) else 0,
                second=start["hour"] if "second" in start and isinstance(start["second"], int) else 0
            )

            #
            # if any parameter is not sent i will use the current time by default!
            end = datetime(
                year=dates["end"]["year"]
                if "end" in dates and "year" in dates['end'] else
                datetime.now(tehran).year,
                month=dates["end"]["month"]
                if "end" in dates and "month" in dates['end'] else
                datetime.now(tehran).month,
                day=dates["end"]["day"]
                if "end" in dates and "day" in dates['end'] else
                datetime.now(tehran).day,
                hour=dates["end"]["hour"]
                if "end" in dates and "hour" in dates['end'] else 23,
                minute=dates["end"]["minute"]
                if "end" in dates and "minute" in dates['end'] else 59
            )

            search_by_date(result, start, end)


def search_by_date(records, start, end):
    pass
