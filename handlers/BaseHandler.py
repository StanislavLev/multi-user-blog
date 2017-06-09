import webapp2
from shared import *
from models.Users_db import Users_db


class BaseHandler(webapp2.RequestHandler):
    """
    All web page handlers will check that cookie from user and generated when
    user logged in are the same, check_cookie function will help with that.
    """
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def check_cookie(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        user_exists = Users_db.all().filter("username", username).count()
        if user_exists:
            user_key = db.GqlQuery(
                "SELECT * FROM Users_db WHERE username=:user ",
                user=username).get().key()
            user = Users_db.get(user_key)
            return user_cookie[-SALT_NUM:] == user.cookie
        return False
