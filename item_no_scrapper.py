import pandas as pd
from lxml import html, cssselect
import requests
import grequests
from lxml.cssselect import CSSSelector
import numpy as np
import cPickle as pickle
def get_table(content):
	return content.cssselect('div#ResultSetItems')[0]

def get_itm_tables(content):
	return [s for s in content.cssselect('table.li.rsittlref')]
def get_items(content):
	return [s.text_content().strip() for s in content.cssselect('div.dynS')]
def get_itm_table_cont(content):
	return [s.text_content().strip() for s in content.cssselect('table.li.rsittlref')]
def get_itm_name(content):
	return content.cssselect('div.ittl')[0].text_content().strip()
def get_milage_year(content):
	return [s.text_content().strip() for s in content.cssselect('span.v')]

def get_models():
	brandArr = []
	strtest  = '{ name : "AC"},{ name : "AM General"},{ name : "Abarth"},{ name : "Acura"},{ name : "Alfa Romeo", alt : "Alfa%20Romeo"},{ name : "Allard"},{ name : "Allstate"},{ name : "Alpine"},{ name : "Alvis"},{ name : "American Austin"},{ name : "American Bantam"},{ name : "American Motors"},{ name : "Amphicar"},{ name : "Apollo"},{ name : "Apperson"},{ name : "Armstrong-Siddeley"},{ name : "Arnolt-Bristol"},{ name : "Arnolt-MG"},{ name : "Aston Martin", alt : "Aston%20Martin"},{ name : "Asuna"},{ name : "Auburn"},{ name : "Audi"},{ name : "Austin"},{ name : "Austin Healey", alt : "Austin%20Healey"},{ name : "Avanti"},{ name : "BMW"},{ name : "Bentley"},{ name : "Berkeley"},{ name : "Bertone"},{ name : "Biddle"},{ name : "Bizzarrini"},{ name : "Blackhawk"},{ name : "Bond"},{ name : "Borgward"},{ name : "Bricklin"},{ name : "Bristol"},{ name : "Bugatti"},{ name : "Buick"},{ name : "Cadillac"},{ name : "Case"},{ name : "Chandler"},{ name : "Checker"},{ name : "Chevrolet"},{ name : "Chrysler"},{ name : "Cisitalia"},{ name : "Citroen"},{ name : "Cleveland"},{ name : "Coda"},{ name : "Cole"},{ name : "Continental"},{ name : "Cord"},{ name : "Crosley"},{ name : "Cunningham"},{ name : "DAF"},{ name : "DKW"},{ name : "Daewoo"},{ name : "Daihatsu"},{ name : "Daimler"},{ name : "Darrin"},{ name : "Davis"},{ name : "De Vaux"},{ name : "DeLorean"},{ name : "DeSoto"},{ name : "DeTomaso"},{ name : "Delage"},{ name : "Delahaye"},{ name : "Dellow"},{ name : "Denzel"},{ name : "Deutsch-Bonnet"},{ name : "Diana"},{ name : "Dodge"},{ name : "Doretti"},{ name : "Du Pont"},{ name : "Dual-Ghia"},{ name : "Duesenberg"},{ name : "Durant"},{ name : "Duryea"},{ name : "Eagle"},{ name : "Edsel"},{ name : "Elcar"},{ name : "Elva"},{ name : "Erskine"},{ name : "Essex"},{ name : "Excalibur"},{ name : "FWD"},{ name : "Facel Vega"},{ name : "Fairthorpe"},{ name : "Falcon Knight"},{ name : "Fargo"},{ name : "Ferrari"},{ name : "Fiat"},{ name : "Flint"},{ name : "Ford"},{ name : "Franklin"},{ name : "Frazer"},{ name : "Frazer Nash"},{ name : "Freightliner"},{ name : "GMC"},{ name : "Gardner"},{ name : "Geo"},{ name : "Glas"},{ name : "Goggomobil"},{ name : "Goliath"},{ name : "Gordon-Keeble"},{ name : "Graham"},{ name : "Graham-Paige"},{ name : "Griffith"},{ name : "HCS"},{ name : "HRG"},{ name : "Hansa"},{ name : "Haynes"},{ name : "Healey"},{ name : "Henry J"},{ name : "Hertz"},{ name : "Hillman"},{ name : "Hino"},{ name : "Hispano-Suiza"},{ name : "Honda"},{ name : "Hotchkiss"},{ name : "Hudson"},{ name : "Humber"},{ name : "Hummer"},{ name : "Hupmobile"},{ name : "Hyundai"},{ name : "Infiniti"},{ name : "International"},{ name : "Iso"},{ name : "Isotta Fraschini"},{ name : "Isuzu"},{ name : "Iveco"},{ name : "Jaguar"},{ name : "Jeep"},{ name : "Jeffery"},{ name : "Jensen"},{ name : "Jewett"},{ name : "Jordan"},{ name : "Jowett"},{ name : "Kaiser"},{ name : "Kenworth"},{ name : "Kia"},{ name : "Kissel"},{ name : "Kurtis"},{ name : "LaSalle"},{ name : "Lada"},{ name : "Laforza"},{ name : "Lagonda"},{ name : "Lamborghini"},{ name : "Lanchester"},{ name : "Lancia"},{ name : "Land Rover", alt : "Land%20Rover"},{ name : "Lea-Francis"},{ name : "Lexington"},{ name : "Lexus"},{ name : "Lincoln"},{ name : "Lloyd"},{ name : "Locomobile"},{ name : "Lotus"},{ name : "MG"},{ name : "Mack"},{ name : "Maico"},{ name : "Marathon"},{ name : "Marauder"},{ name : "Marcos"},{ name : "Marmon"},{ name : "Marquette"},{ name : "Maserati"},{ name : "Matra"},{ name : "Maxwell"},{ name : "Maybach"},{ name : "Mazda"},{ name : "McLaren"},{ name : "Mercedes-Benz", alt : "Mercedes%2DBenz"},{ name : "Mercury"},{ name : "Merkur"},{ name : "Messerschmitt"},{ name : "Metropolitan"},{ name : "Mini"},{ name : "Mitsubishi"},{ name : "Mitsubishi Fuso"},{ name : "Monteverdi"},{ name : "Moon"},{ name : "Moretti"},{ name : "Morgan"},{ name : "Morris"},{ name : "Moskvich"},{ name : "NSU"},{ name : "Nardi"},{ name : "Nash"},{ name : "Nissan"},{ name : "Oakland"},{ name : "Oldsmobile"},{ name : "Omega"},{ name : "Opel"},{ name : "Osca"},{ name : "Packard"},{ name : "Paige"},{ name : "Panhard"},{ name : "Panoz"},{ name : "Panther"},{ name : "Peerless"},{ name : "Pegaso"},{ name : "Peterbilt"},{ name : "Peugeot"},{ name : "Pierce-Arrow"},{ name : "Plymouth"},{ name : "Pontiac"},{ name : "Porsche"},{ name : "Qvale"},{ name : "Ram"},{ name : "Rambler"},{ name : "Reliant"},{ name : "Renault"},{ name : "Reo"},{ name : "Rickenbacker"},{ name : "Riley"},{ name : "Roamer"},{ name : "Rockne"},{ name : "Rollin"},{ name : "Rolls Royce"},{ name : "Roosevelt"},{ name : "Rover"},{ name : "SRT"},{ name : "Saab"},{ name : "Sabra"},{ name : "Saleen"},{ name : "Salmson"},{ name : "Saturn"},{ name : "Scion"},{ name : "Scripps Booth"},{ name : "Shelby"},{ name : "Sheridan"},{ name : "Siata"},{ name : "Simca"},{ name : "Singer"},{ name : "Skoda"},{ name : "Smart"},{ name : "Standard"},{ name : "Stanguellini"},{ name : "Star"},{ name : "Stearns Knight"},{ name : "Sterling"},{ name : "Stevens-Duryea"},{ name : "Studebaker"},{ name : "Stutz"},{ name : "Subaru"},{ name : "Sunbeam"},{ name : "Suzuki"},{ name : "Swallow"},{ name : "TVR"},{ name : "Talbot-Lago"},{ name : "Tatra"},{ name : "Tesla"},{ name : "Toyopet"},{ name : "Toyota"},{ name : "Triumph"},{ name : "Tucker"},{ name : "Turner"},{ name : "UD"},{ name : "VPG"},{ name : "Vauxhall"},{ name : "Velie"},{ name : "Vespa"},{ name : "Viking"},{ name : "Volkswagen"},{ name : "Volvo"},{ name : "Wartburg"},{ name : "Westcott"},{ name : "Whippet"},{ name : "Willys"},{ name : "Windsor"},{ name : "Wolseley"},{ name : "Workhorse"},{ name : "Yellow Cab"},{ name : "Yugo"},{ name : "Zundapp"}'
	for s  in strtest.replace("{","").replace("}","").split(','):
		n = s.split(':')[1].replace("\"","")
		brandArr.append(n)
	return brandArr

