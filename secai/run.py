import sys
sys.path.insert(0,'.')
from secai.scripts.secgov import SECMonitor
from secai.models.shared import db, init_db
from colorama import init, Fore, Style
import time
init()
init_db()
from secai.models.dbmodels import SECUIStatus
from datetime import datetime, timedelta

print('{}{}{}{}{}'.format(Style.BRIGHT,Fore.GREEN, 'SEC A.I', Fore.RESET,Style.RESET_ALL))

filing_type = '8-k'
filing_num = 10
filing_base = 'https://www.sec.gov'

xt = SECMonitor(filing_base+'/cgi-bin/browse-edgar?company=&CIK=&type='+filing_type+'&owner=include&count='+str(filing_num)+'&action=getcurrent', False)
while True:
    #add threads after the scrape, inside SECMonitor
    xres = xt.getNewListings()

    secs = SECUIStatus.query.filter(SECUIStatus.text == 'last_check').first()
    secs.entered_on = datetime.now() + timedelta(hours=3)
    db.flush()

    time.sleep(5)




