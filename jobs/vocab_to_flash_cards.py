from appscript import *

def gotoUrl(word):
    link = 'http://www.thefreedictionary.com/' + word
    app(u'Safari').activate()
    app(u'Safari').documents[1].URL.set(link)


def makeTemplate(pos, var):
    if pos == 'ends':
        title, desc, middle = var
        start = ('<?xml version="1.0" encoding="utf-8"?>\n' + 
        '<qset><name>' + title + '</name>\n' + 
        '<description>' + desc + '</description>\n')
        end = ('</qset>')
        template = start + middle + end
    elif pos == 'middle':
        question, answer = var
        template = ('<qtext>' + question + '</qtext>\n' + 
        '<atext>' + answer + '</atext>\n')
    return template


f = open('/Users/admin/Dropbox/Personal/vocab_list.txt', 'r')
x = f.read()
f.close()

a = x.split('\n')

iterNum = eval(raw_input('How many words?\n'))
print ''

output = ''
for i in range(0, iterNum):
    word = a[i]
    gotoUrl(word)
    definition = raw_input('Definition?\n')
    var = word, definition
    output = output + makeTemplate('middle', var)

title = "Vocab"
desc = "Words-Definitions"
middle = output
var = title, desc, middle
output = makeTemplate('ends', var)

f = open('/Users/admin/Desktop/2010_12_28_vocab_list.xml', 'w')
f.write(output)
f.close()

