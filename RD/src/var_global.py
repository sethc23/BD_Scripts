from rd_lib import pd,np,this_cwd,isfile
import assumptions as A

global ABC
ABC='ABCDEFGHIJKLMNOPQRUSTUVXYZ'

global mock_to_num_dict,num_to_mock_dict
max_delivery_per_dg = A.max_delivery_per_dg
## create dict for total number of possible mock points, e.g., A1:A2,B1:B2,etc...
mock_to_num_dict=dict(zip([it+'1' for it in ABC[:max_delivery_per_dg]],np.arange(0,(len(ABC)+1),1).astype(np.intc)))
mock_to_num_dict.update(dict(zip([it+'2' for it in ABC[:max_delivery_per_dg]],np.arange(100,100*(len(ABC)+1),1).astype(np.intc))))
num_to_mock_dict = {v:k for k,v in mock_to_num_dict.iteritems()}

global ind_to_mock_dict,mock_to_ind_dict
a=[]
w=[a.extend([it+'1',it+'2']) for it in ABC[:max_delivery_per_dg]]
## create maps to quickly interchange between attributes
ind_to_mock_dict = dict(zip(range(0,len(a)),a))
mock_to_ind_dict = {v:k for k,v in ind_to_mock_dict.iteritems()}

global ind_to_num_dict,num_to_ind_dict
w=[mock_to_num_dict[it] for it in a]
ind_to_num_dict = dict(zip(range(0,max_delivery_per_dg*2),w))
num_to_ind_dict = {v:k for k,v in ind_to_num_dict.iteritems()}

# MAKE AND GET COMBINATION DATA #
# gen_good_perms(5,6)
# make_pairSet_store()
# make_orderSet_store()

# TRANSACTIONAL INDICIES

orderSet_path               = this_cwd+'perm_data/store_orderSet.h5'
pairSet_path                = this_cwd+'perm_data/store_pairSet.h5'
ptPairSet_path              = this_cwd+'perm_data/store_ptPairSet.h5'
global orderSet,pairSet,ptPairSet

if isfile(orderSet_path):   orderSet = pd.read_hdf(orderSet_path, 'table')
else:
    from var_gen import make_orderSet_store
    make_orderSet_store()
    orderSet                = pd.read_hdf(orderSet_path, 'table')

if isfile(pairSet_path):    pairSet = pd.read_hdf(pairSet_path, 'table')
else:
    from var_gen import make_pairSet_store
    make_pairSet_store()
    pairSet                 = pd.read_hdf(pairSet_path, 'table')

if isfile(ptPairSet_path):  ptPairSet,new_ptPairSet = pd.read_hdf(ptPairSet_path, 'table'),False
else:
    from var_gen import make_ptPairSet_store
    make_ptPairSet_store()
    ptPairSet               = pd.read_hdf(ptPairSet_path, 'table')
    new_ptPairSet           = True

# MAKE AND GET TRANSACTIONAL ARRAYS

global c_orderSet,c_realCombos
r = len(orderSet.index)
d = max_delivery_per_dg
c_realCombos = np.empty((r,d*2),dtype=np.float_,order='C')
ordSortCols = ['mc2','mc3','mc4','mc5']
orderSet = orderSet.sort_index(by=ordSortCols,ascending=[True,True,True,True])
c_orderSet = np.ascontiguousarray(orderSet.astype(np.intc).as_matrix(),dtype=np.intc)

global c_mc_ranges,c_orderSK_range,c_pointSK_range
global c_ptPairSet,c_tmp_minutes
global c_orderSet2,c_orderSet3,c_orderSet4,c_orderSet5,c_orderSetInd
ordCols = orderSet.columns.tolist()
orderSetInd = []
mc_ranges,orderSK_range,pointSK_range,points_range = [],[],[],[]
mc_start    = ordCols.index('pt0')
ord_start   = ordCols.index('i0')
pt_start    = ordCols.index('a1')
seg_start   = ordCols.index('pp_0')

seg_e_pt=seg_start+3                                # first iteration considers extra column pair
pair_s_pt=0
sortCol,sort_asc=[],[]

