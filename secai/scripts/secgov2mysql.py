import sys
sys.path.insert(0, '../..')
from secai.models.shared import db
from secai.models.dbmodels import Company, Submission
from datetime import datetime
import requests
    
with open('../data/form.idx', 'r') as eightk_file:
    all_reports = eightk_file.read()
print(str(len(all_reports.split('\n'))) + ' Lines')
all_reports_lines = all_reports.split('\n')

eightk = [x for x in all_reports_lines if x.startswith('8-K ')]

test_locate = Company.query.filter(Company.name.ilike('TestX'.lower())).first()
#print(test_locate.name)
matches, misses = 0, 0
u_comps = []
counter = 0
for x in eightk:    
    if counter % 100 == 0:
        print(str(x))

    counter = counter + 1
    #                               type    name       cik       filed     fileurl
    cf = [f.strip() for f in [x[:12], x[12:74], x[74:86], x[86:98], x[98:]]]

    if type(cf[1]) != str:
        continue
    locate = Company.query.filter(
        Company.name.ilike(cf[1].strip().lower())).first()
    c_id = 1
    if locate:
        print(cf[1])
        matches = matches + 1
        c_id = locate.id
    else:
        u_comps.append(cf[1])
        misses = misses + 1

#    res = requests.get('https://www.sec.gov/Archives/' + cf[4])
#    if res.status_code != 200: #great!
#        print('Failed to get report')
#        continue
    

    ns = Submission()
    ns.companyId = c_id
    ns.accessionNo = '-' + str(counter)
    ns.rtype = cf[0]
    ns.acceptedOn = datetime.now()
#    ns.content = res.content
    ns.contentUrl = cf[4]
    ns.matches = 0
    ns.sentiment = 'None'
    db.add(ns)

    #if counter % 100 == 0:
    db.flush()

db.flush()


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
