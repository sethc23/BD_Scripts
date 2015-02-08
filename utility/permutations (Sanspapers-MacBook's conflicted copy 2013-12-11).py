'''
Created on Nov 21, 2013

@author: sethchase
'''
from sys import path
path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
from variables import listFout, listFin

def genperm(iter_count):
    from itertools import permutations
    return permutations(iter_count)

def genOrderedPairPerm(pairCount,generator=False,printThis=False):
    from API_system import checkFilePathExists,getFilesFolders
    basePath='/Users/admin/Desktop/seamless/sim_data/'
    filePath=basePath+'OrderedPairPerm-'+str(pairCount)+'-0.txt'
    if checkFilePathExists(filePath):
        z=getFilesFolders(basePath)
        p=len(str(z).split('OrderedPairPerm-'+str(pairCount)))-1
        z=[]
        for i in range(0,p):
            filePath=basePath+'OrderedPairPerm-'+str(pairCount)+'-'+str(i)+'.txt'
            if generator == False:
                a=listFin(filePath)
                z.extend(a)
            else:
                z.append(filePath)
        if generator == False: return z
        if generator == True: return fileDataGenerator(z)
    else:
        if pairCount > 26: 
            print "too many pairs"
            raise SystemExit
        return gen_good_perms(pairCount,pairCount+1)

def fileDataGenerator(fileList):
    for i in range(0,len(fileList)):
        f=open(fileList[i],'r')
        x=f.read()
        f.close()
        yield eval('['+x.replace('\n',',')+']')

def genAllPairPerm_NoRep(pairCount,choose,generator=False,printThis=False):
    from API_system import checkFilePathExists
    basePath='/Users/admin/Desktop/seamless/sim_data/AllPairPerm_NoRep-'
    filePath=basePath+str(pairCount)+'.txt'
    if checkFilePathExists(filePath):
        return listFin(filePath)
    else:
        # formula = n! / (n-r)!
        if pairCount > 26: 
            print "too many pairs"
            raise SystemExit
        return gen_good_combos(pairCount,choose)

''
def compareRows(first,second,*s):
    if [x for x in s].index(first)>[x for x in s].index(second): return 'no'
    else: return 'yes'

def combine(*items):
    return str([x for x in items])

def genSeg(segSize,generator):
    num = 0
    while num < segSize:
        yield generator.next()
        num += 1

def genPerm_limited(L1,L2): #iterate between lengths of perms
    from time import time
    from itertools import permutations
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    abc=ABC.lower()
    seg=10000
    for i in range(L1,L2):
        t1=time()
        x_A=ABC[:i]
        x_B=ABC[i:i*2]
        z=list(x_A+x_B)
    
        a=permutations(z)
        pt,seg=0,seg
        b=genSeg(seg,a)
        p=list(b)
        while len(p) == seg:
            y=str(p)
            for j in range(0,len(x_A)):
                y=y.replace(x_A[j],x_A[j]+'1')
                y=y.replace(x_B[j],x_A[j]+'2')
            b=y
            saveIndex=''
            for it in x_A:
                c=b.replace(it,'')
                z=list(x_A.replace(it,''))
                for r in z:
                    c=c.replace("'"+r+'1'+"'",'0')
                    c=c.replace("'"+r+'2'+"'",'0')
                c=c.replace("'"+'1'+"'",'1')
                c=c.replace("'"+'2'+"'",'2')
                d=pd.DataFrame(eval(c),columns=list(abc[:i*2]))
                d=d.fillna(0)
                if saveIndex!='': d=d.iloc[saveIndex,:]
                if len(d.index) > 0:
                    d['save']=d.apply(lambda s: compareRows(1,2,*s),axis=1)
                    saveIndex=d[(d['save']=='yes')].index
            d=pd.DataFrame(eval(b))
            d=d.iloc[saveIndex,:]
            if len(d.index) > 0:
                d['save']=d.apply(lambda s: combine(*s),axis=1)
                basePath='/Users/admin/Desktop/seamless/sim_data/permutations/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
                listFout(d['save'].tolist(),basePath)        
                pt+=1
            b=genSeg(seg,a)
            p=list(b)
        
        #-----------
        
        for j in range(0,len(x_A)):
            y=y.replace(x_A[j],x_A[j]+'1')
            y=y.replace(x_B[j],x_A[j]+'2')
        b=y
        saveIndex=''
        for it in x_A:
            c=b.replace(it,'')
            z=list(x_A.replace(it,''))
            for r in z:
                c=c.replace("'"+r+'1'+"'",'0')
                c=c.replace("'"+r+'2'+"'",'0')
            c=c.replace("'"+'1'+"'",'1')
            c=c.replace("'"+'2'+"'",'2')
            d=pd.DataFrame(eval(c),columns=list(abc[:i*2]))
            d=d.fillna(0)
            if saveIndex!='': d=d.iloc[saveIndex,:]
            d['save']=d.apply(lambda s: compareRows(1,2,*s),axis=1)
            saveIndex=d[(d['save']=='yes')].index
        d=pd.DataFrame(eval(b))
        d=d.iloc[saveIndex,:]
        if len(d.index) > 0:
            d['save']=d.apply(lambda s: combine(*s),axis=1)
            basePath='/Users/admin/Desktop/seamless/sim_data/permutations/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
            listFout(d['save'].tolist(),basePath)        
            pt+=1
        t2=time()
        print t2-t1
''

def all_perms(elements):
    #print '-----',elements
    a=''
    
    if len(elements) <=1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                #nb elements[0:1] works in both string and list contexts
                #print elements,perm,i
                #print perm[:i] + elements[0:1] + perm[i:]
                #if (type(perm[:i]) != list and perm[:i].find('2')==-1): 
                yield perm[:i] + elements[0:1] + perm[i:]

def all_pair_perms(elements,choose):
    from itertools import permutations
    return permutations(list(elements),2)

def good_perms(elements):
    z=[]
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_perms(z):
        add=True
        for it in elements:
            q=''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            if [int(s) for s in list(q) if s.isdigit()] != sorted([int(s) for s in list(q) if s.isdigit()]):
                add=False
                break
        if add==True: yield perm

def good_combos(elements,choose):
    z=[]
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_pair_perms(z,choose):
        add=True
        for it in elements:
            q=''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            if [int(s) for s in list(q) if s.isdigit()] != sorted([int(s) for s in list(q) if s.isdigit()]):
                add=False
                break
        if add==True: yield eval(str(perm).replace('(','[').replace(')',']'))

def gen_good_perms(L1,L2):
    from time import time
    t1= time()
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    abc=ABC.lower()
    seg=10000
    for i in range(L1,L2):
        t1=time()
        b=list(ABC[:i])
        q=good_perms(b)
        b=genSeg(seg,q)
        p=list(b)
        pt=0
        basePath='/Users/admin/Desktop/seamless/sim_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
        listFout(p,basePath)
        pt+=1
        while len(p) == seg:
            b=genSeg(seg,q)
            p=list(b)
            basePath='/Users/admin/Desktop/seamless/sim_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
            listFout(p,basePath)
            pt+=1
        t2= time()
        print i,t2-t1
    return p

def gen_good_combos(pairCount,choose):
    ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    b=list(ABC[:pairCount])
    q=good_combos(b,choose)
    g=list(q)
    basePath='/Users/admin/Desktop/seamless/sim_data/AllPairPerm_NoRep-'
    filePath=basePath+str(pairCount)+'.txt'
    listFout(g,filePath)
    return g
    

#gen_good_perms(5,6)
#gen_good_combos(5,2)
