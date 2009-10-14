
from google.appengine.api import urlfetch
import urllib
import base64
from django.utils import simplejson as json

class Client:
  def __init__(self, imgur_key): self.imgur_key = imgur_key

  # upload: imgdata is binary image data
  def upload(self, imgdata):
    return self.upload_b64(base64.b64encode(imgdata))

  # upload: data already b64'd
  def upload_b64(self, b64imgdata):
    payload_data=urllib.urlencode({"key":self.imgur_key, "image":b64imgdata})
    s = urlfetch.fetch("http://imgur.com/api/upload.json", method=urlfetch.POST, payload=payload_data)
    data = json.loads(s.content)
    return data

  # delete
  def delete(self, dhash):
    return json.loads(urlfetch.fetch("http://imgur.com/api/delete/"+dhash+".json"))

  # image stats
  def istats(self, ihash):
    return json.loads(urlfetch.fetch("http://imgur.com/api/stats/"+ihash+".json"))

  # site stats
  def sstats(self, view="all"):
    payload_data=urllib.urlencode({"view":view})
    return json.loads(urlfetch.fetch("http://imgur.com/api/stats.json", payload=payload_data))

  def gallery(self, sort="latest", view="all", count=20, page=1):
    payload_data=urllib.urlencode({"sort":sort, "view":view, "count":count, "page":page})
    return json.loads(urlfetch.fetch("http://imgur.com/api/stats.json", payload=payload_data))

