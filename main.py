import time
from faker import Faker
# from pprint import pprint

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from models import Base, Posts

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/flask'
db = SQLAlchemy(app)

fake = Faker()


@app.before_first_request
def setup():
    print('BEFORE APP START \n')
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)

    for _ in range(10):
        new_post = Posts(title=fake.name(), content=fake.text())
        db.session.add(new_post)
        db.session.commit()

    print('ADD SOME FAKE CONTENT \n\n')


@app.route('/')
def index():
    return 'Hello, Flask!'


@app.route('/<name>')
def name(name):
    return 'Hello! %s' % name


@app.route("/sleep")
def req():
    t = request.values.get('t', 0)
    time.sleep(float(t))  # just to show it works...
    return 'Hello, %s!' % t


@app.route("/posts")
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
