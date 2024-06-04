from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
#from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(400))
    username = db.Column(db.String(400), unique=True, nullable=False)
    _password = db.Column(db.String(400), nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=True)
    user_type = db.Column(db.String(400))

# class User(db.Model, UserMixin):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     fullname = db.Column(db.String(100))
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     _password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=True)
#     user_type = db.Column(db.String(50))

    # __mapper_args__ = {
    #     "polymorphic_identity": "user",
    #     "polymorphic_on": "user_type",
    # }

    @property
    def password(self):
        return AttributeError("Write-Only Field")

    @password.setter
    def password(self, passwrd):
        self._password = generate_password_hash(passwrd)

    def match_password(self, passwrd):
        return check_password_hash(self._password, passwrd)




class Key(db.Model):
    __tablename__ = "keys"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(400), db.ForeignKey("users.username"), nullable=False)
    e = db.Column(db.String(400), nullable=False)
    d = db.Column(db.String(400), nullable=False)
    n = db.Column(db.String(400), nullable=False)
    