for i in range(2,max_delivery_per_dg+1):
    i_col           = 'mc'+str(i)
    pair_e_pt       = len(ptPairSet[ptPairSet[i_col]==True])
    rowPts          = []
    rowPts.append(mc_start)                         # mock_point as pt #1
    rowPts.append(mc_start+(2*i))
    rowPts.append(ord_start)                        # index for order #.s, i.e., A,B,C, etc...
    rowPts.append(ordCols.index('i'+str(i-1))+1)
    rowPts.append(pt_start)                         # index for pt #1
    rowPts.append(pt_start+(2*i))
    rowPts.append(seg_start)                        # index for route segment
    rowPts.append(seg_start+(2*i)-1)
    rowPts.append(0)                                # index for ptPairSet
    rowPts.append(pair_e_pt)
    # orderSetInd provides column parameters
    orderSetInd.append(rowPts)
    indList         = np.array(orderSet[orderSet[i_col]==True].index.astype(np.intc),dtype=np.intc)
    # mc_ranges (mock_combo_ranges) provides row parameters
    mc_ranges.append(indList)

c_ptPairSet     = np.ascontiguousarray(ptPairSet.pair_idx.tolist(),dtype=np.intc)
c_tmp_minutes   = np.ascontiguousarray(np.empty((c_ptPairSet.shape[0],), dtype=np.float_,order='C'), dtype=np.float_)
c_orderSet2     = np.ascontiguousarray(orderSet.ix[mc_ranges[0],:].astype(np.intc).as_matrix(),dtype=np.intc)
c_orderSet3     = np.ascontiguousarray(orderSet.ix[mc_ranges[1],:].astype(np.intc).as_matrix(),dtype=np.intc)
c_orderSet4     = np.ascontiguousarray(orderSet.ix[mc_ranges[2],:].astype(np.intc).as_matrix(),dtype=np.intc)
c_orderSet5     = np.ascontiguousarray(orderSet.ix[mc_ranges[3],:].astype(np.intc).as_matrix(),dtype=np.intc)
c_orderSetInd   = np.ascontiguousarray(orderSetInd,dtype=np.intc)

global c_MPH,c_max_delivery_time,c_mttlt,c_max_delivery_per_dg
c_MPH = A.MPH
float_vars = np.asarray([A.max_delivery_time,A.max_travelToLocTime],dtype=np.float_)
c_max_delivery_per_dg = np.intc(max_delivery_per_dg)
c_max_delivery_time,c_mttlt = float_vars[0],float_vars[1]

global c_tripPoints,c_deliv_ids,c_order_times,c_rv_comboStartInfo,c_rv_bestCombo,c_bestDG
c_tripPoints = np.ascontiguousarray(np.empty((d*2,), dtype=np.float_,order='C'), dtype=np.float_)
c_deliv_ids = np.ascontiguousarray(np.empty((d,), dtype=np.float_,order='C'), dtype=np.float_)
c_order_times = np.ascontiguousarray(np.empty((d,), dtype=np.float_,order='C'), dtype=np.float_)
c_rv_comboStartInfo = np.ascontiguousarray(np.zeros((d,12), dtype=np.float_,order='C'), dtype=np.float_)
c_rv_bestCombo = np.ascontiguousarray(np.zeros((d,12), dtype=np.float_,order='C'), dtype=np.float_)
c_bestDG = np.ascontiguousarray(np.empty((d,12), dtype=np.float_, order='C'), dtype=np.float_)

global c_travel_times,c_start_times,c_end_times,c_odtTimes,c_oMaxTimes,c_tMaxTimes,c_tddTimes,c_ctMarker,c_rv_updatedBestCombo,c_returnVars
c_travel_times = np.ascontiguousarray(np.empty((r,d*2), dtype=np.float_,order='C'))
c_start_times = np.ascontiguousarray(np.empty((r,d), dtype=np.float_,order='C'))
c_end_times = np.ascontiguousarray(np.empty((r,d), dtype=np.float_,order='C'))
c_odtTimes = np.ascontiguousarray(np.empty((r,d), dtype=np.float_,order='C'))
c_tddTimes = np.ascontiguousarray(np.empty((r,d), dtype=np.float_,order='C'))
c_oMaxTimes = np.ascontiguousarray(np.zeros(r, dtype=np.float_,order='C'))
c_tMaxTimes = np.ascontiguousarray(np.zeros(r, dtype=np.float_,order='C'))
c_ctMarker = np.ascontiguousarray(np.zeros(r, dtype=np.float_,order='C'))
c_rv_updatedBestCombo = np.ascontiguousarray(np.empty((d,12), dtype=np.float_,order='C'))
c_returnVars = np.ascontiguousarray(np.empty((d,12), dtype=np.float_,order='C'))
