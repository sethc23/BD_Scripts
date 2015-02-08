
def cleanTitle(s):
    clean = ['<b>', '</b>', '<i>', '</i>', '<br>', '\n', '[Go To Supp]', '[Go To Main]', '  ']
    qw = s.decode('UTF-8')
    s = qw.encode('ascii', 'replace').replace('?', ' ')
    for dirt in clean:
        s = s.replace(dirt, ' ')
    if s.count('<span') != 0:
        for i in range(0, s.count('<span')):
            pt = s.find('<span')
            e = s.find('</span>') + len('</span>')
            s = s[:pt] + s[e:]
    return s.strip()


p = '/Users/admin/Reference/Law/Chisum on Patents.html'
dirPath = '/Users/admin/Reference/Law/Chisum/'
dirPath2 = '/Users/admin/Reference/Law/Chisum2/'

f = open(p, 'r')
x = f.read()
f.close()

header = x[:x.find('<body>')]
'''
footer='</html>\n'
splitTag='<p class="p6">'

w=x.split(splitTag)
t=[]

for i in range(1,221):
    item=w[i]
    s=item[:item.find('</p>')]

    s=cleanTitle(s)


    
    if s[0].isdigit():
        f=open(dirPath+s+'.html','w')
        f.write(header+splitTag+item+footer)
        f.close()
        t.append(s)


newHeader=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'+
           '<html xmlns="http://www.w3.org/1999/xhtml">\n'+
            '<head>'+
            '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n'+
            '<title>Chisum On Patents - INDEX</title>\n'+
            '</head>\n'+
            '<body>\n')
linkForm='<a href="LINK">TITLE</a>'
newFooter=('</body>\n</html>')
htmlText=newHeader
for pt in t:
    newLink=linkForm.replace('LINK',dirPath+pt+'.html').replace('TITLE',pt)
    htmlText=htmlText+newLink+'<br>\n'

htmlText=htmlText+newFooter

f=open(dirPath+'Chisum_Index.html','w')
f.write(htmlText)
f.close()
'''

