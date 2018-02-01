
# Flask playground

This is a demo version of a flask API with different scenarios.

## Install requirements

Install all dependencies `Flask, SQLAlchemy, PyMySQL, Faker, ...`

```
    pip3 install -r requirements.txt
```

## Mysql database credentials

Edit `app.config['SQLALCHEMY_DATABASE_URI']` with your credentials


## Start the server with autoreload

Start the server wih the command below and go to http://localhost:5000

```
FLASK_APP=main.py FLASK_DEBUG=1 python3 -m flask run
```