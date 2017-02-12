import requests
import json
from pprint import pprint
import collections
import threading
import time

url ="https://newsapi.org/v1/articles?source=bloomberg&sortBy=top&apiKey=e05f8cb500624c4eb877cd9d79a78a6d"


def get_data():

	r = requests.get(url)
	# we have r in response form
	# To convert that into dictionary form, we use following command
	#r = r.json() # we get a dictionary of articles 
	#print type(r)

	return r.json()

# but the problem is here we get the dictionary of unicode strings


def convert(data):
    if isinstance(data, basestring):
            return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
            return type(data)(map(convert,data))
    else:
    		return data


#print len(z['articles'])

def news():
	r = get_data()
	#z = convert(r)
	description = []
	title = []
	desc_url =[]
	image_url =[]
	for i in range(len(r['articles'])):
		description.append(r['articles'][i]['description'])
		title.append(r['articles'][i]['title'])
		desc_url.append(r['articles'][i]['url'])
		image_url.append(r['articles'][i]['urlToImage'])

	return description, title, desc_url, image_url

if __name__ == '__main__':
	news()
	


