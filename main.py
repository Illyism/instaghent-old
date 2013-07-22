# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os
from instagram import client, subscriptions
from instaghent import i18n, instaghent
import codecs
import simplejson as json

import logging
import urllib
import urllib2
from google.appengine.api import urlfetch
from google.appengine.api import memcache


CONFIG = {
    'client_id': 'a5a67115f0fc45d6b97d318ac915aa91',
    'client_secret': '76458a657e8c4317a32ebb9b8b224219',
    'redirect_uri': 'http://localhost:8002/oauth_callback'
}


api = client.InstagramAPI(**CONFIG)

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        language = self.request.headers.get('accept_language') or "en";
        photos = instaghent.fetchImages();
        template_values = {
            'i18n': i18n.get(language),
            "sortingMethod": "time",
            "photos": photos
        }
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(template_values))

class MorePages(webapp2.RequestHandler):
    def get(self, sortingMethod, page):
        photos = instaghent.fetchPage(sortingMethod, page)
        template = jinja_environment.get_template('templates/photos.json')
        template_values = {
            "photos": json.dumps(photos)
        }
        self.response.out.write(template.render(template_values))

class MainFilterPage(webapp2.RequestHandler):
    def get(self, filt):
        language = self.request.headers.get('accept_language') or "en";
        photos = instaghent.fetchImages(filt);
        template_values = {
            'i18n': i18n.get(language),
            "sortingMethod": filt,
            "photos": photos
        }
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(template_values))

class FiestePage(webapp2.RequestHandler):
    def get(self):
        language = self.request.headers.get('accept_language') or "en";
        photos = instaghent.fetchFieste();
        template_values = {
            'i18n': i18n.get(language),
            "sortingMethod": "tag",
            "photos": photos
        }
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(template_values))

class MoreFieste(webapp2.RequestHandler):
    def get(self, page):
        photos = instaghent.fetchFiestePage("tag", "gf13", page)
        template = jinja_environment.get_template('templates/photos.json')
        template_values = {
            "photos": json.dumps(photos)
        }
        self.response.out.write(template.render(template_values))

class MapPage(webapp2.RequestHandler):
    def get(self):
        language = self.request.headers.get('accept_language') or "en";
        photos = instaghent.fetchLocation()
        template_values = {
            'photos': photos,
            'i18n': i18n.get(language)
        }

        template = jinja_environment.get_template('templates/map.html')
        self.response.out.write(template.render(template_values))

class AboutPage(webapp2.RequestHandler):
    def get(self):
        language = self.request.get("Accept-Language") or "en";
        template_values = {
            'i18n': i18n.get(language),
        }

        template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(template.render(template_values))

# Shots & Author

class ShotPage(webapp2.RequestHandler):
    def get(self, authorname, photoid):
        language = self.request.headers.get('accept_language') or "en";
        photo = instaghent.fetchImage(photoid)
        title =  authorname + " | "
        tags = eval(photo["tags"])
        if (photo["caption"]):
            title = title +  photo["caption"] + " | "
        template_values = {
            'i18n': i18n.get(language),
            "sortingMethod": "author",
            "author": authorname,
            "title": title,
            "photo": photo,
            "tags": tags,
            "ghentmeter": int(photo["ghents"]) + int(photo["likes"]) 
        }
        template = jinja_environment.get_template('templates/detail.html')
        self.response.out.write(template.render(template_values))

class AuthorPage(webapp2.RequestHandler):
    def get(self, authorname):
        language = self.request.headers.get('accept_language') or "en";
        photos = instaghent.fetchbyAuthor(authorname)
        for photo in photos:
            if "tags" in photo:
                photo["tags"] = eval(photo["tags"])
        template_values = {
            'i18n': i18n.get(language),
            "sortingMethod": "author",
            "photos": photos,
            "profile_picture": photos[0]["profile_picture"],
            "author": authorname,
            "title": authorname + " | "
        }
        template = jinja_environment.get_template('templates/author.html')
        self.response.out.write(template.render(template_values))


class ShotJSON(webapp2.RequestHandler):
    def get(self, author, photoid):
        photo = instaghent.fetchImage(photoid)
        template = jinja_environment.get_template('templates/photo.json')
        template_values = {
            "photo": instaghent.fetchImage(photoid)
        }
        self.response.out.write(template.render(template_values))

