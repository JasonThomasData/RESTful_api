#! usr/bin/env python3

import os
import API.controller
import API.views
import API.process_data
import API.database_manager
import unittest
import psycopg2
import datetime

#Replace the user with your own credentials
db_credentials = "dbname=test_flask_api user=john"


'''
These tests are for units - single functions.
These are the smaller units that the API relies on.
'''


class TestDateValidatorIncorrectDay(unittest.TestCase):
    '''
    Tests the validate_date_string function. The tests of the app above used this, and this is a specific test.
    Same for next two tests.
    '''

    def test(self):
        result_1, result_2 = API.process_data.validate_date_string('test_date', '2011-01-32')
        assert result_1 == False
        assert result_2 == 'Incorrect test_date format, should be like -- test_date=2000-01-01'


class TestDateValidatorIncorrectMonth(unittest.TestCase):
    '''
    Tests the validate_date_string function. The tests of the app above used this, and this is a specific test. 
    '''

    def test(self):
        result_1, result_2 = API.process_data.validate_date_string('test_date', '2011-MM-31')
        assert result_1 == False
        assert result_2 == 'Incorrect test_date format, should be like -- test_date=2000-01-01'


class TestDateValidatorCorrect(unittest.TestCase):
    '''
    Tests the validate_date_string function. The tests of the app above used this, and this is a specific test.
    '''

    def test(self):
        result_1, result_2 = API.process_data.validate_date_string('test_date', '2011-05-31')
        assert result_1 == True
        assert result_2 == '2011-05-31'


class TestDateValidatorCorrect(unittest.TestCase):
    '''
    Tests the validate_date_string function. The tests of the app above used this, and this is a specific test.
    '''

    def test(self):
        result_1, result_2 = API.process_data.validate_date_string('test_date', '2011-05-31')
        assert result_1 == True
        assert result_2 == '2011-05-31'


class TestJsonDataFormatter(unittest.TestCase):
    '''
    Tests the format_json function.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

    def test(self):
        with API.controller.app.test_request_context():
            access_details = access_details = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            data_from_db = [(1, '2011-05-31', 'Amsterdam')]

            formatted_data = API.process_data.format_json(access_details, data_from_db)

            #I found the .data attribute, because every python function returns all object attributes with .__dir__()
            assert '"date": "2011-05-31",' in str(formatted_data.data)
            assert '"value": "Amsterdam"' in str(formatted_data.data)


class TestCheckUserApiKeyPass(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message to user.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        with API.controller.app.test_request_context():
            assert API.process_data.check_user_api_key('12Jas97l59N603Kj3460a52') == True


class TestCheckUserApiKeyFail(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message to user.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        with API.controller.app.test_request_context():
            assert API.process_data.check_user_api_key('12Jas97l59N603Kfailj3460a52') == False


'''
These tests are at the application level.
These replicate the requests that users would send to the API via query strings.
'''

class TestFirstRequest(unittest.TestCase):
    '''
    Tests the request to URL/ returns a message to user.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

    def test(self):
        rv = self.app.get('/')
        assert b'To retrieve data, use the /get url. If you have priveledges to write to the database, you can use /post.' in rv.data


