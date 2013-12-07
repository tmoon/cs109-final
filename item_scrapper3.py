from lxml import html, cssselect
import requests, grequests
from lxml.cssselect import CSSSelector
import time
import pandas as pd
import random

random.seed(42)

def get_random_agent():
	USER_AGENT_LIST = [
	    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 \
	         (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
	    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) \
	       Gecko/16.0 Firefox/16.0',
	    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 \
	       (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'
	]
	return random.choice(USER_AGENT_LIST)

def get_url(pid):
	return 'http://offer.ebay.com/ws/eBayISAPI.dll?ViewBids&item='+str(pid)+'&showauto=true'

def get_req_instance(u):
	HTTP_PROXY ={"http":'http://127.0.0.1:8123'}
	return requests.get(u, headers = {'user-agent': get_random_agent}, proxies=HTTP_PROXY)

def getNameBid(content):
	itemText = content.cssselect('a.BHitemDesc')[0].text_content()
	winningBid = content.cssselect('td.BHctBidVal')[0].text_content()

	return itemText, winningBid

def headVals(content):
	return [s.text_content().strip() for s in content.cssselect('span.titleValueFont')]
def contentVals(content):
	return [s.text_content().strip() for s in content.cssselect('td.newcontentValueFont')]
def getMembers(content):
	return [s.text_content().strip() for s in content.cssselect('td.onheadNav')]

def get_table(pid):
	url = get_url(pid)
	page = get_req_instance(url)
	print page.url
	tree = html.fromstring(page.text)
	t0 = time.time()
	sel = CSSSelector('div.BHbidSecBorderGrey')
	res = sel(tree)

	# print getNameBid(res[0])
	# print html.tostring(res[1])
	print headVals(res[1])
	bids =  contentVals(res[1])
	members = getMembers(res[1])

	# print bids

	for i in range(len(bids)/3):
		print bids[3*i], bids[3*i + 1], bids[3*i +2 ]
	print '\n', time.time() - t0
if __name__ == '__main__':

	# df = pd.read_pickle('data.pkl')
	# items = df.prod_id[:1000]
	# items.to_pickle('arr.pkl')
	items = pd.read_pickle('arr.pkl')
	df = 1
	print 'done with huge df!'
	for pid in items:
		print '\n ------------------------------- \n'
		get_table(pid)		
		# time.sleep(1)
		print '\n'
