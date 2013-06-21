#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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

import cgi
import webapp2

form="""
<form method="POST">
    What is your birthday ?
    <br>
    <div style="color: red">%(error)s</div>
    <label>Month<input type="text" name="month" value="%(month)s"></label>
    <label>Day<input type="text" name="day" value="%(day)s"></label>
    <label>Year<input type="text" name="year" value="%(year)s"></label>
    <br>
    <br>
    <input type="submit">
</form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):
    month = month.lower()
    for e in months:
        if month == e.lower():
            return e
    return None


def valid_day(day):
    try:
        if 0 < int(day) <= 31:
            return int(day)
    except ValueError:
        return None


def valid_year(year):
    if year and year.isdigit():
        if 1900 < int(year) < 2020: 
            return int(year)
    return None


def escape_html(string):
    return cgi.escape(string, quote = True)


navigations = ['<a href="/">Home (Unit 1)</a>', '<a href="/unit2/forms">Forms (Unit 2)</a>',
        '<a href="/unit2/rot13">ROT13 (Unit 2)</a>', '<a href="/unit2/login">Login</a>']


def navbar():
    string = ''
    for e in navigations:
        string += e
        string += '|'
    return string+'<br>'


class Lesson1Handler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(navbar())
        self.response.write('Hello, Udacity')



class Lesson2Handler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.write(navbar())
        self.response.out.write(form % { 'error': error,
            'month': escape_html(month),
            'day': escape_html(day),
            'year': escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("This does not look valid to me.", user_month, user_day, user_year)
        else:
            self.redirect('/unit2/thanks')



class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(navbar())
        self.response.write("Thanks! Thats a totally valid day")


html = """
<!doctype html>
<html>
<head>
    <title> Unit 2 ROT13 </title>
</head>
<body>
    <h2>Enter some text to ROT13</h2>
    <form method="POST">
        <textarea name="text" style="style="height: 100px; width: 400px;">%(value)s</textarea>
        <br>
        <input type="submit">
    </form>
</body>
</html>
"""

class ROT13Handler(webapp2.RequestHandler):
    def write_html(self, value=''):
        self.response.write(navbar())
        self.response.out.write(html % {'value': value,})

    def get(self):
        self.write_html()

    def post(self):
        string = self.request.get('text')
        self.write_html(string.encode('rot13'))



login_form = """
<!doctype html>
<html>
<head>
</head>
<body>
    <form method="POST">
        <label>Name<input type="text" name="name"></label><br>
        <label>Password<input type="password" name="password1"></label><br>
        <label>Verify Password<input type="password" name="password2"></label><br>
        <label>Email (optional) <input type="email" name="email"></label><br>
        <input type="submit">
    </form>
</body>
</html>
"""

class SignUpHandler(webapp2.RequestHandler):
    def write_loginform(self):
        self.response.out.write(login_form)

    def get(self):
        self.write_loginform()

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/', Lesson1Handler),
    ('/unit2/forms', Lesson2Handler),
    ('/unit2/thanks', ThanksHandler),
    ('/unit2/rot13', ROT13Handler),
    ('/unit2/login', SignUpHandler),
], debug=True)

