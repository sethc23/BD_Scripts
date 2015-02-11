
from sys import argv
from rd_lib import pd,np,this_cwd
from assumptions import max_delivery_per_dg

from utility_and_permutation_fxs import genAllStructPerm,genAllPairPerm_NoRep,get_pair_combos
from fxs_for_fxs import pd_combine,pd_create_sortKey
from os.path import isfile
from os import remove as os_remove

# Local Vars:
ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'
mock_to_num_dict=dict(zip([it+'1' for it in ABC[:max_delivery_per_dg]],np.arange(0,(len(ABC)+1),1).astype(np.intc)))
mock_to_num_dict.update(dict(zip([it+'2' for it in ABC[:max_delivery_per_dg]],np.arange(100,100*(len(ABC)+1),1).astype(np.intc))))


def make_initial_ptPairSet_store():
    b                   = list(ABC[:max_delivery_per_dg])
    z                   = list(get_pair_combos(b,2))
    x                   = pd.DataFrame(z,columns=['a','b'])
    char_int_dict       = { 'A1':0,'A2':1,
                            'B1':2,'B2':3,
                            'C1':4,'C2':5,
                            'D1':6,'D2':7,
                            'E1':8,'E2':9,
                            'F1':10,'F2':11,
                            'G1':12,'G2':13,
                            'H1':14,'H2':15,
                            'I1':16,'I2':17  }
    x['a']              = x.a.map(char_int_dict)
    x['b']              = x.b.map(char_int_dict)
    x                   = x.apply(lambda s: "[%s,%s]"%(sorted([s[0],s[1]])[0],sorted([s[0],s[1]])[1]),axis=1)
    a                   = x.unique().tolist()
    ppd                 = pd.DataFrame({'pair_idx':map(lambda s: eval(s),a)})
    ppd.to_hdf(this_cwd+'/perm_data/store_ptPairSet.h5','table',append=False)
    return ppd
def set_ptPair_order(pts,ptPairSet,save_to_hdf=True):
    seg_start           = pts.columns.tolist().index('pp_0')
    seg_e_pt            = seg_start+3
    sortCol,sort_asc    = [],[]
    for i in range(2,max_delivery_per_dg+1):
        i_col           = 'mc'+str(i)
        z               = np.unique(pts[pts[i_col]==True].ix[:,seg_start:seg_e_pt].as_matrix().flatten())
        ptPairSet[i_col]= ptPairSet.index.isin(z)
        seg_e_pt       += 2
        # if i==2:      seg_e_pt   += 1
        sortCol.append(i_col)
        sort_asc.append(False)
    ptPairSet           = ptPairSet.sort(columns=sortCol,ascending=sort_asc).reset_index(drop=True)
    if save_to_hdf==True:   ptPairSet.to_hdf(this_cwd+'/perm_data/store_ptPairSet.h5','table',append=False)
    return ptPairSet
