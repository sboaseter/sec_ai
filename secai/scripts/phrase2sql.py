import codecs
from secai.models.shared import db
from secai.models.dbmodels import Phrase
x = codecs.open('secai/data/phrases.txt', 'r', 'utf-8')
xc = x.read()
xcl = xc.split('\r\n')
fail_p = []
for l in xcl:
    if len(l) == 0:
        continue
    try:
        p = Phrase()
        w, t = (l.split('|'))
        p.weight = float(w)
        p.text = t.lower()
        db.add(p)
        db.flush()
    except Exception as e:
        print(str(e))
        print(l.encode('utf-8'))
        fail_p.append(l)

for fp in fail_p:
    print(fp.encode('utf-8'))

