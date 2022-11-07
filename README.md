# Pet-project on Fast-API: notes | posts
This API service provides the ability to create personal notes with the ability to edit them, public posts visible to 
other users of the platform, as well as a system for subscribing to users and adding them to friends (whose posts will be displayed on the home page).

### Main functionality:
* **Registration and authorization of users**
* **Create personal notes and public posts**
* **Editing private notes and public posts**
* **System of subscriptions and friends**
* **Demo admin-panel (refinement of table links in the database is required)**

### Requirements
* Language: **Python 3.10**
* Framework: **FastAPI**
* ORM: **SQLAlchemy**
* Database: **PostgreSQL**

## Installation
Install requirements:

    pip install -r requiremets

Before creating a database and running the project, you need to configure the database access parameters and the secret 
key for hashing user passwords in a file:

* `config.py`

Fill in the following fields in file config.py:

        DB_USER = 'user_name'
        DB_PASSWORD = 'your_password'
        DB_HOST = 'your_host'
        DB_NAME = 'your_db_name'


Secret-key for hashing user password:

    SECRET_KEY = 'secret'

## Application launch
After installing all the necessary dependencies and parameters, first run the database creation script in the path:

* `scripts/create_db.py`

###### Or use alembic migrations.

And then run the app itself on the path:

* `app/main.py`

###### Or use the terminal, the command to run the application:

    uvicorn app.main:app
