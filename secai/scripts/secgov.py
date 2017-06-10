#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from secai.scripts.cncslookup import getSymbolByName
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission, Phrase
from secai.scripts.utils import replace_trash
from secai.scripts.iflychat import IFlyPoster 
import re
from datetime import datetime, timedelta
import codecs
from colorama import init, Fore, Style
init()
from textblob import TextBlob

class SECMonitor:
    def __init__(self, sec_url):
        self.sec_url = sec_url
        self.debug_on = False
        self.acno_proc = []

    # Main listing refresh
    def getNewListings(self):
        try:        
            res = requests.get(self.sec_url)
        except Exception as ssl_error:
            print('SSLError!')
            print(str(ssl_error))
            getNewListings()

        try:
            soup = bs(str(res.content).encode('utf-8'), 'html.parser')
            all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[html]')
#            print('Found {} Filings'.format(len(all_links)))
            for f in all_links: # Link | Processed
                linkref = f['href']
                accessno = re.search(r'^.*\/([^.]*)-.*$', linkref).group(1).strip()
                if accessno in self.acno_proc:
                    continue
                self.acno_proc.append(accessno)

                existingsub = Submission.query.filter(Submission.accessionNo.ilike(accessno)).first()
                if existingsub:
                    print('Exists: ' + existingsub.accessionNo)
                    continue

                # Collect data from listing page and lookup symbol

                fp1 = f.parent
                prev_row = fp1.parent.previous_sibling.previous_sibling.text.strip()
                company = re.sub('\((.*?)\)', '', prev_row)
                company = re.sub(r'^(?:\\n)+','', company)
                if company.endswith(r'\n'): company = company[:-2]

                company = company.lstrip().rstrip()
#                print('ncount: ' + str(company.count('\n')) + ': ' + company)
                company_symbol = getSymbolByName(company)
                # TODO
                if company_symbol == 'Not found':
                    continue
                filing8k_txt_url = self.locate8kReport(f['href'])
                print('[{}]: {}{}{}\t\t{}'.format(accessno, Fore.GREEN,company_symbol, Fore.RESET,company))
                if filing8k_txt_url == None:
                    continue
                subm = self.addSubmission((accessno, company_symbol, company, filing8k_txt_url))


                if subm.content == '[]':
                    continue

                print(subm.content)
                self.notifyIFlyMatches(company, company_symbol, subm.content, subm.contentUrl, subm.sentiment,
                subm.acceptedOn)
#            return [x['href'] for x in all_links] # List of hrefs to the Filing detail page

        except Exception as e:
            
            print('getNewListings: ' + str(e))

    # Locate the 8-k text document on the filing detail page
    def locate8kReport(self, url_detail):
        res = requests.get('https://www.sec.gov' + url_detail)
        try:
            soup = bs(str(res.content).encode('utf-8'), 'html.parser')
            # 8-K text file in a table, td-cell to the left of description column '8-K'
            all_links = soup.findAll(lambda tag: tag.name == 'td' and tag.text == '8-K')
            for l in all_links: # Should only be one
                pvtd = l.previous_sibling.previous_sibling.findAll(lambda tag: tag.name == 'a')
                return pvtd[0]['href']
        except Exception as e:
            pass
            if self.debug_on: 
                print('locate8kReport: ' + str(e))

    #Process 8-K report text
    def processContent(self, filing_url):
#        print('Processing: ' + filing_url)
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
        return (matches, str(res.content))


    def addSubmission(self, new_subm):
#        print('Adding: ')
#        print(new_subm)
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
        ns.acceptedOn = datetime.now() + timedelta(hours=3)

        procRes = self.processContent(new_subm[3])
        ns.content = str(procRes[0])
        ns.contentUrl = new_subm[3]
        ns.matches = 0
        try:
            sentx = TextBlob(procRes[1])
            ns.sentiment = str(sentx.sentiment)
#            print(ns.sentiment)
        except Exception as e:
#            print('Sent: ' + str(e))
            ns.sentiment = 'None'
        try:
            db.add(ns)
        except:
            print('Allready entered')

#        return ns.content
        return ns

    def notifyIFlyName(self, company):
        ifcp = IFlyPoster()
        ifcp.postMessage(company)
        print(company)

    def notifyIFlySymbol(self, company, company_symbol):
        ifcp = IFlyPoster()
        print(company + ': ' + company_symbol)

    def notifyIFlyMatches(self, company, company_symbol, dictmatches, contentUrl, sentiment, acceptedOn):
        ifcp = IFlyPoster()
        ifc_msg = 'Symbol: {} Keywords Triggered: {} Time Stamp: {}. 8k Link: https://www.sec.gov{}'.format(company_symbol, dictmatches, acceptedOn.time().strftime("%H:%M %p"), contentUrl)
        ifcp.postMessage(ifc_msg)
#        ifcp.postMessage('({})[{}] {} :: {} :: {} :: https://www.sec.gov{}'.format(acceptedOn, company_symbol, company, dictmatches, sentiment,
#        contentUrl))
#        print(company + ': ' + company_symbol + ': ' + dictmatches)

