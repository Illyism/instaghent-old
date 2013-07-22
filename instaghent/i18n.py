# -*- coding: utf-8 -*-

def parseAcceptLanguage(acceptLanguage):
  languages = acceptLanguage.split(",")
  locale_q_pairs = []

  for language in languages:
	if language.split(";")[0] == language:
	  # no q => q = 1
	  locale_q_pairs.append((language.strip(), "1"))
	else:
	  locale = language.split(";")[0].strip()
	  q = language.split(";")[1].split("=")[1]
	  locale_q_pairs.append((locale, q))

  return locale_q_pairs


def detectLocale(acceptLanguage):
  defaultLocale = 'en'
  supportedLocales = ['en', 'nl']

  locale_q_pairs = parseAcceptLanguage(acceptLanguage)
  for pair in locale_q_pairs:
	for locale in supportedLocales:
	  # pair[0] is locale, pair[1] is q value
	  if pair[0].replace('-', '_').lower().startswith(locale.lower()):
		return locale

  return defaultLocale

text = {
	"en": {
		"title": u"Instaghent",
		"tagline": u"Everyday Instagram photographs of Ghent, Belgium",
		"description": u"""<p>Instaghent is a collection of all the cool and amazing images taken in Ghent that can be found on Instagram. You can add your own images by adding the hashtag <b>#instaghent.</b></p><p>We want the citizens of Ghent and the travellers from all over the world to be able to see and enjoy the beauty and style of the city. People can take a picture of their favorite spot, tag it and it will show up here.</p><p>You can rate images as <b>Totally Ghent</b> and <b>Not Ghent</b>.</p>""",
		"short": u"""A collection of Instagram images taken in Ghent. Add your own with <strong>#instaghent</strong>""",
		"metashort": u"""A collection of Instagram images taken in Ghent. Add your own with #instaghent. User-voted photographs by Instagram photographers in Ghent, Belgium. See the best shots of Korenmarkt, Graslei, Gravensteen and all the others.""",
		"tweet": u"Collection%20of%20everyday%20Instagram%20shots%20taken%20in%20#Ghent.",
		"disclaimer": u"""This app is not connected to the City of Ghent in any way. The images are automatically added from several hashtags and location data used by Instagram. We are not responsible for what you see here, please rate any disturbing images you see as "Not Ghent".""",
		"sorting": {
			"sort": u"Sort by",
			"comments": u"Most Commented",
			"ghents": u"Most Ghent-like",
			"likes": u"Most likes",
			"location": u"Location",
			"time": u"Newest",
			"author": u"Photographer",
		},
		"motto": u"Let's celebrate the beauty of Ghent.",
		"about": u"About",
		"more": u"more",
		"loadmore": u"Laad meer",
		"instalink": u"View on Instagram",
		"upvote": u"Totally Ghent",
		"downvote": u"Not Ghent",
		"back": u"back to home",
		"lang": u"en",
		"ghentmeter": u"Ghent-meter",
		"filter": u"Filter",
		"likes": u"Likes",
		"comments": u"Comments",
		"time": u"Time",
		"moreby": u"More by",
		"caption": u"Caption",
		"area": u"Area",
		"ghent": u"Ghent",
		"belgium": u"Belgium",
		"details": u"Details",
		"tags": u"Tags"
	},
	"nl": {
		"title": u"Instaghent",
		"tagline": u"Alledaagse Instagram foto's van Gent, België",
		"description": u"""<p>Instaghent is een verzameling van alle coole en geweldige foto's die genomen worden in Gent en die gevonden kunnen worden op Instagram. Je kan je eigen foto's bijvoegen met de hashtag <b>#Instaghent</b></p><p>We willen dat de inwoners van Gent en de reizigers van heel de wereld de schoonheid en stijl van Gent kunnen genieten. Men kan een foto nemen van hun favoriete plek, het taggen en het verschijnt op deze site.</p><p>Je kan foto's beoordelen als <b>Helemaal Gents</b> en <b>Niet Gents</b>.</p>""",
		"short": u"""Een verzameling Instagram foto's genomen in Gent. Voeg je eigen toe met <strong>#instaghent</strong>""",
		"metashort": u"""Een verzameling Instagram foto's genomen in Gent. Voeg je eigen toe met #instaghent. Gebruiker-gewaardeerde foto's door Instagram fotografen in Gent, België. Zie de beste shots van Korenmarkt, Graslei, Gravensteen en andere top toeristenplekjes.""",
		"tweet": u"Verzameling%20van%20alledaagse%20Instagram%20shots%20genomen%20in%20#Gent.",
		"disclaimer": u"""Deze app is niet verbonden met Stad Gent. De beelden worden automatisch toegevoegd van diverse hashtags en locatiegegevens gebruikt door Instagram. Wij zijn niet verantwoordelijk voor wat u hier ziet, beoordeel storende beelden als "Niet Gents".""",
		"sorting": {
			"sort": u"Sorteren op",
			"comments": u"Meest commentaar",
			"ghents": u"Meest Gents",
			"likes": u"Meeste Likes",
			"location": u"Locatie",
			"time": u"Nieuwste",
			"author": u"Fotograaf"
		},
		"motto": u"Vier samen de pracht van Gent.",
		"about": u"Over",
		"more": u"meer",
		"loadmore": u"Laad meer",
		"instalink": u"Bekijken op Instagram",
		"upvote": u"Helemaal Gents",
		"downvote": u"Niet Gents",
		"back": u"terug naar start",
		"lang": u"nl",
		"ghentmeter": u"Gent-meter",
		"filter": u"Filter",
		"likes": u"Likes",
		"comments": u"Reacties",
		"time": u"Tijdstip",
		"moreby": u"Meer van",
		"caption": u"Onderschrift",
		"area": u"Plaats",
		"ghent": u"Gent",
		"belgium": u"België",
		"details": u"Details",
		"tags": u"Tags"
	}
}


def get(ln):
	return text[detectLocale(ln)]