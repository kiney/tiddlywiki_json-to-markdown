#!/usr/bin/python3

# slice a tiddlywiki json export into individual files
# (hacked together for migration tiddlywiki->gollum + gitlab wiki

import json
import re

tids = json.load(open('tiddlers.json', 'r'))

def ex_date(d):
    return '%s-%s-%s'%(d[:4], d[4:6], d[5:7])

def convert_some_stuff(r):
    '''
    very minimal conversion to markdown
    '''
    r = re.sub('(?m)^!!!', '### ', r)
    r = re.sub('(?m)^!!', '## ', r)
    r = re.sub('(?m)^!', '# ', r)
    r = re.sub('(?m)^\*', '* ', r)
    r = r.replace('{{{', '```')
    r = r.replace('}}}', '```')
    return r

for t in tids:
    ti = t['title']
    co = convert_some_stuff(t['text'])
    cr = ex_date(t['created'])
    if 'modified' in t:
        mo = ex_date(t['modified'])
    else:
        mo = cr
    if 'tags' in t:
        ta = t['tags']
    else:
        ta = ''
    o = 'tiddly/%s.md'%(ti.replace('/', '-'))
    o = o.replace(' ', '-')
    with open(o, 'w') as w:
        w.write(co)
        w.write('\n\n')
        w.write('created: %s\n'%cr)
        w.write('modified: %s\n'%mo)
        w.write('tags: %s\n\n'%ta)
