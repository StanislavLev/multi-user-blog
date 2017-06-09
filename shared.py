import os
import re
from string import letters

import jinja2

# import hmac
import hashlib
import random
import string

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
SALT_NUM = 5


def make_salt():
    return "".join(random.choice(string.letters) for x in xrange(SALT_NUM))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split(",")[1]
    return h == make_pw_hash(name, pw, salt)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


def existing_user(username):
    """
    The function helps to check
    if new username match to existing one when user signup.
    """
    user_query = db.GqlQuery("SELECT * FROM Users_db WHERE username=:user ",
                             user=username)
    user_row = user_query.get()
    if user_row is not None:
        return True
    else:
        return False


def username_password_match(username, password):
    """
    The function helps tho check
    if username and password are match
    to existing in database when user login.
    """
    user_query = db.GqlQuery("SELECT * FROM Users_db WHERE username=:user ",
                             user=username)
    user_row = user_query.get()
    if ((user_row is not None) and
            (valid_pw(username, password, user_row.password))):
        return True
    else:
        return False


# These regexps checks correctness of text, title, username, password, email.
def valid_text(text):
    EMPTY_RE = re.compile(r"^[\s]*$")
    return text and not (EMPTY_RE.match(text))


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)
