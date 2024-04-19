from flask_login import UserMixin
from .base import db
from enum import Enum

class oAuthProviders(Enum):
    GOOGLE = 1
    AZURE  = 2 

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id        = db.Column(db.String(), primary_key=True, index=True)
    name      = db.Column(db.String(64), nullable=False)
    google_email = db.Column(db.String(64), unique=True, index=True)
    azure_email  = db.Column(db.String(64), unique=True, index=True)
    profile_pic  = db.Column(db.String(256), nullable=True)

    main_oauth_provider = db.Column(db.Enum(oAuthProviders), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def __init__(self, id_, name, google_email, azure_email = None, profile_pic = None):
        self.id        = id_
        self.name      = name
        self.google_email = google_email
        self.azure_email  = azure_email
        self.profile_pic = profile_pic

    def __repr__(self):
        """ this function is used to print the object in a more readable format; just ignore it """
        return f"User({self.id}, name={self.name}, g_mail={self.google_email}, a_mail={self.azure_email})"

    def __str__(self):
        return self.__repr__()

