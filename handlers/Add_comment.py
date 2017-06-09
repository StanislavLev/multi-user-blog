from shared import *
from models.Comments_db import Comments_db
from handlers.BaseHandler import BaseHandler


class Add_comment(BaseHandler):
    """
    Add_comment handler renders add_comment.html template.
    Checks that cookie from user and generated one are match,
    if no -> goto login page, if yes it checks for not empty comment
    and save it in datastore,
    otherwise ask from user to write not empty comment.
    "post_to_comment_key_id" parameter comes from post.html
    if user choses to add comment
    "new_comment_text" and "commented_post_key_id"
    come after adding comment from add_comment.html
    """
    def post(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            post_to_comment_key_id = self.request.get(
                'post_to_comment_key_id')
            new_comment_text = self.request.get('new_comment_text')
            commented_post_key_id = self.request.get('commented_post_key_id')
            if post_to_comment_key_id:
                # if post_to_comment_key_id is not number
                # it cause exception in ...int(post_to_comment_key_id))
                try:
                    key = db.Key.from_path(
                        'Posts_db', int(post_to_comment_key_id))
                    post = db.get(key)
                    if post:
                        self.render(
                            "add_comment.html",
                            post_to_comment_key_id=str(
                                post_to_comment_key_id))
                    else:
                        self.redirect("/login?error=Something went wrong, "
                                      "please login.")
                except:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            elif valid_text(new_comment_text):
                # if commented_post_key_id is not number
                # it cause exception in ...int(commented_post_key_id))
                try:
                    key = db.Key.from_path(
                        'Posts_db', int(commented_post_key_id))
                    post = db.get(key)
                    if post:
                        added_comment = Comments_db(
                            username=username,
                            post_key_id=str(commented_post_key_id),
                            post_comment=new_comment_text)
                        added_comment.put()
                        # get function is needed for strong consistency:
                        # to see all comments(including the new one)
                        added_comment = Comments_db.get(added_comment.key())
                        self.redirect("/post/" + commented_post_key_id)
                    else:
                        self.redirect("/login?error=Something went wrong, "
                                      "please login.")
                except:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            else:
                self.render(
                    "add_comment.html",
                    post_to_comment_key_id=str(commented_post_key_id),
                    error="You can`t create empty comment. Please try again.")
        else:
            self.redirect("/login?error=Something went wrong, please login.")
