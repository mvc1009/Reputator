#!/usr/bin/python3
import os,sys
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
import ipcalc

#
# Usage: python3 reputator.py ips.txt out.json
#
# Output json:
#
# [
#	 {
#		 "ip" : "10.10.10.10",
#		 "resume" : "Listed 0 times with 2 timeouts",
#		 "results" : [['OK', '0SPAM', '0'], ['OK', '0SPAM RBL', '0'], ['OK', 'Abuse.ro', '111'], ['OK', 'Abusix Mail Intelligence Blacklist', '0'], ['OK', 'Abusix Mail Intelligence Domain Blacklist', '0'], ['OK', 'Abusix Mail Intelligence Exploit list', '0'], ['OK', 'Anonmails DNSBL', '0'], ['OK', 'BACKSCATTERER', '0'], ['OK', 'BARRACUDA', '0'], ['OK', 'BLOCKLIST.DE', '0'], ['OK', 'CALIVENT', '0'], ['OK', 'CYMRU BOGONS', '0'], ['OK', 'DAN TOR', '0'], ['OK', 'DAN TOREXIT', '0'], ['OK', 'DNS SERVICIOS', '94'], ['OK', 'DRMX', '0'], ['OK', 'DRONE BL', '0'], ['OK', 'FABELSOURCES', '0'], ['OK', 'HIL', '0'], ['OK', 'HIL2', '0'], ['OK', 'Hostkarma Black', '10'], ['OK', 'IBM DNS Blacklist', '10'], ['OK', 'ICMFORBIDDEN', '10'], ['OK', 'IMP SPAM', '10'], ['OK', 'IMP WORM', '10'], ['OK', 'INTERSERVER', '10'], ['OK', 'ivmSIP', '10'], ['OK', 'ivmSIP24', '10'], ['OK', 'JIPPG', '10'], ['OK', 'KEMPTBL', '10'], ['OK', 'KISA', '183'], ['OK', 'Konstant', '0'], ['OK', 'LASHBACK', '0'], ['OK', 'LNSGBLOCK', '0'], ['OK', 'LNSGBULK', '0'], ['OK', 'LNSGMULTI', '0'], ['OK', 'LNSGOR', '0'], ['OK', 'LNSGSRC', '0'], ['OK', 'MAILSPIKE BL', '74'], ['OK', 'MAILSPIKE Z', '74'], ['OK', 'MSRBL Phishing', '0'], ['OK', 'MSRBL Spam', '0'], ['OK', 'NETHERRELAYS', '0'], ['OK', 'NETHERUNSURE', '0'], ['OK', 'NIXSPAM', '0'], ['OK', 'Nordspam BL', '10'], ['OK', 'ORVEDB', '10'], ['OK', 'PSBL', '10'], ['OK', 'RATS Dyna', '10'], ['OK', 'RATS NoPtr', '10'], ['OK', 'RATS Spam', '10'], ['OK', 'RBL JP', '11'], ['OK', 'RSBL', '11'], ['OK', 's5h.net', '11'], ['OK', 'SCHULTE', '11'], ['OK', 'SEM BACKSCATTER', '33'], ['OK', 'SEM BLACK', '33'], ['OK', 'Sender Score Reputation Network', '1'], ['OK', 'SERVICESNET', '0'], ['OK', 'SORBS BLOCK', '0'], ['OK', 'SORBS DUHL', '0'], ['OK', 'SORBS HTTP', '0'], ['OK', 'SORBS MISC', '0'], ['OK', 'SORBS NEW', '0'], ['OK', 'SORBS SMTP', '0'], ['OK', 'SORBS SOCKS', '0'], ['OK', 'SORBS SPAM', '0'], ['OK', 'SORBS WEB', '0'], ['OK', 'SORBS ZOMBIE', '0'], ['OK', 'SPAMCOP', '0'], ['OK', 'Spamhaus ZEN', '0'], ['OK', 'SPFBL DNSBL', '259066', '0'], ['OK', 'Suomispam Reputation', '0'], ['OK', 'SWINOG', '10'], ['OK', 'TRIUMF', '10'], ['OK', 'TRUNCATE', '10'], ['OK', 'UCEPROTECTL1', '10'], ['OK', 'UCEPROTECTL2', '10'], ['OK', 'UCEPROTECTL3', '10'], ['OK', 'Woodys SMTP Blacklist', '10'], ['OK', 'ZapBL', '11'], ['TIMEOUT', 'MADAVI', '0', 'Ignore'], ['TIMEOUT', 'NoSolicitado', '0', 'Ignore']]
# 	 }
# ]
#
def get_reputation(ip):
	try:
		print("[+] Checking %s" % ip)
		driver = webdriver.Firefox() #open a firefox
		driver.get("https://mxtoolbox.com/blacklists.aspx") # search the url
		assert "Blacklist" in driver.title #confirm Blacklist in title
		elem = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ucToolhandler$txtToolInput") #find the textbox to put the IP
		elem.clear()
		elem.send_keys(ip)
		elem.send_keys(Keys.RETURN)
		time.sleep(12)
		assert "known blacklists" in driver.page_source
		html = driver.page_source
		driver.close()
		soup = BeautifulSoup(html, 'html.parser')

		# Resume: Listed 0 times with 2 timeouts 
		data = soup.body.find('div', attrs={'class':'tool-result-body'}).text
		resume = data.split('\n')[1]
		print(resume)

		# Table results
		results = []
		table = soup.body.find('table', attrs={'class':'tool-result-table'})
		table_body = table.find('tbody')
		rows = table_body.find_all('tr')
		for row in rows:
			cols = row.find_all('td')
			cols = [ele.text.strip() for ele in cols]
			results.append([ele for ele in cols if ele])

		return {
			'ip':ip,
			'resume':resume,
			'results':results
			}
	except:
		return None
	return None

output = []
f = open(sys.argv[1], 'r')
ips = f.read().split('\n')
for ip in ips:
	if '/' in ip:
		for lip in ipcalc.Network(ip):
			a = None
			while not a:
				a = get_reputation(ip)
			output.append(a)
	else:
		a = None
		while not a:
			a = get_reputation(ip)
			
	# Adding the results to the output variable
	output.append(a)
	
	# Rewrite the output in every loop iteration in order to avoid losing results due to a failure
	json_object = json.dumps(output, indent=4)
	with open(sys.argv[2], "w") as outfile:
		outfile.write(json_object)
	print('\t[+] Saving results in %s' % sys.argv[2])
	
	# Sleep time to avoid being banned
	time.sleep(120)
