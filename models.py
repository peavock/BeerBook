"""SQLAlchemy models for Cicerone"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class TriedBeer(db.Model):
    """relationship table of beers tried"""
    __tablename__="beers_tried"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = "cascade"),
        primary_key = True
    )

    beer_id = db.Column(
        db.Text,
        primary_key = True
    )

class Category(db.Model):
    """table of beer category ids and names pre-loaded into app"""
    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key = True
    )    

    name = db.Column(
        db.Text
    )

class Style(db.Model):
    """table of beer style ids and names pre-loaded into app"""
    __tablename__ = "styles"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id')
    )    

    name = db.Column(
        db.Text
    )

class LikedBeer(db.Model):
    """relationship table of beers liked"""
    __tablename__="beers_liked"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = "cascade"),
        primary_key = True
    )

    beer_id = db.Column(
        db.Text,
        primary_key = True
    )

class WishedBeer(db.Model):
    """relationship table of beers user wants to try"""
    __tablename__="beers_wished"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete = "cascade"),
        primary_key = True
    )

    beer_id = db.Column(
        db.Text,
        primary_key = True
    )

class Review(db.Model):
    """reviews and the associated parameters"""

    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    beer_name = db.Column(
        db.Text,
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',ondelete = "cascade"),
        nullable = False
    )

    beer_id = db.Column(
        db.Text,
        nullable = False
    )

    rating = db.Column(
        db.Integer,
        nullable = False
    )

    text = db.Column(
        db.String,
        nullable = False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow()
    )

    author = db.relationship("User")



class User(db.Model):
    """User and the associated parameters"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    username = db.Column(
        db.Text,
        nullable = False,
        unique = True
    )

    password = db.Column(
        db.Text,
        nullable = False
    )


    tried_beer_ids = db.relationship("TriedBeer")

    liked_beer_ids = db.relationship("LikedBeer")

    wished_beer_ids = db.relationship("WishedBeer")

    reviews = db.relationship("Review")

    def number_tried(self):
        """return the number of beers you have tried"""
        return len (self.tried_beer_ids)

    @classmethod
    def signup(cls, username, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username = username,
            password = hashed_pwd
        )

        db.session.add(user)

        return user
        
    @classmethod
    def authenticate(cls, username, password):
        """Find user and authenticate if password is correct"""

        user = cls.query.filter_by(username = username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

        
def connect_db(app):
    """Connect this database to the flask app """

    db.app = app
    db.init_app(app)