def get_total_result(link):
	link = link.replace("PAGE_NO", '1')
	try:
		page = requests.get(link)
		tree = html.fromstring(page.text)
		center = tree[1][2]
		return int(center.cssselect('span.rcnt')[0].text_content().replace(",",""))/50 + 1
	except Exception, e:
		print 'Failed to estimate exact total page numbers', e
		# or try to scrape 5 pages
		return 5


def get_info_apage(page, make, info_arr):
	info = []
	tree = html.fromstring(page.text)
	center = tree[1][2][1][2]
	table = get_table(center)

	# print len(get_items(table))
	item_nos = get_itm_tables(table)
	total_elems = len(item_nos)
	print total_elems, make
	for k in range(total_elems):
		d = item_nos[k]
		# item # - name - milage - year - make
		milage_yr = get_milage_year(d)
		prod_id = int(d.get('listingid'))
		prod_name = get_itm_name(d)

		try:
			prod_milage = int(milage_yr[1].replace(",",""))
		except Exception, e:
			# print "no valid milage info"
			prod_milage = -1
		
		try:
			prod_yr = int(milage_yr[0])
		except Exception, e:
			# print "no valid year info"
			prod_yr = 0
		info.append([prod_id, prod_name, prod_milage, prod_yr, make])

		info_arr.extend(info)

		# make = make
		# print d.get('listingid'), get_itm_name(d), milage_yr[1], milage_yr[0]
	if total_elems == 0:
		return False
	else:
		return True

