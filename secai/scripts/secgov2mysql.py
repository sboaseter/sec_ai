import sys
sys.path.insert(0,'../..')
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission

with open('../data/form.idx', 'r') as eightk_file:
	all_reports = eightk_file.read()
print(str(len(all_reports.split('\n'))) + ' Lines')
all_reports_lines = all_reports.split('\n')

eightk = [x for x in all_reports_lines if x.startswith('8-K ')]

test_locate = Company.query.filter(Company.name.ilike('TestX'.lower())).first()
print(test_locate.name)
matches, misses = 0, 0
u_comps = []

for x in range(len(eightk)):
#for x in range(5):
	c_name = eightk[x][12:74]
	if type(c_name) != str:
		continue
	locate = Company.query.filter(Company.name.ilike(c_name.strip().lower())).first()
	if locate:
		print(c_name)
		matches = matches + 1
	else:
		u_comps.append(c_name)
		misses = misses + 1

print(str(matches) + ' Matches')
print(str(misses) + ' Misses')

#	t1 = eightk[x].split('\t')
#	t1comp = eightk[x][12:74]
#	print(t1)
#	print(t1comp)
#	print(x)
#	xf = x.split(';')
#	nc = Company()
#	nc.name = xf[1]
#	nc.symbol = xf[0]
#	nc.cik = ''
#	nc.sic = ''
#	db.add(nc)

#db.flush()


