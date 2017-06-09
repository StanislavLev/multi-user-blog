from google.appengine.ext import db


class Comments_db(db.Model):
    """The db.model stores comments related information."""
    username = db.StringProperty(required=True)
    post_key_id = db.StringProperty(required=True)
    post_comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_updated = db.DateTimeProperty(auto_now=True)

    def comment_nl2br(self):
        """The func helps to render new line in jinja2 templates."""
        return self.post_comment.replace('\n', '<br>')
