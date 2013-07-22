item = {
	"name": "a",
	"tags": ["ghent", "gent", "belgium"]
}

item2 = {
	"name": "b",
	"tags": ["gent", "belgium", "city", "street"]
}

item3 = {
	"name": "c",
	"tags": ["gent", "fashion", "scholar", "style", "ladies"]
}

photos = [item, item2, item3]


# Ghent - Reliable, only City
	# Gent 
		# City, no extra except 'belgium' sometimes
			# belgium
			# graslei
			# city, street, 
		# Gentleman
			# sexy, ladies, mr, dangerous, cute, hot
			# fashion, highclass, blazer, menswear, dress, class
			# dapper, style, 
			# gents, people, dude, man, kid
	#   Instaghent > Ghent > Gent (+belgium) (-fashion)

forbidden = ["menswear", "fashion", "gents", "gentleman"]
bad = ["cute", "ladies", "sexy", "mr", "hot", "dapper", "style",
"dude", "man", "kid", "people", "dangerous", "highclass","suit", "blazer",
"menswear"]
locations = ["graslei", "korenmarkt", "veldstraat", "gravensteen"]
allowed = ["belgium", "ghent", "city", "streets"]
allowed.extend(locations)

def filterItems(items): 
	for photo in items:
		score = 0
		for tag in photo["tags"]:
			if tag in allowed:
				score += 1
			if tag in bad:
				score -= 1
			if tag in forbidden:
				score -= 10
		if score < 0:
			items.remove(photo)
	return items

photos = filterItems(photos)
print(photos)