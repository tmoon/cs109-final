from lxml import html, cssselect
import requests, grequests
from lxml.cssselect import CSSSelector
import time
import pandas as pd
import cPickle as pickle
import random
from time_convert import convert_UTC
import numpy as np
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

	return itemText.replace("Item Title: ", ""), winningBid

def headVals(content):
	return [s.text_content().strip() for s in content.cssselect('span.titleValueFont')]
# def contentVals(content):
# 	return [s.text_content().strip() for s in content.cssselect('td.newcontentValueFont')]
# def getMembers(content):
# 	return [s.text_content().strip() for s in content.cssselect('td.onheadNav')]
def get_rows(content):
	rows = content.cssselect('tr')[1:]
	info_arr = []
	for r in rows:
		auto = 1
	
		if r.get('class') == None:
			auto = 0
		if r.get('id') == 'viznobrd':
			auto = -1

		if auto == 1:
			vals = [s.text_content().strip() for s in r.cssselect('td.newcontentValueFont')]
		elif auto == 0:
			vals = [r.cssselect('td.onheadNav')[0].text_content().strip()]
			vals.extend([s.text_content().strip() for s in r.cssselect('td.contentValueFont')])
			if vals[0][:10] == 'Member Id:':
				vals[0] = vals[0][11:]
		else:
			vals = ['Starting Price']
			vals.extend([s.text_content().strip() for s in r.cssselect('td.contentValueFont')])

		assert (len(vals) == 3)
		vals.append(auto)
		info_arr.append(vals)

	return info_arr


def get_bid_table(content):
	return content.cssselect('div#vizrefdiv')[0]

def get_table(pid):
	url = get_url(pid)
	page = get_req_instance(url)
	print page.url
	tree = html.fromstring(page.text)
	t0 = time.time()
	sel = CSSSelector('div.BHbidSecBorderGrey')
	res = sel(tree)

	itm_info = [pid]
	name_price = getNameBid(res[0])
	itm_info.extend(name_price)
	
	bid_data = headVals(res[1])
	itm_info.extend(bid_data)

	# bids =  contentVals(res[1])
	# members = getMembers(res[1])

	# print bids

	# for i in range(len(bids)/3):
	# 	print bids[3*i], bids[3*i + 1], bids[3*i +2 ]
	# print '\n', time.time() - t0
	tab = get_bid_table(res[1])
	return itm_info, get_rows(tab)
if __name__ == '__main__':

	# df = pd.read_pickle('data.pkl')
	# items = df.prod_id[:1000]
	# items.to_pickle('arr.pkl')
	items = pd.read_pickle('arr.pkl')
	df = 1
	pid = 331077709269
	get_table(pid)
	
	basic_info = []
	time_series = {}
	t0 = time.time()
	for k, pid in enumerate(items):

		itm_info, arr = np.array(get_table(pid))

		time_series[pid] = arr
		basic_info.append(itm_info)
		# time.sleep(1)
		t = time.time() - t0
		print 'scrapped %d items, current item id %s, time elapsed %f' % (k, pid, t)
		print '\n ------------------------------- \n'

		if k % 100 == 0:
			pickle.dump( basic_info, open( "./data/basic_"+str(k/100)+".pkl", "wb" ) )
			pickle.dump( time_series, open( "./data/time_series_"+str(k/100)+".pkl", "wb" ) )
			basic_info = []
			time_series = {}
	# end for
	# dump the last batch
	pickle.dump( basic_info, open( "./data/basic_last.pkl", "wb" ) )
	pickle.dump( time_series, open( "./data/time_series_last.pkl", "wb" ) )
	