def add_ptPair_info_to_orderSet(pts=False,ptPairSet=False,save_to_hdf=True):
    """
    ------
    <<  SUMMARY:

    ptPairSet provides an index connecting:
        (a) mockCombo routes, and
        (b) all possible pair permutations.

    >>

    ------
    <<  EXPLANATION:

    testSet:    all permutations for 2 deliveries (4 points),
                where pickup (single digits) comes before dropoff (100s #s)

    demo_vars:  for demonstration purposes, an index is applied to testSet,
                where testSet vars {0,100,1,101} is mapped to {0,1,2,3}

    testSet             demo_vars
    0   100 1   101     0   1   2   3
    0   1   100 101     0   2   1   3
    0   1   101 100     0   2   3   1
    1   0   100 101     2   0   1   3
    1   0   101 100     2   0   3   1
    1   101 0   100     2   3   0   1


    ptPairSet:  a list of possible pair permutations.
                the list contains pairs of SORTED demo_vars.


        i={}  ptPairSet
        0       0   1
        1       0   2
        2       0   3
        3       1   2
        4       1   3
        5       2   3


    Each segment of a route (e.g., 0 to 100, 100 to 1, 1 to 101, etc...) can now be mapped using the ptPairSet.

    ptPairSK:   an index is generated for each row in testSet.
                'SK' stands for 'Sort Key'
                # route segments   ==   # route points - 1


    testSet             demo_vars           ptPairSK
    0   100 1   101     0   1   2   3       0   3   5
    0   1   100 101     0   2   1   3       1   3   4
    0   1   101 100     0   2   3   1       1   5   4
    1   0   100 101     2   0   1   3       1   0   4
    1   0   101 100     2   0   3   1       1   2   4
    1   101 0   100     2   3   0   1       5   2   0

    >>
    """
    pts_path                = this_cwd+'/perm_data/store_orderSet.h5'
    if type(pts)==bool: pts = pd.read_hdf(pts_path,'table')
    if type(pts)==bool:
        ptPairSet           = make_initial_ptPairSet_store()
    num_int_dict        = { 0:0,  100:1,
                            1:2,  101:3,
                            2:4,  102:5,
                            3:6,  103:7,
                            4:8,  104:9,
                            5:10, 105:11,
                            6:12, 106:13,
                            7:14, 107:15,
                            8:16, 108:17 }
    ptPairSet           = ptPairSet.pair_idx.tolist()
    cols                = pts.columns.tolist()
    c_i                 = 1 + cols.index('pt0')
    c_i_end             = cols.index('pt'+str(2*max_delivery_per_dg-1))
    pt                  = -1
    for i in range(c_i,1 + c_i_end):        # below is sorted less->more to reduce number of possible pair permutations
        pt                 += 1
        pts['pp_'+str(pt)]  = pts.ix[:,[cols[i-1],cols[i]]].apply(lambda s:     ptPairSet.index(eval("[%s,%s]"%(num_int_dict[s[0]],
                                                                                                           num_int_dict[s[1]])))
                                                                                if num_int_dict[s[0]] <= num_int_dict[s[1]] else
                                                                                ptPairSet.index(eval("[%s,%s]"%(num_int_dict[s[1]],
                                                                                                           num_int_dict[s[0]]))),
                                                                  axis=1)
        #import embed_ipython as I; I.i_trace()
    if save_to_hdf==True:   pts.to_hdf(pts_path,'table',append=False)
    return pts

def make_orderSet_store(test=False):
    """
    ptPairSet (a subset of orderSet) is made by:
        1. make orderSet
        2. generate generic ptPairSet           ->  make_initial_ptPairSet_store
        3. add ptPairSet info to orderSet       ->  add_ptPair_info_to_orderSet
        4. sort ptPairSet by mc#
        5. redo ptPairSet info (3)

    """
    ptCols      = ['pt'+str(it) for it in range(0,max_delivery_per_dg*2)]
    pts         = pd.DataFrame(genAllStructPerm(max_delivery_per_dg),columns=ptCols)
    for it in ptCols:   pts[it]         = pts[it].map(mock_to_num_dict)
    pts['mc'+str(max_delivery_per_dg)]  = pts.apply(lambda x: True, axis=1)
    pts['mockComboMax'] = pts[ptCols].apply(lambda x: [pd_combine(*x)], axis=1).ix[:,0]
    pts['mockComboMax'] = pts['mockComboMax'].map(lambda s: eval(s))

    for i in np.arange(max_delivery_per_dg-1,1,-1):
        ptsCols     = ['pt'+str(it) for it in range(0,i*2)]
        ptsTemp     = pd.DataFrame(genAllStructPerm(i),columns=ptsCols)
        for it in ptsCols:
            ptsTemp[it] = ptsTemp[it].map(mock_to_num_dict)
        ptsTemp['mc']   = ptsTemp.apply(lambda x: str(pd_combine(*x)), axis=1)

        pts['temp']     = pts[ptsCols].apply(lambda x: str(pd_combine(*x)), axis=1)
        pts['isdupe']   = pts.duplicated(['temp'])
        pts['mc'+str(i)]= pts.temp.where(pts.temp.isin(ptsTemp.mc.tolist())==True).where(pts.isdupe == False).apply(lambda s: True if type(s)==str else False)

    # columns a1,a2,b1,b2,etc... identify index for THAT POINT ONLY
    # i need index
    dropCols    = []
    dropCols.extend(['temp','isdupe'])
    for it in ABC[:max_delivery_per_dg]:
        pts[it.lower()+'1'] = pts['mockComboMax'].apply(lambda x: x.index(mock_to_num_dict[it+'1']))
        pts[it.lower()+'2'] = pts['mockComboMax'].apply(lambda x: x.index(mock_to_num_dict[it+'2']))
    dropCols.extend(['mockComboMax'])
    cols            = []
    x               = [cols.extend([ABC[n].lower()+'1']) for n in range(0,max_delivery_per_dg)]

    # sortKey ONLY describes location of pick-up point
    pts['sortKey']      = pts[cols].apply(lambda s: [pd_combine(*s)],axis=1).ix[:,0]
    pts['sortKey']      = pts['sortKey'].map(lambda s: eval(s)).map(pd_create_sortKey)
    for i in range(0,max_delivery_per_dg):
        pts['i'+str(i)] = pts['sortKey'].map(lambda s: s[i])
    dropCols.append('sortKey')
    pts                 = pts.drop(dropCols,axis=1)
    ptPairSet           = make_initial_ptPairSet_store()
    pts                 = add_ptPair_info_to_orderSet(pts,ptPairSet=False,save_to_hdf=True)
    ptPairSet           = set_ptPair_order(pts,ptPairSet)
    pts                 = add_ptPair_info_to_orderSet(pts,ptPairSet,save_to_hdf=True)

    pts.to_hdf(this_cwd+'/perm_data/store_orderSet.h5','table',append=False)

    if test==True:
        """
        Since permutations for 5 orders includes permutations for 2 orders (with extra cols),
        a count of all pts should be equal to the number of permutations for the max_deliv_per_dg (currently 5).

        In this case, files 5-0 through 5-22 were created (23 files), and the total number of lines should equal
        number of permutations for 5 orders.

        If true, the generated text files will be deleted (by hand).
        """
        base_f = this_cwd+'/perm_data/OrderedPairPerm-'
        z=['5-'+str(it) for it in range(0,23)]
        y=[]
        for it in z:
            f=open(base_f+it+'.txt','r')
            y.extend(f.readlines())
        print len(y),' = ',len(pts)

