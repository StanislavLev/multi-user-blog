from shared import *
from models.Posts_db import Posts_db
from handlers.BaseHandler import BaseHandler


class New_post(BaseHandler):
    """
    New_post handler renders new_post.html template.
    Checks that cookie from user and generated one are match,
    if no -> goto login page, if yes it checks for not empty title and post
    and save them in datastore,
    otherwise ask from user to fill both post and title.
    "new" parameter comes from welcome.html if user want to create new post,
    "post"and "title" from new_post.html, after user create new post.
    """
    def post(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            new = self.request.get('new')
            post = self.request.get('post')
            title = self.request.get('title')
            if new:
                self.render("new_post.html")
            elif valid_text(post) and valid_text(title):
                new_post = Posts_db(
                    username=username,
                    title=title,
                    post=post,
                    likes=[],
                    unlikes=[])
                new_post.put()
                # get function is needed for strong consistency:
                # to see all posts(including the new one) in welcome page
                new_post = Posts_db.get(new_post.key())
                self.redirect("/post/" + str(new_post.key().id()))
            else:
                self.render(
                    "new_post.html",
                    username=username,
                    post=post,
                    title=title,
                    error="You have to fill both: Post and Title."
                          "Please try again.")
        else:
            self.redirect("/login?error=Something went wrong, please login.")
