import sys
sys.path.insert(0, '../..')
#from secai.models.shared import db
#from secai.models.dbmodels import Company, Submission
#from datetime import datetime
import requests
import json

def getSymbolByName(srch):
    xpf = 'https://in.finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={}?bkt=finance-IN-en-IN-def'    
    res = requests.get(xpf.format(srch))
    #print(str(res.status_code))
    #print(res.content)
    my_json = res.content.decode('utf8').replace("'", '"')
    if 'Thank you for your patience.' in my_json:
        return "Request error"

    try:
        data = json.loads(my_json)
    except json.decoder.JSONDecodeError:
       
        print(my_json)
        return 'Not found'

    if len(data['items']) > 0:
        return data['items'][0]['symbol']
    else:
        return "Not found"

#print('Looking up: ' + sys.argv[1])

#companies = 

#xpf = 'https://in.finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={}?bkt=finance-IN-en-IN-def'

#res = requests.get(xpf.format('Dewmar'))

#print(type(res.content))
#print(res.content)


#my_json = res.content.decode('utf8').replace("'", '"')
#print(my_json)
#print('- ' * 20)
#data = json.loads(my_json)
#print('Result: ' + data['items'][0]['symbol'])
#s = json.dumps(data, indent=4, sort_keys=True)
#print(s.items)
