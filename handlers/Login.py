from shared import *
from models.Users_db import Users_db
from handlers.BaseHandler import BaseHandler


class Login(BaseHandler):
    """
    Login handler render login.html tamplate, if username and password
    are match cookie for user is generated and saved in Users_db for
    future comparison till user logout.
    User is forwarded to welcome page is password and username are match,
    otherwise to login page with error msg
    """
    def get(self):
        error = self.request.get('error')
        self.render("login.html", error=error)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        if username_password_match(username, password):
            user_query = db.GqlQuery("SELECT * FROM Users_db "
                                     "WHERE username=:user ", user=username)
            user = user_query.get()
            salt_for_cookie = make_salt()
            user.cookie = salt_for_cookie
            user.put()
            self.response.headers.add_header('Set-Cookie', 'username=%s|%s' %
                                             (str(username), salt_for_cookie))
            self.redirect('/welcome')
        else:
            self.render("login.html", error=("Invalid password or username, "
                        "please try again. New user please signup."))
