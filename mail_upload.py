
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from config import imgur_key, mail_sender
import imgur

imgur_client = imgur.Client(imgur_key)

class UploadMailHandler(InboundMailHandler):
  def receive(self, msg):
    logging.info('Received greeting from %s: %s: %s' % (msg.sender,
                                                        msg.body,
                                                        str(msg.attachments)))
    ds = []
    # workaround for issue 2265:
    attachments = None
    if isinstance(msg.attachments, tuple):
      attachments = [msg.attachments]
    else:
      attachments = msg.attachments
    for attachment in attachments:
      (n,p) = attachment
      #FAIL: d = imgur_client.upload(p.decode())
      #TODO: check for base64 encoded payload? is it safe to assume?
      d = imgur_client.upload_b64(p.payload)
      logging.info('Uploaded: %s' % str(d))
      ds.append(d)
    mail.send_mail(sender=mail_sender,
                   to=msg.sender,
                   subject="re:"+msg.subject,
                   body=str(ds))

application = webapp.WSGIApplication(
                                     [UploadMailHandler.mapping()],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

