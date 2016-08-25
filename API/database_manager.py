#! usr/bin/env python3

import psycopg2

'''
#This is the code to connect to the PostgreSQL database on Heroku.

import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''

#This is the code to connect to the database on your local dev env
conn = psycopg2.connect("dbname=john user=john")

def create_tables():
    '''
    Initialises the databases in whichever postgreSQL database we are connected to.
    '''
    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS registered_users (api_key varchar PRIMARY KEY, user_name varchar, user_email varchar);")
            cur.execute("CREATE TABLE IF NOT EXISTS data_store (id serial PRIMARY KEY, data_date varchar, value varchar);")

def drop_tables():
    '''
    Destroys the databases in whichever postgreSQL database we are connected to.
    '''
    with conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS registered_users;")
            cur.execute("DROP TABLE IF EXISTS data_store;")


def insert_API_data(date, data_value):
    '''
    This can be used by any user who has an api key
    '''
    with conn:
        with conn.cursor() as cur:
            query = "INSERT INTO data_store (data_date, value) VALUES (%s, %s);"
            query_data = (date, data_value)
            cur.execute(query, query_data)
            return 'Data entered'

def retrieve_API_data(date_start, date_end):
    '''
    This can be used by any user who has an api key
    Creates a new entry in the db
    '''
    with conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM data_store WHERE (data_date >= %s AND data_date <= %s);"
            query_data = (date_start, date_end)
            cur.execute(query, query_data)
            results = cur.fetchall()
            return results

def retrieve_user_details(api_key_from_request):
    '''
    This can be used by the application itself.
    This will search through the table of api_keys and check if the user's key is there.
    '''
    with conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM registered_users WHERE (api_key = %s);"
            query_data = (str(api_key_from_request), )
            cur.execute(query, query_data)
            result = cur.fetchall()
            return result

def insert_user_details(api_key, user_name, user_email):
    '''
    This can be used by the application itself.
    This will search through the table of api_keys and check if the user's key is there.
    '''
    with conn:
        with conn.cursor() as cur:
            query = "INSERT INTO registered_users (api_key, user_name, user_email) VALUES (%s, %s, %s);"
            query_data = (api_key, user_name, user_email)
            cur.execute(query, query_data)
            return 'Entered user details'
