from google.appengine.ext import db


class Users_db(db.Model):
    """
    Users_db store all usernames, hashed passwords,
    when username was created and cookie, that will be
    generated and stored each time when user will login.
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    cookie = db.StringProperty(required=True)
