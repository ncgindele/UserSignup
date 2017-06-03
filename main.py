import os

import jinja2
import webapp2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render('mytemplate.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        verify = verify_match(password, verify)
        password = verify_password(password)
        username = verify_username(username)
        email = verify_email(email)
        if verify and password and username and not (email is False):
            self.redirect("/Welcome?username=" + username)
        else:
            self.render('mytemplate.html', username=username, password=password, verify=verify, email=email,)

class WelcomePage(Handler):
    def get(self):
        username = self.request.get('username')
        self.render('welcome.html', username=username)

def verify_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    if USER_RE.match(username):
        return username
    else:
        return False

def verify_password(password):
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    if PASSWORD_RE.match(password):
        return password
    else:
        return False

def verify_match(password, verify):
    if password == verify:
        return verify
    else:
        return False

def verify_email(email):
    if not email:
        return email
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    if EMAIL_RE.match(email):
        return email
    else:
        return False

app = webapp2.WSGIApplication([('/', MainPage), ('/Welcome', WelcomePage)], debug=True)
