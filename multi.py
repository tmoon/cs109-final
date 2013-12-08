from multiprocessing import Process, Pool
import time, random
import urllib2
# from requests import async
# import grequests as greq
def millis():
	return int(round(time.time() * 1000))
 
# def http_get(url):
# 	start_time = millis()
# 	result = {"url": url, "data": urllib2.urlopen(url, timeout=5).read()[:100]}
# 	print url + " took " + str(millis() - start_time) + " ms"
# 	return result
urls = ['http://www.google.com/', 'https://foursquare.com/', 'http://www.yahoo.com/', 'http://www.bing.com/', "https://www.yelp.com/"]
 
# pool = Pool(processes=5)
 
# start_time = millis()
# results = pool.map(http_get, urls)
 
# print "\nTotal took " + str(millis() - start_time) + " ms\n"
 
# for result in results:
# 	print result
# If using requests > v0.13.0, use
# from grequests import async

import grequests, requests

urls = [
    'http://www.heroku.com',
    'http://tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://kennethreitz.com'
]


	
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 \
         (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) \
       Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 \
       (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
]




import pandas as pd
import cPickle as pickle
# df = pd.read_pickle('data.pkl')
# print df
# uids = df.prod_id.unique()
# pickle.dump( uids, open( "big_arr.pkl", "wb" ) )
uids = pickle.load(open( "./big_arr.pkl", "rb" ))
print len(uids)
# items = df.prod_id[200:300]
# # url_arr = []
# for pid in items:
# 	url_arr.append('http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item='+str(pid)+'&showauto=true')

# anyc_reqs = []
# for u in url_arr:
# 	page = grequests.get(u, headers = {'user-agent': random.choice(USER_AGENT_LIST)}, proxies=HTTP_PROXY)
# 	anyc_reqs.append(page)

# for r in grequests.map(anyc_reqs, size = 8):
# 	# print r.url
#     print r.text[:10], '\n'


# r = requests.get('http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item=111216505626&showauto=true', headers={'pid':'111216505626'})

# print r.request.headers['pid']