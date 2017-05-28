import requests
from bs4 import BeautifulSoup as bs
import codecs
from secai.scripts.mlstripper import MLStripper
secgov_8k = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=8-K&owner=include&count=100&action=getcurrent'
secgov_f_base = 'https://www.sec.gov'


def getNewListings():
    res = requests.get(secgov_8k)
    try:
        soup = bs(str(res.content).encode('utf-8'), 'html.parser')
        all_links = soup.findAll(lambda tag: tag.name == 'a' and tag.text == '[html]')
        return [x['href'] for x in all_links]

    except Exception as e:
        print(str(e))

def locate8kReport(url_main):
    res = requests.get('https://www.sec.gov' + url_main)
    try:
        soup = bs(str(res.content).encode('utf-8'), 'html.parser')
        all_links = soup.findAll(lambda tag: tag.name == 'td' and tag.text == '8-K')
        for l in all_links:
            pvtd = l.previous_sibling.previous_sibling.findAll(lambda tag: tag.name == 'a')
            return pvtd[0]['href']
#            print(l)
    except Exception as e:
        print(str(e))

def process8k(url_8k):
    print('Processing: ')
    print(url_8k)
    if url_8k == None:
        return
    res = requests.get('https://www.sec.gov' + url_8k)
#    soup = bs(str(res.content).encode('utf-8'), 'html.parser')
#    mls = MLStripper()
#    print(type(res.content))
#    print(str(res.content)[-20:])
#    content = str(res.content)
#    h_text = mls.strip_tags(content)
    soup = bs(res.content, 'html.parser')
    return soup


#    print(soup.text.encode('utf-8'))

newest = getNewListings()
print(newest)
for listing in newest:
    print('Listing: ')
    print(listing)
    url_8k_htm = locate8kReport(listing)
    print(url_8k_htm)
    res = process8k(url_8k_htm)
    if res == None: continue

    counter = 0
    for i in res.stripped_strings:
        ni = replace_trash(i)
        print(str(counter) + ': ' + repr(ni.encode('utf-8')))
        counter = counter + 1

