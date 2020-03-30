import requests
import re
import shelve
from progress.bar import Bar

db = shelve.open('data','w')

print('Downloading hero list.\n')
code = requests.get('http://www.dotamax.com/hero/rate/').text
regex = r'/\w+_hphover\.png\"></img><span class=\"hero-name-list\">.+?<'
etc = dict()
cte = dict()
for s in re.findall(regex,code):
    eng = s[1:s.find('_hph')]
    chn = s[s.find('t\">') + 3:len(s) - 1]
    etc[eng] = chn
    cte[chn] = eng
db['etc'] = etc
db['cte'] = cte
wrate = dict()
anti = dict()
comb = dict()
print('Downloading win rate data.\n')
bar = Bar('   Downloading', max = len(etc.keys()), fill='#', suffix='%(percent)d%%')
for name in etc.keys():
    code = requests.get('http://www.dotamax.com/hero/detail/match_up_anti/%s/' % (name)).text
    regex = r'率: \d+\.\d+'
    wrate[name] = float(re.findall(regex,code)[0][3:]) / 100
    d = dict()
    regName = r'\w+_hp'
    regRate = r'>\d+\.\d+%</div><div class=\"segment segment-gold'
    names = re.findall(regName,code)
    rates = re.findall(regRate,code)
    for i in range(len(names)):
        d[names[i][:len(names[i]) - 3]] = float(rates[i][1:6]) / 100
    anti[name] = d
    code = requests.get('http://www.dotamax.com/hero/detail/match_up_comb/%s/' % (name)).text
    d = dict()
    regName = r'\w+_hp'
    regRate = r'>\d+\.\d+%</div><div class=\"segment segment-gold'
    names = re.findall(regName,code)
    rates = re.findall(regRate,code)
    for i in range(len(names)):
        d[names[i][:len(names[i]) - 3]] = float(rates[i][1:6]) / 100
    comb[name] = d
    bar.next()
bar.finish()
print('Constructing the database.\n')
db['wrate'] = wrate
db['anti'] = anti
db['comb'] = comb
db.close()