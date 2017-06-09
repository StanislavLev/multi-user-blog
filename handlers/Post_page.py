from shared import *
from models.Posts_db import Posts_db
from models.Comments_db import Comments_db
from handlers.BaseHandler import BaseHandler


class Post_page(BaseHandler):
    """
    Post_page handler renders post.html template.
    Checks if registered user or guest visits the page,
    guest have no access to edit, delete, like buttons.
    For valid user checks that cookie from user and generated one are match,
    if no -> goto login page, if yes it displays post with comments
    and options to edit, delete or like/unlike the post.
    "guest" parameter comes from welcome.html
    to point that guest reads the post
    and to hide additional options available for valid users.
    "comment_to_delete_key_id" "delete" "like" "unlike"
    parameters come from post.html
    """
    def get(self, post_key_id):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        guest = self.request.get('guest')
        key = db.Key.from_path('Posts_db', int(post_key_id))
        post = db.get(key)
        if post:
            comments_db = Comments_db.all()\
                            .filter("post_key_id", str(post_key_id))\
                            .order('-created')
            if comments_db.count():
                no_comments = False
            else:
                no_comments = True
            if guest == "guest":
                self.render(
                    'post.html',
                    no_comments=no_comments,
                    guest=guest,
                    post=post,
                    comments_db=comments_db)
            elif self.check_cookie():
                self.render(
                    'post.html',
                    no_comments=no_comments,
                    username=username,
                    post=post,
                    comments_db=comments_db)
            else:
                self.redirect("/login?error=Something went wrong, "
                              "please login.")
        else:
            self.redirect("/login?error=Something went wrong, please login.")

    def post(self, post_key_id):
        user_cookie = self.request.cookies.get('username')
        username = (str(user_cookie))[:-SALT_NUM-1]
        if self.check_cookie():
            comment_to_delete_key_id = self.request.get(
                'comment_to_delete_key_id')
            delete = self.request.get('delete')
            like = self.request.get('like')
            key = db.Key.from_path('Posts_db', int(post_key_id))
            post = db.get(key)
            if post:
                if comment_to_delete_key_id:
                    # if comment_to_delete_key_id is not number
                    # it cause exception in ...int(comment_to_delete_key_id))
                    try:
                        key = db.Key.from_path(
                            'Comments_db', int(comment_to_delete_key_id))
                        comment_to_delete = db.get(key)
                        if (comment_to_delete and
                                comment_to_delete.username == username and
                                comment_to_delete.post_key_id == post_key_id):
                            Comments_db.delete(comment_to_delete)
                            # get function is needed for strong consistency,
                            # otherwise comment can be displayed
                            # some time after deleting
                            Comments_db.get_by_id(
                                int(comment_to_delete_key_id))
                            self.redirect("/post/" + post_key_id)
                        else:
                            self.redirect("/login?error=Something went wrong, "
                                          "please login.")
                    except:
                        self.redirect("/login?error=Something went wrong, "
                                      "please login.")
                elif like == "like" or like == "unlike":
                    if ((username != post.username) and
                            (username not in post.likes) and
                            (username not in post.unlikes)):
                        if like == "like":
                            post.likes.append(str(username))
                        else:
                            post.unlikes.append(str(username))
                        Posts_db.put(post)
                    self.redirect("/post/" + post_key_id)
                elif delete == "delete" and post.username == username:
                    Posts_db.delete(post)
                    # get function is needed for strong consistency,
                    # otherwise post can be displayed some time
                    # after deleting
                    Posts_db.get_by_id(int(post_key_id))
                    all_related_comments = db.GqlQuery(
                        "SELECT * FROM Comments_db WHERE post_key_id=:key ",
                        key=str(post.key().id()))
                    for related_comment in all_related_comments:
                        Comments_db.delete(related_comment)
                    self.redirect("/welcome")
                else:
                    self.redirect("/login?error=Something went wrong, "
                                  "please login.")
            else:
                self.redirect("/login?error=Something went wrong, "
                              "please login.")
