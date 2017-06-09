from shared import *
from models.Users_db import Users_db
from models.Posts_db import Posts_db
from handlers.BaseHandler import BaseHandler


class Welcome(BaseHandler):
    """
    Welcome handler renders welcome.html template with valid username.
    If username cookie not math to saved one, user is forwarded to login page.
    If user want to logout, new cookie generated and saved in Users_db,
    empty cookie is sent in header.
    Logout form appears on pages when user logged in.
    """
    def get(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            posts_db = db.GqlQuery("SELECT * FROM Posts_db "
                                   "ORDER BY created DESC")
            self.render('welcome.html', username=username, posts_db=posts_db)
        else:
            self.redirect("/login?error=Something went wrong, please login.")

    def post(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            logout = self.request.get('logout')
            if logout == "logout":
                user_query = db.GqlQuery("SELECT * FROM Users_db WHERE "
                                         "username=:user ", user=username)
                user = user_query.get()
                salt_for_cookie = make_salt()
                user.cookie = salt_for_cookie
                user.put()
                self.response.headers.add_header(
                    'Set-Cookie', 'username=%s|%s' % (str(username), ""))
                self.redirect('/')
            else:
                self.redirect("/welcome")
        else:
            self.redirect("/login?error=Something went wrong, please login.")
