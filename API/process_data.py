#! usr/bin/env python3

from flask import jsonify
from API import database_manager
import datetime

def validate_date_string(date_type, date_to_check):
    '''
    This will check dates are valid and return formatted dates if they are valid.
    Otherwise this will return instructions about the correct formatting of datestrings.
    '''
    try:
        formatted_date = datetime.datetime.strptime(date_to_check, '%Y-%m-%d').strftime('%Y-%m-%d')
        return True, formatted_date
    except ValueError:
        return False, 'Incorrect %s format, should be like -- %s=2000-01-01' %(date_type, date_type)
    except TypeError:
        return False, 'You must have a %s, like -- %s=2000-01-01' %(date_type, date_type)

def check_user_api_key(api_key_from_request):
    '''
    This is where we check the user has a valid user id. This api_key will be in a table called registered_users
    '''
    api_key_match = database_manager.retrieve_user_details(api_key_from_request)
    if len(api_key_match) > 0:
        return True
    return False

def format_json(access_details, data_from_db):
    '''
    Return this data in json format.
    First convert each tuple (row from db) to dicts with key-value pairs. flask.jsonify will convert that
    to a json object that will be pretty printed on the client side.
    '''
    array_of_dicts = []
    for data_tuple in data_from_db:

        dict_from_tuple = dict([('date', data_tuple[1]), ('value', data_tuple[2])])
        array_of_dicts.append(dict_from_tuple)
    formatted_json = jsonify(accessed = access_details, results = array_of_dicts)
    return formatted_json
