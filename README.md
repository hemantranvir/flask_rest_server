# Flask RESTful Server
## Installation
  - Install python3, pipenv and postgresql
  - Clone the repository
  - Go to the project directory `$ cd /flask_rest_server`
  - Activate the project virtual environment with `$ pipenv shell` command
  - Install all required dependencies with `$ pipenv install`
  - Create database
    ```
    $ sudo -u postgres createdb customer_db
    $ sudo -u postgres psql -c "create user test with password 'test'"
    $ sudo -u postgres psql -c "grant all privileges on database customer_db to test"
    ```
  - Create tables
    ```
    $ python3 manage.py db init
    $ python3 manage.py db migrate
    $ python3 manage.py db upgrade
    ```
  - Export the required environment variables
      ```
      $ export TARGET_ENV=development
      $ export DATABASE_URL=postgres://name:password@localhost:5432/customer_db
      $ export JWT_SECRET_KEY=ghkjghgkjhfkhgkh
      ```
  - Start the app with `python run.py`
