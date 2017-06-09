from shared import *
from models.Users_db import Users_db
from handlers.BaseHandler import BaseHandler


class Signup(BaseHandler):
    """
    Signup handler renders signup-form.html,
    checks correctness of new username and password.
    """
    def get(self):
        self.render("signup-form.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username,
                      email=email)

        if existing_user(username):
            params['error_username'] = ("This username already exists, "
                                        "please chose another one")
            have_error = True
        elif not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)
        # if password username and email are correct then generated
        # cookie is sent to user and saved in Users_db for
        # future comparison till user logout
        else:
            salt_for_pw = make_salt()
            salt_for_cookie = make_salt()
            pw_hash = make_pw_hash(username, password, salt_for_pw)
            users_db = Users_db(username=username, password=pw_hash,
                                cookie=salt_for_cookie)
            users_db.put()
            # get function is needed for strong consistency:
            # to be able get all users (including the new created one)
            # in Welcome handler (check_cookie func)
            users_db.get(users_db.key())
            self.response.headers.add_header('Set-Cookie', 'username=%s|%s' %
                                             (str(username), salt_for_cookie))
            self.redirect('/welcome')
