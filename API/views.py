#! usr/bin/env python3

from flask import request
from API.controller import app
import API.controller

@app.route('/get', methods=['GET'])
def get_data():
    '''
    Process a request to /get.
    This is what a registered user will use to retrive the data
    '''
    return API.controller.process_get_request()

@app.route('/post', methods=['GET', 'POST'])
def post_data():
    '''
    Process a request to /post.
    This is how we add datato the database for users to access.
    '''
    return API.controller.process_post_request()

@app.errorhandler(404)
def pageNotFound(error):
    '''
    Usually when a request does not specify whether to use /get or /post.
    '''

    return 'To retrieve data, use the /get url. If you have priveledges to write to the database, you can use /post.'
