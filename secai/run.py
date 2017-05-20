#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), "../secai"))
#print(sys.path)
from secai.models.dbmodels import TestSEC
from colorama import init, Fore
init()

print('{}{}{}'.format(Fore.GREEN, 'SEC A.I', Fore.RESET))

x = TestSEC('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=8-k&owner=include&count=10&action=getcurrent')
xres = x.scrape()
print(str(len(xres)) + ' links')

for x in xres:
	print(x)




