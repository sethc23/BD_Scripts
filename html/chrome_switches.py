import os,json
from subprocess import Popen as sub_popen
from subprocess import PIPE as sub_PIPE

store_file = os.environ['BD'] + '/html/chromedriver_switches.json'
http_src = 'http://peter.sh/experiments/chromium-command-line-switches'

def run_cmd(cmd):
    p = sub_popen(cmd,stdout=sub_PIPE,shell=True,executable='/bin/zsh')
    (_out,_err) = p.communicate()
    assert _err is None
    return _out.rstrip('\n')

def update_store(update='auto'):
    
    day=60*60*24
    update_period_in_seconds=day*30
    if update=='auto' and os.path.exists(store_file):
        last_updated,now = run_cmd("stat -c '%Y' " + store_file + "; date +%s").split('\n')
        last_updated,now = int(last_updated),int(now)
        if (now-last_updated) <= update_period_in_seconds:
            # print('not updating')
            return
    print('Updating ' + store_file)
    
    from bs4 import BeautifulSoup as BS
    import HTML_API as H
    import sys,re

    sys.path.append(os.environ['BD']+'/html')
    run_cmd("wget -q -L -O tmp --local-encoding=$LANG %s;" % http_src)
    with open('tmp','r') as f: x=f.read()
    run_cmd("rm tmp;")
    
    h=BS(x,from_encoding='utf8')
    s=H.remove_non_ascii(h.decode_contents())
    h=BS(s)

    t=h.find_all('table',attrs={'class':'overview-table'})
    assert len(t)==1
    t=t[0]

    conditions=t.find_next_siblings()[-1]
    notes={}
    for r in conditions.find_all('li'):
        notes.update({int(r.attrs['id'].replace('condition-','')):str(H.remove_non_ascii(r.text)).strip()})

    headers=[]
    for c in t.find('thead').find_all('th'):
        headers.append(str(H.remove_non_ascii(c.text)).strip())

    res=[]
    for r in t.find_all('tr')[1:]:
        d={ 'Condition':'',
            'Explanation':'',
            'Note':'',}
        pt=0
        for c in r.find_all('td'):
            d[ headers[pt] ] = str(H.remove_non_ascii(c.text)).strip()
            pt+=1

        _condition = d[ headers[0] ]
        matches = re.match(r'(.*)(\[[0-9]+\])+$',_condition)
        if matches:
            fnts=list(matches.groups())
            _note=''
            for n in fnts[1:]:
                rpt = _condition.rfind(n)
                _condition = _condition[:rpt] + _condition[rpt:].replace(n,'',1)
                t = eval(n)[0]
                _note+=notes[ t ]
            d.update({'Condition':_condition,
                      'Note':_note,})
        res.append(d)

    j = json.dumps(res)
    with open(store_file,'w') as f: f.write(j)
    cmd = ';'.join(["cat %s | jq -Mr '.' > tmp" % store_file,
                    'cat tmp > %s' % store_file,
                    'rm tmp && echo true'])
    assert run_cmd(cmd)=='true'

def get(update='auto'):
    if update=='auto' or update!=False:
        update_store(update)
    import pandas as pd
    with open(store_file,'r') as f:
        x=json.loads( f.read() )
    return pd.DataFrame(x)

