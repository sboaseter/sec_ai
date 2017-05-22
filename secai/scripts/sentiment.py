from textblob import TextBlob

t1 = 'This is a reall good day, it\'s all awesome!'
t2 = 'What a crappy day, when will it improve?'

t1s = TextBlob(t1)
t2s = TextBlob(t2)

print(t1s.sentiment)
print(t2s.sentiment)

with open('all_symbols.csv', 'r') as otc_file:
	otc_symbols = otc_file.read()
print(str(len(otc_symbols.split('\n'))) + ' Lines')
[print(x) for x in otc_symbols.split('\n')[0:5]]
#print(otc_symbols.split('\n')[0:5])

import requests
from bs4 import BeautifulSoup as bs
import codecs
filing_url = 'https://www.sec.gov/Archives/edgar/data/1437517/000101054917000191/act8k051917.htm'
res = requests.get(filing_url)
print(res.status_code)
filing_content = bs(res.content, 'html.parser')

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

print(strip_tags(str(filing_content.encode('utf-8'))))
filing_content_sent = TextBlob(str(strip_tags(str(filing_content))))
print(filing_content_sent.sentiment)


