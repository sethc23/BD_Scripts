# Utility & Permutation f(x)s
from rd_lib import pd,combinations,this_cwd,time
from pg_fxs import pg_get_travel_dist
from assumptions import MPH
from os import path as os_path
from os import listdir as os_listdir

def get_all_node_combo_dist_miles(node_array,clean=False):
    if clean==False:
        uniq_node_arr = dict(zip(node_array.tolist(),range(node_array.shape[0]))).keys()
    else:
        uniq_node_arr = node_array
    node_array1,node_array2 = [],[]
    for it in combinations(uniq_node_arr,2):
        node_array1.append(it[0])
        node_array2.append(it[1])
    dist_in_miles = pg_get_travel_dist(node_array1,node_array2)

    d = pd.DataFrame({  'A'     : node_array1,
                        'B'     : node_array2,
                        'dist'  : dist_in_miles})
    d['minutes'] = d.dist.map(lambda f: round((float(f)/float(MPH))*60,1))
    return d

    #     c.append(it)
    # x=np.array(c).T
    # print x[0].tolist()
    # print x[1].tolist()

def systemError():
    if alert_bell == True:
        cmd='say -v Bells "dong"'
        # system(cmd)

    print time(),'systemError()'
    raise SystemError

def listFin(F_in,delimiter=''):
    L_out = []
    if delimiter=='':
        fin = open(F_in, 'r')
        data = fin.readlines()
        fin.close()
        for row in data:
        #    #L_out.append(float(data[i]))
            try:
                L_out.append(eval(row))
            except:
                L_out.append(row)
        return L_out
    else:
        fin = open(F_in, 'r')
        data = fin.read()
        fin.close()
        data=data.split('\r')
        for row in data:
            nrow=row.split(delimiter)
            row_vars=[]
            for it in nrow:
                try:
                    row_vars.append(eval(it))
                except:
                    row_vars.append(it)
            L_out.append(row_vars)
        return L_out
def listFout(L_in, F_out):
    row = len(L_in)
    fileArray = []
    for line in range(0, row):
        fileArray.append(L_in[line])
    fmin = open(F_out, "w")
    for i in range(0, row):
        line = str(fileArray[i])
        fmin.writelines(line)
        fmin.writelines('\n')
    fmin.close()
def getFilesFolders(workDir, full=False):
    x = os_listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    popList, y = [], []
    for i in range(0, len(x)):
        if os_path.isdir(x[i]):
            popList.append(i)
        else: y.append(workDir.rstrip('/')+'/'+x[i])
    popList.reverse()
    for it in popList: x.pop(it)
    if full == False: return x
    else:
        return y
def fileDataGenerator(fileList):
    for i in range(0,len(fileList)):
        f   = open(fileList[i],'r')
        x   = f.read()
        f.close()
        yield eval('['+x.replace('\n',',')+']')
def genSeg(segSize,generator):
    num = 0
    while num < segSize:
        yield generator.next()
        num += 1

def all_perms(elements,choose=''):
    from itertools import permutations
    if choose!='':  return permutations(list(elements),choose)
    else:           return permutations(list(elements))

def get_pair_combos(elements,choose):
    z=[]
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_perms(z,choose):
        add=True
        for it in elements:
            q=''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            x = [int(s) for s in list(q) if s.isdigit()]
            if x != sorted(x):
                add=False
                break
        if add==True: yield eval(str(perm).replace('(','[').replace(')',']'))
def gen_pair_combos(pairCount,choose):
    ABC         = 'ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    b           = list(ABC[:pairCount])
    q           = get_pair_combos(b,choose)
    g           = list(q)
    basePath    = this_cwd + 'perm_data/AllPairPerm_NoRep-'
    filePath    = basePath+str(pairCount)+'.txt'
    listFout(g,filePath)
    return g
def genAllPairPerm_NoRep(pairCount,choose,generator=False,printThis=False):
    basePath    = this_cwd + 'perm_data/AllPairPerm_NoRep-'
    filePath    = basePath+str(pairCount)+'.txt'
    if os_path.isfile(filePath):
        return listFin(filePath)
    else:
        # formula = n! / (n-r)!
        if pairCount > 26:
            print "too many pairs"
            systemError()
        return gen_pair_combos(pairCount,choose)

def get_struct_perms(elements):
    z   = []
    for it in elements:
        z.append(it+'1')
        z.append(it+'2')
    for perm in all_perms(z):
        add = True
        for it in elements:
            q   = ''.join(perm).replace(it+'1','3').replace(it+'2','4').replace('1','').replace('2','')
            x   = [int(s) for s in list(q) if s.isdigit()]
            if x != sorted(x):
                add = False
                break
        if add==True: yield eval(str(perm).replace('(','[').replace(')',']')) # yield perm
def gen_struct_perms(L1,L2,save=False,test=False):
    t1          = time()
    ABC         = 'ABCDEFGHIJKLMNOPQRUSTUVXYZ'
    seg_size    = 5000
    for i in range(L1,L2):
        t1          = time()
        pts         = list(ABC[:i])
        perm_gen    = get_struct_perms(pts)
        gen_part    = genSeg(seg_size,perm_gen)
        seg_res     = list(gen_part)
        pt          = 0

        if test==True:
            import pandas as pd
            df_cols     = [it.lower() for it in seg_res[0]]
            df          = pd.DataFrame(seg_res,columns=df_cols)
            for _pt in pts:
                test    = df.apply(lambda s: [[it for it in s]],axis=1)
                step    = test.map(lambda s: [s[0].index(_pt+'1'),s[0].index(_pt+'2')])
                check   = step.map(lambda s: True if sorted(s)==s else False)
                if len(check[check==False])>0:
                    print 'trouble in china town'
                    raise SystemError()

        basePath    = this_cwd + 'perm_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
        if save==True:  listFout(seg_res,basePath)
        pt += 1
        while len(seg_res) == seg_size:
            gen_part    = genSeg(seg_size,perm_gen)
            seg_res     = list(gen_part)

            if test==True:
                df          = pd.DataFrame(seg_res,columns=df_cols)
                for _pt in pts:
                    test    = df.apply(lambda s: [[it for it in s]],axis=1)
                    step    = test.map(lambda s: [s[0].index(_pt+'1'),s[0].index(_pt+'2')])
                    check   = step.map(lambda s: True if sorted(s)==s else False)
                    if len(check[check==False])>0:
                        print 'trouble in china town2'

            basePath    = this_cwd + 'perm_data/OrderedPairPerm-'+str(i)+'-'+str(pt)+'.txt'
            if save==True:  listFout(seg_res,basePath)
            pt += 1
        t2  = time()
    return
def genAllStructPerm(pairCount,generator=False,printThis=False,test=False):
    basePath    = this_cwd+'perm_data/'
    filePath    = basePath+'OrderedPairPerm-'+str(pairCount)+'-0.txt'
    if os_path.isfile(filePath):
        z   = getFilesFolders(basePath)
        p   = len(str(z).split('OrderedPairPerm-'+str(pairCount)))-1
        z   = []
        for i in range(0,p):
            filePath    = basePath+'OrderedPairPerm-'+str(pairCount)+'-'+str(i)+'.txt'
            if generator == False:
                a   = listFin(filePath)
                z.extend(a)
            else:
                z.append(filePath)
        if generator == False:  return z
        if generator == True:   return fileDataGenerator(z)
    else:
        if pairCount > 26:
            print "too many pairs"
            systemError()
        x = gen_struct_perms(pairCount,pairCount+1,save=True,test=test)
        return genAllStructPerm(pairCount)