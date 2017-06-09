from shared import *
from models.Posts_db import Posts_db
from handlers.BaseHandler import BaseHandler


class MainPage(BaseHandler):
    """
    MainPage handler called when user open the web site,
    it renders welcome.html page template with guest parameter
    guest parameter passed to post.html and "edit", "delete", "(un)like"
    options are unavailable for not logged in user
    """
    def get(self):
        posts_db = db.GqlQuery("SELECT * FROM Posts_db ORDER BY created DESC")
        self.render("welcome.html", guest="guest", posts_db=posts_db)
