#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), "../secai"))
#print(sys.path)
from secai.models.dbmodels import TestSEC
from colorama import init, Fore, Style
init()

print('{}{}{}{}{}'.format(Style.BRIGHT,Fore.GREEN, 'SEC A.I', Fore.RESET,Style.RESET_ALL))
filing_type = '8-k'
filing_num = 10

x = TestSEC('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type='+filing_type+'&owner=include&count='+str(filing_num)+'&action=getcurrent')
xres = x.scrape()
print(str(len(xres)) + ' links')

for x in xres:
	print(str(Style.DIM), Fore.YELLOW + str(x) + Fore.RESET + (Style.RESET_ALL))




