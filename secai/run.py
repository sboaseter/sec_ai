#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), "../secai"))
#print(sys.path)
from secai.models.dbmodels import TestSEC
from colorama import init, Fore
init()
x = TestSEC()

print('{}{}{}'.format(Fore.GREEN, 'SEC A.I', Fore.RESET))