class AuthorJSON(webapp2.RequestHandler):
    def get(self, authorname):
        photos = instaghent.fetchbyAuthor(authorname)
        
        template = jinja_environment.get_template('templates/photos.json')
        template_values = {
            "photos": json.dumps(photos),
            "author": authorname
        }
        self.response.out.write(template.render(template_values))




class Upghent(webapp2.RequestHandler):
    def get(self, photoid):
        photo = instaghent.fetchImage(photoid)
        template = jinja_environment.get_template('templates/photo.json')
        template_values = {
            "photo": instaghent.fetchImage(photoid)
        }
        self.response.out.write(template.render(template_values))
    def post(self, photoid):
        self.response.out.write(instaghent.upGhentImage(photoid))

class Downghent(webapp2.RequestHandler):
    def get(self, photoid):
        photo = instaghent.fetchImage(photoid)
        template = jinja_environment.get_template('templates/photo.json')
        template_values = {
            "photo": instaghent.fetchImage(photoid)
        }
        self.response.out.write(template.render(template_values))
    def post(self, photoid):
        self.response.out.write(instaghent.downGhentImage(photoid))

class RedirectToMain(webapp2.RequestHandler):
    def get(self, photoid):
        self.response.out.write(jinja_environment.get_template('redirect.html').render({"redirect":"/"}))


class RealTime(webapp2.RequestHandler):
    def get(self):
        #    curl -F 'client_id=CLIENT-ID' \
        #    -F 'client_secret=CLIENT-SECRET' \
        #    -F 'object=user' \
        #    -F 'aspect=media' \
        #    -F 'verify_token=myVerifyToken' \
        #    -F 'callback_url=http://YOUR-CALLBACK/URL' \
        #    https://api.instagram.com/v1/subscriptions/

        form_fields = {
          "client_id": instaghent.CONFIG["client_id"],
          "client_secret": instaghent.CONFIG["client_secret"],
          "object": "tag",
          "aspect": "media",
          "object_id": "gf13",
          "callback_url": "http://www.instaghent.com/realgo"
        }
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url="https://api.instagram.com/v1/subscriptions/",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.response.out.write("result:"+result.content)


class RealTimeCallback(webapp2.RequestHandler):
    def get(self):
        def process_tag_update(update):
            update = update

        mode         = self.request.get('hub.mode')
        challenge    = self.request.get('hub.challenge')
        verify_token = self.request.get('hub.verify_token')
        if challenge:
            template_values = {'challenge':challenge}
            #path = os.path.join(os.path.dirname(__file__), '../templates/instagram.html')
            #html = template.render(path, template_values)
            self.response.out.write(challenge)
        else:
            x_hub_signature = self.request.headers.get('X-Hub-Signature')
            if hasattr(self.request, "data"):
                raw_response    = self.request.data
                memcache.add("real", memcache.get("real") + raw_response) 
                get_real = memcache.get("real")
                logging.info(get_real)
                self.response.out.write(get_real)
            memcache.add("real", memcache.get("real") + "err") 
    def post(self):
        logging.info(self.request)
        x_hub_signature = self.request.headers.get('X-Hub-Signature')
        self.response.out.write(instaghent.collectOne())


app = webapp2.WSGIApplication([
    (r'/by/(.*)/(.*)', ShotPage),
    (r'/by/(.*)', AuthorPage),
    (r'/by-json/(.*)/(.*)', ShotJSON),
    (r'/by-json/(.*)', AuthorJSON), 
    (r'/map', MapPage),
    (r'/about', AboutPage),
    (r"/upghent/(.*)", Upghent),
    (r"/downghent/(.*)", Downghent),
    (r'/', MainPage),
    (r'/more/(.*)/(.*)', MorePages),
    (r'/gf13', FiestePage),
    (r'/real', RealTime),
    (r'/realgo', RealTimeCallback),
    (r'/gf13/(.*)', MoreFieste),
    (r'/filter/(.*)', MainFilterPage),
    (r'.*', RedirectToMain),
    ], debug=False)
