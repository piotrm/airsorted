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
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/api/v1/contacts
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
### Structure
### Models
### Views
### Tests
### Seeds

## Further improvements
1. Utilize __marshmallow-jsonapi__ (https://github.com/marshmallow-code/marshmallow-jsonapi) in order to deliver JSON:API compliant responses
2. Replace `test.sh` with __nose__ (https://nose.readthedocs.io/en/latest/)
3. Refactor
