
import os

import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import imgur

from config import imgur_key

imgur_client = imgur.Client(imgur_key)

class HomePageHandler(webapp.RequestHandler):

  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'upload.html')
    self.response.out.write(template.render(path, {}))

  def post(self):
    imgdata = self.request.get("img")
    data = imgur_client.upload(imgdata)
    path = os.path.join(os.path.dirname(__file__), 'uploaded.html')
    self.response.out.write(template.render(path, {"data":data}))

application = webapp.WSGIApplication(
                                     [('/', HomePageHandler)],
                                     debug=False)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()


