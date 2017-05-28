import sys
sys.path.insert(0,'.')
from secai.scripts.secgov import SECMonitor
from secai.models.shared import init_db
from colorama import init, Fore, Style
import time
init()
init_db()

print('{}{}{}{}{}'.format(Style.BRIGHT,Fore.GREEN, 'SEC A.I', Fore.RESET,Style.RESET_ALL))

filing_type = '8-k'
filing_num = 10

xt = SECMonitor('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type='+filing_type+'&owner=include&count='+str(filing_num)+'&action=getcurrent')
while True:
    #add threads after the scrape, inside SECMonitor
    xres = xt.getNewListings()
    time.sleep(60)




