import time
from faker import Faker

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# DATABASE MODELS
from models.models import Base, Posts

app = Flask(__name__)

# CHANGE AFTER API VERSIONING
CORS(app, resources=r'/*')

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/flask'

db = SQLAlchemy(app)

fake = Faker()

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return 'Hello, From Flask!'


@app.route('/<name>')
def name(name):
    return 'Hello! %s' % name


@app.route('/hash/<password>')
def hash(password):
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return u"".join([u"Hashing <strong> {0} </strong>  with BCRYPT and got =>  <strong> {1} </strong>".format(password, pw_hash)])


@app.route("/fakes", methods=['GET'])
def add_fake():
    if 'numbers' in request.args:
        numbers = request.args.get('numbers', 0)

        try:
            for _ in range(int(numbers)):
                new_post = Posts(title=fake.name(), content=fake.text())
                db.session.add(new_post)
                db.session.commit()
            return "%s posts added" % numbers

        except ValueError:
            return "Numbers must be and Integer"

    else:
        return "Numbers is not define, please add has url parameter"


@app.route("/posts", methods=['GET'])
def get_posts():
    posts = db.session.query(Posts).all()
    return u"<br>".join([u"<h2> {0} </h2 > <p> {1} </p>".format(post.title, post.content) for post in posts])


@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.query(Posts).filter_by(id=post_id).first()

    if post is not None:
        return u"<br>".join([u"<h2> {0} </h2 > <p> {1} </p>".format(post.title, post.content)])
    else:
        return "Post not Found"


@app.route("/for_test", methods=['GET'])
def for_test():
    if 'sheep' in request.args:
        z = request.args.get('sheep', 0)

        try:
            for x in range(0, int(z)):
                print("%d sheep" % (x + 1))

            return "Counted %s sheeps, Have a good night ! " % z

        except ValueError:
            return "sheep is not an integer"

    else:
        return "sheep is not define"


@app.route("/getTime", methods=['GET'])
def get_time():
    print("server time : ", time.strftime('%A %B, %d %Y %H:%M:%S'))
    return "Done"


if __name__ == "__main__":
    app.run(use_debugger=True, use_reloader=True)
