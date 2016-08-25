#! usr/bin/env python3

from flask import Flask, request
import os, datetime, watchdog

app = Flask(__name__)

app.config.update(dict(
    DEBUG=False
))

from API.views import get_data, post_data, pageNotFound
from API import process_data, database_manager

database_manager.create_tables()

def process_post_request():
    '''
    This will check the date for this data point is valid and send instructions to insert that into db.
    date and value are named to make it more obvious that they're different.
    '''

    api_key_from_request = request.args.get('api_key')

    if process_data.check_user_api_key(api_key_from_request) is False:
        return 'You do not have a valid API key to write data. Enter key like -- api_key=YOUR_KEY'
    
    date = request.args.get('date')
    value = request.args.get('value')

    valid_date, formatted_date = process_data.validate_date_string('date', date)

    if valid_date is False:
        return formatted_date

    if value is None:
        return 'You must enter a value for this record. Some suggestions -- value=John_Smith, value=12, value=False, value={lat:12.3, lng: 34.2}'

    return database_manager.insert_API_data(date, value)

def process_get_request():
    '''
    This will pick the parts of a user's query string that the API needs for a get request.
    This will check each are valid and format the inputs correctly.
    If correct, these arguments will be sent to the database manager module to retrive data.
    '''

    api_key_from_request = request.args.get('api_key')

    if process_data.check_user_api_key(api_key_from_request) is False:
        return 'You do not have a valid API key to retreive data. Enter key like -- api_key=YOUR_KEY'

    date_start = request.args.get('start_date')
    date_end = request.args.get('end_date')

    valid_date_start, formatted_date_start = process_data.validate_date_string('start_date', date_start)
    valid_date_end, formatted_date_end = process_data.validate_date_string('end_date', date_end)

    if valid_date_start is False:
        return formatted_date_start
    elif valid_date_end is False:
        return formatted_date_end

    access_details = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    data_from_db = database_manager.retrieve_API_data(date_start, date_end)
    return process_data.format_json(access_details, data_from_db)
