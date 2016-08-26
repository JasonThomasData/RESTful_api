###A restful API made with Flask.

Making APIs is almost certainly something I'll need to do in my software career, so I thought I'd show some initiative and prove I can make an API.

This API has the following features:

- Lets the admin create user IDs via the API interface.
- Allows a third-party user with a valid api_key to submit data and retrieve data from the API.
- Returns a json object with the data to the client.

This is RESTful in the sense it does not need a client state: state is handled with a query string. This API is modular in design and is scalable. This uses a production-ready database, postgreSQL. 

The principles outlined in [this tutorial](http://www.tutorialspoint.com/restful/restful_statelessness.htm) are addressed.

This interface is self-explanatory: at no point in the process of formatting a query string should the user not receive feedback.

####Installation for development

This was produced using Ubuntu 14.04 and python3.

To start, create a virtualenv in python3:

    virtualenv -p python3 env

Activate it:

    source env/bin/activate

Then install all requirements:

    pip3 install -r requirements.txt

You will need to have postgreSQL installed on your machine. You can install it like this:

    sudo apt-get install postgresql

####Deployment

I've made my API to run on Heroku. To connect to the postgreSQL database in Heroku, you need this code:

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

In development, you can replace the above code with your own connection:

    conn = psycopg2.connect("dbname=john user=john")

Of course for this to work, you will need to have created a postgreSQL database already. From the terminal:

    psql

If you get a fatal error, it's most likely because there's no database.

To spin up a db [here for more info](http://stackoverflow.com/questions/17633422/psql-fatal-database-user-does-not-exist):

    createdb <db_name>

To run the app, via the terminal, type:

    export FLASK_APP=API/controller.py

Then:

    flask run

The above is preferable to using app.run(), according to the [API docs](http://flask.pocoo.org/docs/0.11/quickstart/#a-minimal-application), since it has wierd side effects.

####Tests

Currently these unit tests work in a development environment.

First, you'll need to create a database called ```test_flask_api```.

This is exactly the same as creating your other database, type:

    createdb test_flask_api

Inside unit_test.py file, you'll need to change the user details in the ```db_credentials``` variable so you can use the postgreSQL database. That should be the same username that you used to create the db in the ```psql``` terminal tool.

To run the tests, use:

    python3 unit_test.py

####Usage

To allow anyone to use this API, their details must be stored in a table called ```registered_users```.

You'll need to enter that person's details and their unique id, or api_key. Open Python in ther terminal and run:

    import API.database_manager as db
    db.create_tables() #This will create tables if they don't exist already, meaning the app hasn't run yet.
    db.insert_user_details('1412519715937603534460152', 'Amy', 'amy@gmail.com')

You should see this echo:

    Entered user details

That function is not used in the API and no request the user enters will allow access to it.

Now, this user can add and retrieve data from the ```data_store``` table with her ```api_key```.

Accesing the database can be done through a query string to ```/post?```:

    API_URL/post?api_key=1412519715937603534460152&date=2000-01-01&value=1323

The query string above has these arguments:

    api_key = 1412519715937603534460152
    date = 2000-01-01
    value = 1323

This user will receive a response that they have submitted a data row to the database.

If the same user wants to retrieve that data:

    API_URL/get?api_key=1412519715937603534460152&start_date=1900-01-01&end_date=2050-01-01

This query string has these arguments:

    api_key = 1412519715937603534460152
    start_date = 1900-01-01
    end_date = 2050-01-01

The response from that ```/get?``` request will look like:

    {
        "accessed": "2016-08-21 20:23:06", 
        "results": [
            {
                "date": "2000-01-01", 
                "value": "1323"
            }
        ]
    }

The above value will be parsed to the data as a string - that's just so the value can handle any input. Ints and floats can be converted to ints from those strings. If this api is to be used to accept different types like like boolean variables etc, the db schema could be changed for this.

If the user makes more ```/post?``` requests, then the ```results``` array would contain more data objects.

####Licence

I made this to show future employers that I can make an API... that's it. 

If you can seriously think of a reason to use this, go ahead. 

No copyright applies, appart from the licences distributed with any packages this API uses.

####Last thoughts

If I was going to do this again, I'd use the SQLAlchemy tool for this. I did investigate this tool and I like it, and I think it's worth using. This is my first Flask/postgreSQL/Heroku build so I thought I'd do things with postgreSQL and psycopg2 to see how that went first.

One thing I find really appealing about SQLAlchemy is it requires you to create classes as models, which are used to build the databases. This is then sensible to seperate the class concern into a module called models. You can then put the views in a view module, and you've got a nice, neat, MVC design patter. I've got my 'models' in a file called ```database_manager```. Not a perfect MVC pattern, but it makes sense to the author and is seperate from the ```controller``` and ```views```.

Also, I've been unsure when to commit anything to Github with this project. The entire project has been a learning experience and it was in prototype mode right until the end. I feel like having the Git history recorded of that prototype process would not be useful.
