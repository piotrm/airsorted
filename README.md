# airsorted

## Setup
### Prerequisites
In order to run the application one must first install:
* Python 3
* Sqlite3 - https://sqlite.org/download.html
* virtualenv - https://virtualenv.pypa.io/en/stable/installation/

### Setting up the app
#### Clone the app
```
$ git clone https://github.com/piotrm/airsorted_address_book.git
```
#### Activate virtual env
Access the app's directory and follow the steps

1. Create virtual env - ONLY if it does not yet exist
```
$ virtualenv airsorted
```
2. Activate virtual env
```
$ . airsorted/bin/activate
```

#### Install dependencies
To install the dependencies form `requirements.txt` do the following:
```
$ pip install -r requirements.txt
```

#### Set the environmental variables
1. Allow the application to be discovered
```
$ export FLASK_APP=airsorted_address_book/airsorted_address_book.py
```
2. Set the environment
```
$ export ADDRESS_BOOK_SETTINGS=development
```
4. Set the path to DB

__NOTE__: if it is not set the default path will be used
```
$ export SQLALCHEMY_DATABASE_URI=/whatever/path
```

5. Set secret key
```
$ export SECRET_KEY=secretkey
```

#### Seed the database
```
$ python manage.py seed
```

### Running tests
In order to run test one may either run them separately:
```
$ python contacts_test.py
```
or run a script that will execute all of them:
```
./test.sh
```

### Running the app
```
$ flask run
```

## API
The application exposes Contacts API. It can be accessed by cURL or via browser (index, show)

#### Index
All contacts:
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/contacts
```
All contacts, paginated (default attributes: __page__: 1, __per_page__: 10):
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/contacts?page=1&per_page=2
```
Search by email:
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/contacts?email=rysiek@gmail.com
```

#### Show
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/contacts/1
```

#### Update
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X PUT -d '{"emails":["another@email.com"]}' http://localhost:5000/api/v1/contacts/1
```
#### Create
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X POST -d '{"first_name":"Jack","last_name":"Sparrow","emails":["jack@disney.com", "jsparrow@gmail.com"],"company":"Disney"}' http://localhost:5000/api/v1/contacts
```
#### Delete
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/v1/contacts/1
```

## Rationale
It has been my first project in Python and Flask. Some of the things were not yet obvious for me, especially in comparison to what I got used to working with Rails. I have tried to do my best to follow the documentation and guidelines. Here is the rationale behind some of the decisions I have made.

### Structure
I have chosen to build the app in form of a package instead of module as it was not going to fit into one or two files.

### Models
I have chosen SQLAlchemy ORM instead of going pure sql because I wanted to check how it worked. It also looked like less overhead in terms of table creation etc.

__models.py__ consist of two models, __Contact__ and __Email__, staying in a relationship. It also consist of two schemas (Marshmallow), that act as data serializers. They should probably be moved out to a separate file.

### Views
__views.py__ consist of all the view functions that builds the Contacts API. Most of the functions are probably too big, and could be refactored, so that some of the functionality is move to the outside module - but the main focus was not the optimization.

Params here are usually validated for presence (in case there are none at all) - with one exception, __email__ - that is also validated for format by a custom module `EmailParamsValidator`.

Questionable decision that I have made is the way the emails are handled during the update. The mechanism implemented replaces the current set of emails for given contact with those that are provided via params. This is not an ideal solution - the alternative would be merging - but this is also something that would require additional discussion.

Another thing that may look suspicious is `from IPython import embed`. It has been used during the development to enable easy debugging.

### Validation
There is almost no validation at all except for beforementioned email validation. There is no presence requirement for any particular fields for contact, nor there is any special formatting required. It may be the field for discussion. If I were to add the validation I would probably start from extending Marshmallow schemas in __model.py__ as described here: http://marshmallow.readthedocs.io/en/latest/quickstart.html#validation

### Tests
There are two separate files with tests: __validators_test.py__ and __contacts_test.py__. First of them consist of tests for custom email validator and the other consist of the tests for view functions. They can be either run separately or together with __test.sh__. It is just a makeshift solution, as I was supposed to use __nose__ runner (https://nose.readthedocs.io/en/latest/) but I have had some problems with setting it up to on my machine. There is also one helper method in __contacts_test.py__ that should probably be moved outside of __ContactsTestCase__ class, but I have yet to figure out where to put it.

### Seeds
I have used __Flask-script__ in order to prepare a mechanism for seeding the DB. It seemed to be the most reasonable solution that was available out of the box. The mechanism loads the data from __seeds.json__ file and creates objects in the DB.

## Further improvements
~~1. Add pagination to index~~
2. Make sure that query in index is not prone to n+1 query issue
3. Utilize __marshmallow-jsonapi__ (https://github.com/marshmallow-code/marshmallow-jsonapi) in order to deliver JSON:API compliant responses
4. Replace `test.sh` with __nose__ (https://nose.readthedocs.io/en/latest/)
