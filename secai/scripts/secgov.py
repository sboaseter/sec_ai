#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from secai.scripts.cncslookup import getSymbolByName
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission, Phrase
from secai.scripts.iflychat import IFlyPoster 
import re
from datetime import datetime
import codecs


class SECMonitor:
    def __init__(self, sec_url):
        self.sec_url = sec_url

    def processContent(self, filing_url):
        res = requests.get('https://www.sec.gov' + filing_url)
        try:
            filing_content = bs(res.content, 'html.parser')
        except:
            return []
        hardcoded_dict = [x.text for x in Phrase.query.all()]
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
                pass
            c_id = c.id

        ns = Submission()
        ns.companyId = c_id
        ns.accessionNo = new_subm[0]
        ns.rtype = '8-K'
        ns.acceptedOn = datetime.now()
    #    ns.content = res.content
        ns.content = str(self.processContent(new_subm[3]))
#        print('Processing: ' + new_subm[1] + ': ' + new_subm[2])
#        print(self.processContent(new_subm[3]))
#        ns.content = ''
        ### Spawn process
        ns.contentUrl = new_subm[3]
        ns.matches = 0
        ns.sentiment = 'None'
        try:
            db.add(ns)
        except:
            print('Allready entered')

        return ns.content

    def notifyIFlyName(self, company):
        ifcp = IFlyPoster()
        ifcp.postMessage(company)
        print(company)

    def notifyIFlySymbol(self, company, company_symbol):
        ifcp = IFlyPoster()
        print(company + ': ' + company_symbol)

    def notifyIFlyMatches(self, company, company_symbol, dictmatches):
        ifcp = IFlyPoster()
        ifcp.postMessage(company + ': ' + company_symbol + ': ' + dictmatches)
#        print(company + ': ' + company_symbol + ': ' + dictmatches)

    def scrape(self):
        ret = []
        res = requests.get(self.sec_url)
        if res.status_code != 200:  # great!
            return ['Error code: ' + str(res.status_code)]
        try:
            soup = bs(res.content, 'html.parser')
        except:
            return 'Error...'
            
        #all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[html]')
        #[text]-link is too big, need to use the above [html] to do 1 more crawl for access to the pure 8-k report!
        all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[text]')
        for f in all_links:
            fp1 = f.parent
            prev_row = fp1.parent.previous_sibling.previous_sibling.text.strip()
            #accessionNo, unique
            company = re.sub('\((.*?)\)', '', prev_row).strip()

   #         self.notifyIFlyName(company)
            company_symbol = getSymbolByName(company)
#            self.notifyIFlySymbol(company,company_symbol)

            linkref = f['href']
            #accessno = re.sub('\(/.*?-index.htm\)', linkref).strip()
            accessno = re.search(r'^.*\/([^.]*)-.*$', linkref).group(1)
            existingsub = Submission.query.filter(Submission.accessionNo.ilike(accessno.strip())).first()
            if existingsub:
                continue
            subm = self.addSubmission(
                (accessno, company_symbol, company, f['href']))
            print('newsubmission:' + str(subm))
#            self.notifyIFlyMatches(company, company_symbol, str(subm))
            ret.append(subm)
            #pr = '\n\t'.join((company, f['href']))
        if len(ret) > 0:
            return ret
#		if len(all_links) > 0:
#			return all_links
        else:
            return ['No links found']

