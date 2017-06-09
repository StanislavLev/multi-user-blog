from google.appengine.ext import db


class Posts_db(db.Model):
    """The db.model stores posts related information."""
    username = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    post = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_updated = db.DateTimeProperty(auto_now=True)
    likes = db.StringListProperty(required=True)
    unlikes = db.StringListProperty(required=True)

    def post_nl2br(self):
        """The func helps to render new line in jinja2 templates."""
        return self.post.replace('\n', '<br>')
