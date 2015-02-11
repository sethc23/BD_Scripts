# Data Recordation
from rd_lib import this_cwd

def export_all_data(globalVars,program_stats=False):
    order_q,order_delivered,dg_q,dg_delivered,dg_pool,dg_pool_pt = globalVars

    pd_EDA_order_q_Path=this_cwd+'/sim_data/EDA_order_q_data.txt'
    order_q=order_q.sort_index(by=['dg_id','order_time'], ascending=[True,True])
    order_q.to_csv(pd_EDA_order_q_Path, index=False, header=True, sep='\t')

    pd_EDA_dg_q_Path=this_cwd+'/sim_data/EDA_dg_q_data.txt'
    dg_q=dg_q.sort_index(by='dg_id', ascending=True)
    dg_q.to_csv(pd_EDA_dg_q_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_dg_pool.txt'
    dg_pool=dg_pool.sort_index(by=['dg_id'], ascending=[True])
    dg_pool.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_order_delivered.txt'
    order_delivered=order_delivered.sort_index(by=['dg_id','order_time'], ascending=[True,True])
    order_delivered.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    pd_EDA_data_Path=this_cwd+'/sim_data/EDA_dg_delivered.txt'
    dg_delivered=dg_delivered.sort_index(by=['dg_id'], ascending=[True])
    dg_delivered.to_csv(pd_EDA_data_Path, index=False, header=True, sep='\t')

    if type(program_stats) != bool:
        program_stats.to_csv(this_cwd+'/sim_data/program_stats.txt', index=False, header=True, sep='\t')
    print 'data exported'
    return True