files = ['1 Introduction.html',
'2 Constitutional Enablement: The 1790 and 1793 Acts.html',
'3 The 1836 and 1870 Acts.html',
'4 The First Invention Concept.html',
'5 Shifting Supreme Court Attitudes Toward Patents.html',
'6 The 1952 Act.html',
'7 The 1966 Graham Trilogy and Beyond.html',
'1.01 Introduction.html',
'1.02 Products.html',
'1.03 Processes.html',
'1.04 Design Patents.html',
'1.05 Plants.html',
'1.06 Inventions Relating to National Security, Atomic Energy, and Aeronautics and Space.html',
'2.01 Introduction.html',
'2.02 Joint and Sole Inventorship.html',
'2.03 Proper Joinder of Inventors Correct Naming of Inventors.html',
'2.04 Correction of Inventorship Errors.html',
'3.01 Introduction.html',
'3.02 The Standard of Anticipation.html',
'3.03 Accidental and Unintended Anticipations Inherency.html',
'3.04 Description in a Publication.html',
'3.05 Knowledge, Use or Invention.html',
'3.06 Patenting.html',
'3.07 Description in United States Patent.html',
'3.08 The Date of Invention.html',
'4.01 Introduction.html',
'4.02 Minimum Utility.html',
'4.03 Illegal, Immoral, and Harmful Inventions.html',
'4.04 Proof of Utility and Operability.html',
'5.01 Introduction.html',
'5.02 Historical Development.html',
'5.03 Factual Inquiries: The Pertinent Art.html',
'5.04 The Conclusion as to Obviousness.html',
'5.05 Secondary Considerations.html',
'5.06 Proof of Obviousness.html',
'6.01 Introduction.html',
'6.02 Delay in Filing Application Section 102(b).html',
'6.03 Abandonment Section 102(c).html',
'6.04 Foreign Patenting Section 102(d).html',
'7.01 Introduction.html',
'7.02 Historical Development.html',
'7.03 The Enablement Requirement.html',
'7.04 The Description Requirement.html',
'7.05 The Best Mode Requirement.html',
'8.01 Introduction.html',
'8.02 Historical Development.html',
'8.03 Definiteness and Particularity of Claims.html',
'8.04 Functional Language in Claims.html',
'8.05 Product-By-Process Claims.html',
'8.06 Selected Problems in Claim Drafting.html',
'9.01 Introduction.html',
'9.02 Historical Development Supreme Court Cases.html',
'9.03 The Standard of Duplicity.html',
'9.04 Terminal Disclaimers.html',
'9.05 Different Inventors with a Common Assignee.html',
'10.01 Introduction.html',
'10.02 Historical Development.html',
'10.03 Priority Rules.html',
'10.04 Conception.html',
'10.05 Constructive Reduction to Practice.html',
'10.06 Actual Reduction to Practice.html',
'10.07 Diligence.html',
'10.08 Abandonment, Suppression and Concealment.html',
'10.09 Interference Procedure.html',
'11.01 Introduction.html',
'11.02 Application.html',
'11.03 Examination and Prosecution.html',
'11.04 Amendments New Matter.html',
'11.05 Late Claiming.html',
'11.06 Appeals.html',
'11.07 Post-Allowance Procedures Reexamination.html',
'12.01 Introduction.html',
'12.02 Historical Development.html',
'12.03 The Independent and Distinct Standard.html',
'12.04 Procedure for Division and Election.html',
'12.05 Double Patenting.html',
'12.06 Misjoinder.html',
'13.01 Introduction.html',
'13.02 Historical Development.html',
'13.03 Definitions.html',
'13.04 Continuity of Disclosure.html',
'13.05 Copendency Number of Applications Abuse of Patent Prosecution Equitable Estoppel.html',
'13.06 Cross-Referencing Specific Reference to Earlier Filed Applications.html',
'13.07 Identity of Inventorship.html',
'14.01 Introduction.html',
'14.02 Historical Development.html',
'14.03 Requirements for Priority.html',
'14.04 Procedure for Establishing Priority; Formalities.html',
'14.05 Effect of Priority.html',
'15.01 Introduction.html',
'15.02 Historical Development.html',
'15.03 Requirements for Reissue.html',
'15.04 Reissue Procedure.html',
'15.05 Effect of Reissue.html',
'15.06 Exclusiveness of Reissue as a Remedy for Expanding Claim Coverage.html',
'16.01 Introduction.html',
'16.02 Rights Conferred.html',
'16.03 Limitations.html',
'16.04 Temporal Scope Period of Monopoly.html',
'16.05 Territorial Scope.html',
'16.06 Corporate and Government Infringers.html',
'17.01 Introduction.html',
'17.02 Historical Development.html',
'17.03 Sale of a Component Section 271(c).html',
'17.04 Active Inducement Section 271(b).html',
'17.05 Privilege as to Misuse Section 271(d).html',
'18.01 Introduction.html',
'18.02 Historical Development.html',
'18.03 Claim Construction Infringement Determination.html',
'18.03 Claim Construction Infringement Determination (cont).html',
'18.04 Doctrine of Equivalents.html',
'18.05 Prosecution History (File Wrapper) Estoppel.html',
'18.06 Proof of Infringement.html',
'18.07 Case Examples Selected Technologies.html',
'19.01 Introduction.html',
'19.02 Invalidity.html',
'19.03 Fraudulent Procurement Inequitable Conduct.html',
'19.04 Misuse.html',
'19.05 Delay in Filing Suit: Laches and Estoppel.html',
'19.06 Bad Faith Enforcement.html',
'20.01 Introduction.html',
'20.02 Historical Development.html',
'20.03 Monetary Relief.html',
'20.04 Injunctive Relief.html',
'21.01 Introduction.html',
'21.02 Jurisdiction and Venue.html',
'21.03 Parties.html',
'22.01 Introduction.html',
'22.02 Ownership and Inventorship: The Procedural Context of Ownership Disputes.html',
'22.03 The Employed Inventor.html',
'23.01 Introduction.html',
'23.02 Historical Development.html',
'23.03 Requirements for Patentability.html',
'23.04 Specification and Claim Continuation Applications.html',
'23.05 Infringement.html',
'23.06 Relation to Copyright Protection.html',
'23.07 Relation to Trademark Protection and Unfair Competition.html',
'23.08 Relation to Utility Patent Protection.html',
'24.01 Introduction.html',
'24.02 The Plant Patent Act.html',
'24.03 Plant Variety Protection: Patent-Like Protection for Sexually Reproduced Plants 1.html',
'24.04 Protecting Plant Material under Section 101.html',
'24.05 Comparing the PVPA, Plant Patent Act, and Utility Patent Protection for Plants.html']

# get tags with blue heading in order to make general index
'''
styleTag=header[header.find('<style'):header.find('</style>')+len('</style>')]
pt=0
for i in range(0,styleTag.count('\n')):
    n_pt=styleTag.find('\n',pt)+2
    prop=styleTag[pt:n_pt]
    pt=n_pt
    if prop.find('#0000ff')!=-1:
        print "'"+prop[:prop.find('{')].strip()+"',"
'''

