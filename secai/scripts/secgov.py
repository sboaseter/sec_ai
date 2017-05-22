#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
class TestSEC:
	def __init__(self, sec_url):
		self.sec_url = sec_url
 
	def scrape(self):
		res = requests.get(self.sec_url)
		if res.status_code != 200: #great!
			return ['Error code: ' + str(res.status_code)]
		soup = bs(res.content, 'html.parser')
		all_links = soup.findAll(lambda tag: tag.name=='a' and tag.text == '[html]')
		if len(all_links) > 0:
			return all_links
		else:
			return ['No links found']

