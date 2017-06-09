from shared import *
from models.Comments_db import Comments_db
from handlers.BaseHandler import BaseHandler


class Edit_comment(BaseHandler):
    """
    Edit_comment handler renders edit_comment.html template.
    Checks that cookie from user and generated one are match,
    if no -> goto login page, if yes it checks for not empty comment
    and save it in datastore,
    otherwise ask from user to write not empty comment.
    "comment_to_edit_key_id" parameter comes from post.html
    when user want to edit his comment
    "edited_comment_text" and "edited_comment_key_id"
    comes from edit_comment.html after editing
    """
    def post(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            edited_comment_text = self.request.get('edited_comment_text')
            comment_to_edit_key_id = self.request.get(
                'comment_to_edit_key_id')
            edited_comment_key_id = self.request.get('edited_comment_key_id')
            if comment_to_edit_key_id:
                # if comment_to_edit_key_id is not number
                # it cause exception in ...int(comment_to_edit_key_id))
                try:
                    key = db.Key.from_path(
                        'Comments_db', int(comment_to_edit_key_id))
                    comment_to_edit = db.get(key)
                    if comment_to_edit:
                        self.render(
                            "edit_comment.html",
                            comment_to_edit=comment_to_edit)
                    else:
                        self.redirect("/login?error=Something went wrong, "
                                      "please login.")
                except:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            elif valid_text(edited_comment_text) and edited_comment_key_id:
                # if edited_comment_key_id is not number
                # it cause exception in ...int(edited_comment_key_id))
                try:
                    key = db.Key.from_path(
                        'Comments_db', int(edited_comment_key_id))
                    comment_to_edit = db.get(key)
                    if ((comment_to_edit) and
                            (comment_to_edit.username == username)):
                        # if comment_to_edit.post_key_id is not number
                        # it cause exception in
                        # ...int(comment_to_edit.post_key_id))
                        try:
                            key = db.Key.from_path(
                                'Posts_db', int(comment_to_edit.post_key_id))
                            post = db.get(key)
                            if post:
                                comment_to_edit.post_comment = \
                                    edited_comment_text
                                comment_to_edit.put()
                                # get func is needed for strong consistency:
                                # to see edited comment updated
                                comment_to_edit = Comments_db.get(
                                    comment_to_edit.key())
                                self.redirect(
                                    "/post/" + comment_to_edit.post_key_id)
                            else:
                                self.redirect("/login?error=Something went "
                                              "wrong, please login.")
                        except:
                            self.redirect("/login?error=Something went wrong, "
                                          "please login.")
                    else:
                        self.redirect("/login?error=Something went wrong, "
                                      "please login.")
                except:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            else:
                self.render(
                    "edit_comment.html",
                    edited_comment_key_id=edited_comment_key_id,
                    error="You can`t create empty comment. Please try again.")
        else:
            self.redirect("/login?error=Something went wrong, please login.")