if __name__ == '__main__':
	# link = 'http://www.ebay.com/sch/Cars-Trucks-/6001/i.html?LH_Auction=1&LH_Complete=1&LH_Sold=1&_pgn=1&_skc=200&rt=nc'
	# link = 'http://www.ebay.com/sch/Cars-Trucks-/6001/i.html?LH_Auction=1&LH_Complete=1&LH_Sold=1&_pppn=r1&scp=ce0&_rdc=1'
	# link = 'http://www.ebay.com/sch/Cars-Trucks-/6001/i.html?LH_Auction=1&LH_Complete=1&LH_Sold=1&_pgn=2&_skc=200&rt=nc'
	# get_info_apage(link)
	
	prod_info_arr = []
	models = get_models()

	print 'number of models', len(models)
	for model in models:
		link_struct = 'http://www.ebay.com/sch/Cars-Trucks-/6001/i.html?LH_Auction=1&LH_Complete=1&LH_Sold=1&makeval=BRAND_NAME&_nkw=BRAND_NAME&_pgn=PAGE_NO&rt=nc'
		link_struct = link_struct.replace("BRAND_NAME", model)
		NUM_PAGES = min(199, get_total_result(link_struct))
		print NUM_PAGES
		url_arr = []
		for i in range(1,NUM_PAGES):
			link = link_struct.replace("PAGE_NO", str(i))
			url_arr.append(link)

		# async http fetching for faster response
		async_processes = [grequests.get(u) for u in url_arr]
		responses = grequests.map(async_processes, size = 32)

		for page in responses:
			try:				
				flag = get_info_apage(page, model, prod_info_arr)
				if flag == False:
					break
			except Exception, e:
				print e
	info_arr = np.array(prod_info_arr)
	# df = pd.DataFrame({'prod_id':[0], 'prod_title':['example car'], 'prod_milage':[-1], 'prod_yr':[0] })
	df = pd.DataFrame({'prod_id':info_arr[:,0], 'prod_title':info_arr[:,1], 'prod_milage':info_arr[:,2], 'prod_yr':info_arr[:,3], 'model': info_arr[:,4]})
	df.to_pickle('data.pkl')
	


