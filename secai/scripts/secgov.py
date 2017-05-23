#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from secai.scripts.cncslookup import getSymbolByName
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission
import re
from datetime import datetime
import codecs
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()        

class TestSEC:
    def __init__(self, sec_url):
        self.sec_url = sec_url

    def processContent(self, filing_url):
        res = requests.get('https://www.sec.gov' + filing_url)
        filing_content = bs(res.content, 'html.parser')
        hardcoded_dict = ['delete references to a classified Board structure','statements about anticipated future operating','Spin-Off Agreement','entered into a','change the company’s name','name change','Supply agreement','merger','new symbol','investor presentation','distribution expansion project','third party marketing','brand expansion','entered into an Agreement','entered into a Agreement','accounts payable extinguished','exchange shares of common stock','decreasing the Company’s authorized shares of common stock','Reverse Merger','generated million in revenue','Share exchange agreement','Entry Into a Material Event','PR promotion promote','Securities Purchase Agreement','Awarded (government contract) Contract','Order in favor of the company','Fully exercised the/this convertible note','Convertible notes paid in full','reduce convertible debt','eliminate convertible debt','sold business division','Asset Purchase Agreement','Reduction of debt obligations','reducing outstanding shares','retire shares','Improve company balance sheet','Improve company’s balance sheet','Reduce convertible notes','100 percent converted','100 converted','Application to uplist','Uplist','Uplisted', 'issued a press release announcing']
        matches = []
        for x in hardcoded_dict:
            if x in str(res.content):
                matches.append(x)
        return matches
                

        #print(strip_tags(str(filing_content.encode('utf-8'))))
        #filing_content_sent = TextBlob(str(strip_tags(str(filing_content))))
        #print(filing_content_sent.sentiment)        

    def addSubmission(self, new_subm):
        locate = Company.query.filter(Company.name.ilike(
            new_subm[2].strip().lower())).first()
        c_id = 1
        if locate:  # found in list
            c_id = locate.id
        else:
            c = Company()
            c.name = new_subm[2].strip()
            c.symbol = new_subm[1]
            db.add(c)
            try:
                db.flush()
            except: 
                print('Allready entered')
            c_id = c.id

        ns = Submission()
        ns.companyId = c_id
        ns.accessionNo = new_subm[0]
        ns.rtype = '8-K'
        ns.acceptedOn = datetime.now()
    #    ns.content = res.content
        #ns.content = self.processContent(new_subm[3])
        print('Processing: ' + new_subm[1] + ': ' + new_subm[2])
        print(self.processContent(new_subm[3]))
        ns.content = ''
        ### Spawn process
        ns.contentUrl = new_subm[3]
        ns.matches = 0
        ns.sentiment = 'None'
        try:
            db.add(ns)
        except:
            print('Allready entered')

        return ns

    def scrape(self):
        ret = []
        res = requests.get(self.sec_url)
        if res.status_code != 200:  # great!
            return ['Error code: ' + str(res.status_code)]
        soup = bs(res.content, 'html.parser')
        #all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[html]')
        all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[text]')
        for f in all_links:
            fp1 = f.parent
            prev_row = fp1.parent.previous_sibling.previous_sibling.text.strip()
            #accessionNo, unique
            company = re.sub('\((.*?)\)', '', prev_row).strip()
            company_symbol = getSymbolByName(company)
            linkref = f['href']
            #accessno = re.sub('\(/.*?-index.htm\)', linkref).strip()
            accessno = re.search(r'^.*\/([^.]*)-.*$', linkref).group(1)
            subm = self.addSubmission(
                (accessno, company_symbol, company, f['href']))
            ret.append(subm)
            #pr = '\n\t'.join((company, f['href']))
        if len(ret) > 0:
            return ret
#		if len(all_links) > 0:
#			return all_links
        else:
            return ['No links found']

