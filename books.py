from flask import json
import xmltodict

try:
	from urllib.request import urlopen
	from urllib import parse
except ImportError:
	from urllib2 import urlopen, urlparse as parse

# Method to create the proper search parameter for the URL call
def path_replace_space(slug):
	return slug.replace(' ', '+')

# Method to query for Books given either the Book name, author name or ISBN
# 	from the GoodReads API
def queryBooks(searchParam, pageNum=1):
	key = 'TPC3VnClaHo1iI1xGPI5A'
	searchParam = path_replace_space(searchParam)

	query_url = 'https://www.goodreads.com/search/index.xml?key={0}&q=\"{1}\"&page:{2}'.format(key, searchParam, pageNum)
	print(query_url)
	g = urlopen(query_url)
	results = g.read()
	g.close()

	resultsDict = xmltodict.parse(results)['GoodreadsResponse']['search']
	
	return json.dumps(resultsDict)