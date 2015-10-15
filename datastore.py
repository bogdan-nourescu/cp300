import jinja2
import os
import webapp2
import datetime
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), 
		extensions=['jinja2.ext.autoescape'], 
		autoescape=True)


class Conference(ndb.Model):
    title = ndb.StringProperty()
    city = ndb.StringProperty()
    startdate = ndb.DateProperty(indexed=False)
    enddate = ndb.DateProperty(indexed=False)
    maxAttendees = ndb.IntegerProperty()
	
	
class MainPage(webapp2.RequestHandler):
    def get(self):
        conference_values ={"conferences":Conference.query().order(Conference.title)}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(conference_values))

class CreateConference(webapp2.RequestHandler):
    def post(self):
        conference = Conference()
        conference.title = self.request.get('title')
        conference.city = self.request.get('city')
        conference.startdate = datetime.datetime.strptime(self.request.get('startdate'), '%Y-%m-%d').date()
        conference.enddate = datetime.datetime.strptime(self.request.get('enddate'), '%Y-%m-%d').date()
        conference.maxAttendees = int(self.request.get('maxAttendees'))
        conference.put()
        self.redirect('/')
application = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/create', CreateConference),
], debug=True)
