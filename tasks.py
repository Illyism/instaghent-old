# -*- coding: utf-8 -*-
import webapp2
import jinja2
import os
from instagram import client, subscriptions
from instaghent import i18n, instaghent
import codecs

import logging

CONFIG = {
	'client_id': 'a5a67115f0fc45d6b97d318ac915aa91',
	'client_secret': '76458a657e8c4317a32ebb9b8b224219',
	'redirect_uri': 'http://localhost:8002/oauth_callback'
}


api = client.InstagramAPI(**CONFIG)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("nothing to see here")


class Collecter(webapp2.RequestHandler):
	def get(self):
		instaghent.collectFiles()
		self.response.out.write("yay")

class CollecterInsta(webapp2.RequestHandler):
	def get(self):
		instaghent.collectFilesInsta()
		self.response.out.write("yay")

class CollecterFieste(webapp2.RequestHandler):
	def get(self):
		instaghent.collectFilesFieste()
		self.response.out.write("gf13 rules")

class InitFieste(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(instaghent.InitFieste())

class Deleter(webapp2.RequestHandler):
	def get(self):
		x = instaghent.deleteFiles()
		self.response.out.write(x)

class CollecterLong(webapp2.RequestHandler):
	def get(self):
		instaghent.collectFilesLong()
		self.response.out.write("hooray")


app = webapp2.WSGIApplication([
	(r'/tasks/', MainPage),
	(r'/tasks/collect', Collecter),
	(r'/tasks/collectInsta', CollecterInsta),
	(r'/tasks/collectFieste', CollecterFieste),
	(r'/tasks/InitFieste', InitFieste),
	(r'/tasks/delete', Deleter),
	(r'/tasks/collect/long', CollecterLong)
	], debug=True)
