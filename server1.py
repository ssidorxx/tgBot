from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bdBot.db"
db = SQLAlchemy(app)
with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)

# def create_app():
#     app = Flask(__name__)
#
#     with app.app_context():
#         app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bdBot.db"
#
#     return app
# create_app()
#
# def create_app():
#     app = Flask(__name__)
#
#     with app.app_context():
#         init_db()
#
#     return app


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.id


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Subscription %r>' % self.id