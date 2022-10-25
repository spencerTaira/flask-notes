from re import U
from click import password_option
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Site user """

    __tablename__ = 'users'

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.String(100),
                         nullable=False,
                         unique=True)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register user w/hashed password & return user. """

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, password):
        """ Validate that the user exists and their password is correct.
            If valid, return user. Else, return false.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            # if authenticated, return user instance
            return u
        else:
            return False

# class Note(db.Model)