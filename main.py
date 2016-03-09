
# import DataStore
from google.appengine.ext import ndb
import webapp2
import jinja2
import logging
import os
# so we can find the location of the template directory
# define data model using ndb.Model library we want the name of the user the message and a time stamp.
import collections

from stage1_dict import stage1
from stage2_dict import stage2
from stage3_dict import stage3
from stage4_dict import stage4
from stage5_dict import stage5

template_dir = os.path.join(os.path.dirname(__file__), "templates")


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def valid_user_name(user_name):
    if user_name and len(user_name) > 2:
        cap_user_name = user_name.capitalize()
        return cap_user_name

def valid_message(message):
    if message and len(message) > 2:
        min_cap_message = message.capitalize()
        if len(min_cap_message) < 150:
            max_min_cap_message = min_cap_message
            return max_min_cap_message

# Comment properties
class Comments(ndb.Model):
    name = ndb.StringProperty(required=True)
    message = ndb.TextProperty(required=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

# This is the Main Class - Helper functions to Handler Class for rendering templates

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
# returns a string
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
# renders string to the browser
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# function get that handles get requests and writes the response ()
class MainHandler(Handler):
    def get(self):
        user_name_input = valid_user_name(self.request.get("user_name"))
        user_comment_input = valid_message(self.request.get("message"))

        if not (user_name_input and user_comment_input):
            self.response.out.write("/")
        else:
            self.response.out.write("Thanks for taking the time to comment!")

    # def write_form(error=""):
    #     self.response.out.write("/" % {"error": error})

    def get(self):
        # define the number of comments you want to show on the page
        num_comments = 6
         #Get results from the Datastore and list them in reverse order, most recent on top.
        results = Comments.query().order(-Comments.timestamp).fetch(num_comments)
        # render the template with results from the datastore
        self.render("index.html", comments = results)


class CommentsHandler(Handler):
    def post(self):
        user_name = self.request.get("user_name")
        message = self.request.get("message")
        if len(user_name) < 2 or len(message) < 2:
            self.response.out.write("/")
        Comments(name=user_name, message=message).put()

        self.redirect("/")


class Stage1Handler(Handler):
    def get(self):
        self.render("stage1.html", stage1 = stage1, title = "Stage 1")

class Stage2Handler(Handler):
    def get(self):
        self.render("stage2.html", stage2 = stage2,  title = "Stage 2")

class Stage3Handler(Handler):
    def get(self):
        self.render("stage3.html", stage3 = stage3,  title = "Stage 3")

class Stage4Handler(Handler):
    def get(self):
        self.render("stage4.html", stage4 = stage4,  title = "Stage 4")

class Stage5Handler(Handler):
    def get(self):
        self.render("stage5.html", stage5 = stage5,  title = "Stage 5")

class AboutHandler(Handler):
    def get(self):
        self.render("about.html", stage5 = stage5, title = "About Page")

class ContactHandler(Handler):
    def get(self):
        self.render("contact.html", stage1 = stage1, title = "Contact Page")

class OldNotesHandler(Handler):
    def get(self):
        self.render("contact.html", stage1 = stage1, title = "Contact Page")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    # ('/comments_list.html', CommentsHandler),
    ('/comments', CommentsHandler),
    ('/stage1.html', Stage1Handler),
    ('/stage2.html', Stage2Handler),
    ('/stage3.html', Stage3Handler),
    ('/stage4.html', Stage4Handler),
    ('/stage5.html', Stage5Handler),
    ('/about.html', AboutHandler),
    ('/contact.html', ContactHandler),
    ('/static/oldipndnotes.html', OldNotesHandler)
], debug=True)
