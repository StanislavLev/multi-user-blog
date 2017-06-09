import os
import re
from string import letters

import webapp2
import jinja2

# import hmac
import hashlib
import random
import string

from google.appengine.ext import db

from shared import *

from models.Users_db import Users_db
from models.Posts_db import Posts_db
from models.Comments_db import Comments_db

from handlers.BaseHandler import BaseHandler
from handlers.Signup import Signup
from handlers.Login import Login
from handlers.MainPage import MainPage
from handlers.Welcome import Welcome
from handlers.New_post import New_post
from handlers.Edit_post import Edit_post
from handlers.Add_comment import Add_comment
from handlers.Edit_comment import Edit_comment
from handlers.Post_page import Post_page


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', Login),
    ('/signup', Signup),
    ('/welcome', Welcome),
    ('/new_post', New_post),
    ('/edit_post', Edit_post),
    ('/add_comment', Add_comment),
    ('/edit_comment', Edit_comment),
    ('/post/([0-9]+)', Post_page)
], debug=True)