# add table of contents to top
'''
addTags=['p6',
        'p9',
        'p14',
        'p16',
        'p17',
        'p25',
        'p45']
end=False
anchorForm='<a name="LINK">'
linkForm='<a href="#LINK">TITLE</a>'
htmlSpace=' &nbsp;'
alphabet='abcdefghijklmnopqrstuvwxyz'
num=0
for item in files[:31]:
    #print item
    f=open(dirPath+item,'r')
    x=f.read()
    f.close()
    p=0
    alpha_start=False
    linkBlock=''
    
    tr=[]
    for i in range(0,x.count(' class="p')):
        n_p=x.find(' class="p',p)
        p=n_p+len(' class="p')-1
        if addTags.count(x[p:p+x[p:].find('"')]) != 0:
            #print x[p:p+x[p:].find('"')]
            s_p=x[:n_p].rfind('<')
            title=x[n_p+x[n_p:].find('>')+1:n_p+x[n_p:].find('</p>')]
            newTitle=cleanTitle(title)
            linkTitle=newTitle.replace('.','_').replace(' ','_')
            if linkTitle[0]!='[':
                linkSpace=''
            elif linkTitle[1].isdigit():
                linkSpace=htmlSpace*3
                if alpha_start==True:
                    alpha_start==False
                    next_alpha_pt=alphabet[0]
            elif linkTitle[1].isalpha():
                linkSpace=htmlSpace*6
                alpha_pt=linkTitle[1]
                #print linkTitle
                if alpha_start==False:
                    next_alpha_pt=alphabet[alphabet.index(alpha_pt)+1]
                    alpha_start=True
                    #print 'start'
                else:
                    if alpha_pt == next_alpha_pt:
                        next_alpha_pt=alphabet[alphabet.index(alpha_pt)+1]
                        #print 'roman'
                    elif alpha_pt.isupper():
                        linkSpace=htmlSpace*12
                    else:
                        linkSpace=htmlSpace*9
                        
                
            replOrig=x[s_p:s_p+x[s_p:].find('</p>')+4]
            
            replNew=(replOrig[:replOrig.find('>')+1]+
                     anchorForm.replace('LINK',linkTitle)+
                     replOrig[replOrig.find('>')+1:replOrig.rfind('</p>')]+'</a></p>')
            
            x=x.replace(replOrig,replNew,1)

            linkBlock=linkBlock+linkSpace+linkForm.replace('LINK',linkTitle).replace('TITLE',newTitle)+'<br>\n'


    x=x[:x.find('</head>')+len('</head>')]+'\n'+linkBlock+'<br><br><br>'+x[x.find('</head>')+len('</head>'):]
    f=open(dirPath2+item,'w')
    f.write(x)
    f.close()
'''

# ## add {go to main index at each section, go to top index at each section} and clean titles

addTags = ['p6',
        'p9',
        'p14',
        'p16',
        'p17',
        'p25',
        'p45']
anchorForm = '<a name="LINK">'
linkForm = '<a href="#LINK">TITLE</a>'
htmlSpace = ' &nbsp;'
for item in files:
    # print item
    f = open(dirPath + item, 'r')
    x = f.read()
    f.close()
    p = 0

    e = x.find('href="#') + len('href="#')
    x = x[:e].replace(' href="#', ' name="Top_Index"' + ' href="#', 1) + x[e:]
    x = x.replace('[Go To Supp]', '')

    for i in range(0, x.count(' class="p')):
        n_p = x.find(' class="p', p)
        p = n_p + len(' class="p') - 1
        if addTags.count(x[p:p + x[p:].find('"')]) != 0:
            # print x[p:p+x[p:].find('"')]
            s_p = x[:n_p].rfind('<')
            
            origParaTag = x[s_p:s_p + x[s_p:].find('</p>') + 4]
            newTagEnd = '</b></a> &nbsp; &nbsp; &nbsp;<a href="#Top_Index"><b> [TOP] </b></a> &nbsp; &nbsp; &nbsp;<a href="Chisum_Index.html"><b> [MAIN INDEX] </b></a></p>'
            newParaTag = origParaTag.replace('</b></a></p>', newTagEnd)
            
            x = x.replace(origParaTag, newParaTag, 1)

    f = open(dirPath2 + item, 'w')
    f.write(x)
    f.close()
