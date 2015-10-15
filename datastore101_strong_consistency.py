#!/usr/bin/env python
#
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import datetime

import jinja2
import webapp2
from google.appengine.ext import ndb


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Conference(ndb.Model):
    title = ndb.StringProperty()
    city = ndb.StringProperty()
    start_date = ndb.DateProperty(indexed=False)
    end_date = ndb.DateProperty(indexed=False)
    max_attendees = ndb.IntegerProperty()


# TODO 1
#class Ticket(ndb.Model):
#    ticket_number = ndb.IntegerProperty()
#    assigned_to = ndb.StringProperty()
#    available = ndb.StringProperty()
#    conf_key_string = ndb.StringProperty()


# TODO 2
class Ticket(ndb.Model):
    ticket_number = ndb.IntegerProperty()
    assigned_to = ndb.StringProperty()
    available = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        conference_values = {
            "conferences": Conference.query().order(Conference.title)}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(conference_values))


class CreateConference(webapp2.RequestHandler):
    def post(self):
        conference = Conference()
        title = self.request.get('title')
        conference.title = title
        conference.city = self.request.get('city')
        conference.start_date = datetime.datetime.strptime(
            self.request.get('start_date'),
            '%Y-%m-%d').date()
        conference.end_date = datetime.datetime.strptime(
            self.request.get('end_date'),
            '%Y-%m-%d').date()
        max_attendees = int(self.request.get('max_attendees'))
        conference.max_attendees = max_attendees
        key = conference.put()

        """
        TODO 1
        Create Tickets
        """
        #for num in range(1, max_attendees+1):
        #    ticket = Ticket()
        #    ticket.ticket_number = num
        #    ticket.assigned_to = 'user-'+str(num)
        #    ticket.available = 'Available'
        #    ticket.conf_key_string = key.urlsafe()
        #    ticket.put()

        """
        TODO 2
        Create Tickets
        """
        for num in range(1, max_attendees+1):
            ticket = Ticket(parent=key)
            ticket.ticket_number = num
            ticket.assigned_to = 'user-'+str(num)
            ticket.available = 'Available'
            ticket.put()
        self.redirect('/')
class ShowTickets(webapp2.RequestHandler):
    def get(self):
        """
        TODO 1
        Retrieve the Conference Key from Request
        """
        #conf_key_string = self.request.get('conf_key')
        #query = Ticket.query().order(Ticket.ticket_number)
        #filter_query = query.filter(Ticket.conf_key_string == conf_key_string)
        #ticket_values = {"tickets": filter_query}
        #template = jinja_environment.get_template('tickets.html')
        #self.response.out.write(template.render(ticket_values))
        """
        TODO 2
        Retrieve the Conference Key from Request
        """
        conf_key_string = self.request.get('conf_key')
        conf_key = ndb.Key(urlsafe=conf_key_string)
        query = Ticket.query(ancestor=conf_key).order(Ticket.ticket_number)
        ticket_values = {"tickets": query}
        template = jinja_environment.get_template('tickets.html')
        self.response.out.write(template.render(ticket_values))
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create', CreateConference),
    ('/showtickets', ShowTickets)
], debug=True)
