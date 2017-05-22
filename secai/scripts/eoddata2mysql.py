import sys
sys.path.insert(0,'../..')
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission

with open('../data/all_symbols.csv', 'r') as otc_file:
	otc_symbols = otc_file.read()
print(str(len(otc_symbols.split('\n'))) + ' Lines')

for x in otc_symbols.split('\n'):
	xf = x.split(';')
	nc = Company()
	nc.name = xf[1]
	nc.symbol = xf[0]
	nc.cik = ''
	nc.sic = ''
	db.add(nc)

db.flush()


