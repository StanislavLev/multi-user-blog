from shared import *
from models.Posts_db import Posts_db
from handlers.BaseHandler import BaseHandler


class Edit_post(BaseHandler):
    """
    Edit_post handler renders edit_post.html template.
    Checks that cookie from user and generated one are match,
    if no -> goto login page, if yes it checks for not empty title and post
    and save them in datastore,
    otherwise ask from user to fill both post and title.
    "key_id_to_edit" parametr comes from post.html when user want to edit
    his post, "edited..." parameters come from edit_post.html after editing.
    """
    def post(self):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            key_id_to_edit = self.request.get('key_id_to_edit')
            edited_key_id = self.request.get('edited_key_id')
            edited_post = self.request.get('edited_post')
            edited_title = self.request.get('edited_title')
            if key_id_to_edit:
                key = db.Key.from_path('Posts_db', int(key_id_to_edit))
                post_to_edit = db.get(key)
                if post_to_edit:
                    self.render("edit_post.html", post_to_edit=post_to_edit)
                else:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            elif (valid_text(edited_post) and valid_text(edited_title) and
                  edited_key_id):
                key = db.Key.from_path('Posts_db', int(edited_key_id))
                post = db.get(key)
                if post and post.username == username:
                    post.title = edited_title
                    post.post = edited_post
                    post.put()
                    # get function is needed for strong consistency:
                    # to see edited post updated
                    post = Posts_db.get(post.key())
                    self.redirect("/post/" + str(post.key().id()))
                else:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            else:
                key = db.Key.from_path('Posts_db', int(edited_key_id))
                post_to_edit = db.get(key)
                if post_to_edit:
                    self.render(
                        "edit_post.html",
                        edited_post=edited_post,
                        edited_title=edited_title,
                        edited_key_id=edited_key_id,
                        error="You have to fill both: Post and Title."
                              "Please try again.")
                else:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
        else:
            self.redirect("/login?error=Something went wrong, please login.")