def make_pairSet_store():
    dictPairs   = pd.DataFrame(genAllPairPerm_NoRep(max_delivery_per_dg,2),columns=['a','b'])
    for it in ['a','b']:
        dictPairs[it]   = dictPairs[it].map(mock_to_num_dict)
    dictPairs['mc'+str(max_delivery_per_dg)] = dictPairs.a.map(lambda s: True)

    for i in np.arange(max_delivery_per_dg-1,1,-1):
        pairsTemp           = pd.DataFrame(np.array(genAllPairPerm_NoRep(i,2)),columns=['a','b'])
        for it in ['a','b']:
            pairsTemp[it]   = pairsTemp[it].map(mock_to_num_dict)
        pairsTemp['mc']     = pairsTemp.apply(lambda x: str(pd_combine(*x)), axis=1)
        dictPairs['temp']   = dictPairs[['a','b']].apply(lambda x: str(pd_combine(*x)), axis=1)
        dictPairs['mc'+str(i)] = dictPairs.temp.where(dictPairs.temp.isin(pairsTemp.mc)
                                                    ).map(lambda s: True if type(s) == str else False)
        # a=dictPairs.where(dictPairs.temp.isin(pairsTemp.mc)).apply(lambda s: [pd_combine(*x)] if type(s) == list else False)
        # dictPairs['mc'+str(i)]=dictPairs['mc'+str(i)].map(lambda s: True if s == True else False)

    dictPairs   = dictPairs.drop('temp',axis=1)
    dictPairs.to_hdf(this_cwd+'/perm_data/store_pairSet.h5','table',append=False)

def make_ptPairSet_store(with_existing_hdfs=False):
    ptPairSet_path  = this_cwd+'/perm_data/store_ptPairSet.h5'
    pts_path        = this_cwd+'/perm_data/store_orderSet.h5'
    if with_existing_hdfs:
        ptPairSet           = pd.read_hdf(ptPairSet_path,'table')
        pts                 = pd.read_hdf(pts_path,'table')
    else:
        if isfile(ptPairSet_path):
            os_remove(ptPairSet_path)
        ptPairSet           = make_initial_ptPairSet_store()
        pts                 = add_ptPair_info_to_orderSet(pts=False,ptPairSet=ptPairSet,save_to_hdf=True)
        ptPairSet           = set_ptPair_order(pts,ptPairSet,save_to_hdf=True)
    add_ptPair_info_to_orderSet(pts,ptPairSet,save_to_hdf=True)

if __name__ == '__main__':
    # from sys import argv
    try:
        cmd  = []
        for i in range(0, len(argv)): cmd.append(argv[i])
            # cmd[0] == current working directory
            # cmd[1] == function to apply
            # cmd[2] == variable for the function
        stop = False
    except:
        cmd  = []
        stop = True
    if len(cmd)==1: stop = False
    if stop == False:
        if   cmd[1] == 'make_orderSet':         make_orderSet_store()
        elif cmd[1] == 'make_pairSet':          make_pairSet_store()
        elif cmd[1] == 'make_ptPairSet':        make_ptPairSet_store()
        elif cmd[1] == 'redo_ptPairSet':        make_ptPairSet_store(with_existing_hdfs=True)
