import time
import json
from faker import Faker

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# DATABASE PART
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from models.models import Base, Post

app = Flask(__name__)

# CHANGE AFTER API VERSIONING
CORS(app, resources=r'/*')

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/flask'

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

fake = Faker()

bcrypt = Bcrypt(app)


class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post


post_schema = PostSchema()


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


@app.route('/')
def index():

    response = {
        'success': True,
        'message': 'Hello, From Flask !'
    }

    return jsonify(response)


@app.route('/hello/<name>')
def name(name):

    response = {
        'success': True,
        'message': 'Hello, %s !' % name
    }

    return jsonify(response)


@app.route('/hash/<password>')
def hash(password):

    if password is not None:
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        response = {
            'success': True,
            'plain_text': password,
            'bcrypt': pw_hash
        }
    else:
        response = {
            'success': False,
            'message': 'Please submit a plain text',
        }

    return jsonify(response)


@app.route("/fakes/<numbers>", methods=['GET'])
def add_fake(numbers):
    if numbers is not None:
        try:
            for _ in range(int(numbers)):
                new_post = Post(title=fake.name(), content=fake.text())
                db.session.add(new_post)
                db.session.commit()

            response = {
                'success': True,
                'message': '%s Fakes created' % numbers
            }

        except ValueError:
            response = {
                'success': False,
                'message': 'Please submit a number',
            }

    else:
        response = {
            'success': False,
            'message': "Numbers is not define, please add has url parameter"
        }

    return jsonify(response)


@app.route("/posts", methods=['GET'])
def get_posts():

    posts = db.session.query(Post).all()

    output = []
    for post in posts:
        output.append(post_schema.dump(post).data)

    response = {
        'success': True,
        'posts': output
    }

    return jsonify(response)


@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()

    if post is not None:
        output = post_schema.dump(post).data

        response = {
            'success': True,
            'post': output
        }

    else:
        response = {
            'success': False,
            'message': 'Post not found'
        }

    return jsonify(response)


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
    server_time = time.strftime('%A %B, %d %Y %H:%M:%S')
    return server_time


if __name__ == "__main__":
    app.run(use_debugger=True, use_reloader=True)
