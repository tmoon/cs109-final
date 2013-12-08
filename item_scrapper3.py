from lxml import html, cssselect
import requests, grequests
from lxml.cssselect import CSSSelector
import time
import pandas as pd
# import cPickle as pickle
import random
from time_convert import convert_UTC
import numpy as np
random.seed(42)
import os, sys

def get_random_agent():
	USER_AGENT_LIST = [
	    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 \
	         (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
	    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) \
	       Gecko/16.0 Firefox/16.0',
	    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 \
	       (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
	    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
	    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
	    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0)",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 \
	    	(KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre"

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
def get_rows(content, pid):
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
		vals.append(int(pid))
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
	return itm_info, get_rows(tab, pid)
if __name__ == '__main__':

	# df = pd.read_pickle('data.pkl')
	# items = df.prod_id[:1000]
	# items.to_pickle('arr.pkl')
	items = pd.read_pickle('big_arr.pkl')
	print len(items)
	
	basic_info = []
	time_series = []
	t0 = time.time()
	t = 0
	ferrror = open('error_log.txt','w')
	err = 0
	for k, pid in enumerate(items[:25000]):
		k = k
		try:
			itm_info, arr = get_table(pid)
			time_series.extend(arr)
			basic_info.append(itm_info)
		except Exception, e:
			print 'ERROR!', e
			ferrror.write(str(pid)+'\n')
			# restart the network to update ip
			command = 'echo '+str(sys.argv[1])+' | sudo -S service network-manager restart'
			os.system(command)
			err += 1

		# time.sleep(1)
		old_t = t
		t = time.time() - t0
		print t - old_t
		print 'scrapped %d items (failed %d), current item id %s, time elapsed %f' % (k, err, pid, t)
		print '\n ------------------------------- \n'

		if k % 250 == 0 and k > 0:
			basic_info = np.array(basic_info)
			time_series = np.array(time_series)

			df_basic = pd.DataFrame({'prod_id': basic_info[:,0], 'prod_title': basic_info[:,1], 'price': basic_info[:,2], 'bidders': basic_info[:,3], \
				'bids': basic_info[:,4], 'end_time': basic_info[:,5], 'duration': basic_info[:,6]})
			print df_basic.head()
			df_ts = pd.DataFrame({'prod_id': time_series[:,4],'bidder': time_series[:,0],'bid_amount': time_series[:,1],\
				'bid_time': time_series[:,2], 'auto_flag': time_series[:,3]})
			print df_ts.head()
			# reser buffers
			basic_info = []
			time_series = []
			# save everything
			try:
				df_basic.to_csv('./data/basic_'+str(k/250)+'.csv', sep='\t', index=False, header = False)
			except Exception, e:
				print e

			try:
				df_ts.to_csv('./data/ts_'+str(k/250)+'.csv', sep='\t', index=False, header = False)
			except Exception, e:
				print e

	# 	if k % 100 == 99:
	# 		pickle.dump( basic_info, open( "./data/basic_"+str(k/100)+".pkl", "wb" ) )
	# 		pickle.dump( time_series, open( "./data/time_series_"+str(k/100)+".pkl", "wb" ) )
	# 		basic_info = []
	# 		time_series = {}
	# # end for
	# # dump the last batch
	# pickle.dump( basic_info, open( "./data/basic_last.pkl", "wb" ) )
	# pickle.dump( time_series, open( "./data/time_series_last.pkl", "wb" ) )
	