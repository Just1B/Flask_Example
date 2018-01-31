
## Requirements

Install all dependencies `Flask, SQLAlchemy, PyMySQL, Faker`

```
    pip3 install -r requirements.txt
```

## Mysql Database Credentials

Edit `app.config['SQLALCHEMY_DATABASE_URI']` with your credentials


## Start Server with Autoreload

Start the server and go to http://localhost:5000

```
FLASK_APP=main.py FLASK_DEBUG=1 python -m flask run
```