class TestRequestWrongURL(unittest.TestCase):
    '''
    Tests the request to URL/g3t returns a message to use URL/get 
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

    def test(self):
        rv = self.app.get('/g3t?')
        assert b'To retrieve data, use the /get url. If you have priveledges to write to the database, you can use /post.' in rv.data


class TestRequestToGet(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message to user.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get')
        assert b'You do not have a valid API key to retreive data. Enter key like -- api_key=YOUR_KEY' in rv.data


class TestRequestToPost(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message to user.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post')
        assert b'You do not have a valid API key to write data. Enter key like -- api_key=YOUR_KEY' in rv.data


class TestApiKeyWorksPass(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message to enter date. This means the api key was valid.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52')
        assert b'You must have a date, like -- date=2000-01-01' in rv.data


class TestApiKeyWorksFail(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the api_key was invalid. User cannot proceed.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l5invalidkey9N603Kj3460a52')
        assert b'You do not have a valid API key to write data. Enter key like -- api_key=YOUR_KEY' in rv.data


class TestPostDateMonthIncorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the date was invalid. Month 13 - no such month.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000-13-01')
        assert b'Incorrect date format, should be like -- date=2000-01-01' in rv.data


class TestPostDateDayIncorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the date was invalid. Day string - not a date string.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000-12-first')
        assert b'Incorrect date format, should be like -- date=2000-01-01' in rv.data


class TestPostDateYearIncorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the date was invalid. Year has an 'o' char - not a date string.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=200o-12-01')
        assert b'Incorrect date format, should be like -- date=2000-01-01' in rv.data


class TestPostDateIncorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the date was invalid. String has an extra hyphen, won't pass as date
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000--12-01')
        assert b'Incorrect date format, should be like -- date=2000-01-01' in rv.data


class TestPostDateCorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the date was valid. This one is a proper date string, will pass
    Now it will prompt you to enter a value... user can get this far if date is valid.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000-12-01')
        assert b'You must enter a value for this record. Some suggestions -- value=John_Smith, value=12, value=False, value={lat:12.3, lng: 34.2}' in rv.data


class TestPostValueIncorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the value was invalid. The issue is spelling of value, will not pass.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000-12-01&valu=20')
        assert b'You must enter a value for this record. Some suggestions -- value=John_Smith, value=12, value=False, value={lat:12.3, lng: 34.2}' in rv.data


class TestPostValueCorrect(unittest.TestCase):
    '''
    Tests the request to URL/post returns a message that the value was valid.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/post?api_key=12Jas97l59N603Kj3460a52&date=2000-12-01&value=20')
        assert b'Data entered' in rv.data


class TestGetStartDateIncorrectBlank(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message that the start_date was incorrect. Date value is blank, can't parse blank string as date
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get?api_key=12Jas97l59N603Kj3460a52&start_date=')
        assert b'Incorrect start_date format, should be like -- start_date=2000-01-01' in rv.data


class TestGetStartDateIncorrectFormatting(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message that the start_date was incorrect. Date value uses commas as delimeters, needs hyphens
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get?api_key=12Jas97l59N603Kj3460a52&start_date=2000,01,01')
        assert b'Incorrect start_date format, should be like -- start_date=2000-01-01' in rv.data


class TestGetStartDateIncorrectString(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message that the start_date was incorrect. Date value contains string
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get?api_key=12Jas97l59N603Kj3460a52&start_date=s000-01-01')
        assert b'Incorrect start_date format, should be like -- start_date=2000-01-01' in rv.data


class TestGetStartDateCorrect(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message that the start_date was correct. 
    Now it will prompt user to declare an end_date, which won't happen unless start_date is correct.
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get?api_key=12Jas97l59N603Kj3460a52&start_date=2000-01-01')
        assert b'You must have a end_date, like -- end_date=2000-01-01' in rv.data


class TestGetEndDateCorrect(unittest.TestCase):
    '''
    Tests the request to URL/get returns a message that the end_date was correct. 
    The results will be a json file, with an array called results -- "results": [
    '''

    def setUp(self):
        API.controller.app.config['TESTING'] = True
        self.app = API.controller.app.test_client()

        API.database_manager.conn = psycopg2.connect(db_credentials)
        API.database_manager.create_tables()
        API.database_manager.insert_user_details('12Jas97l59N603Kj3460a52', 'Jason', 'jason@jason.com')

    def tearDown(self):
        API.database_manager.drop_tables()

    def test(self):
        rv = self.app.get('/get?api_key=12Jas97l59N603Kj3460a52&start_date=2000-01-01&end_date=2000-01-01')
        assert b'"results": [' in rv.data


if __name__ == '__main__':
    unittest.main()