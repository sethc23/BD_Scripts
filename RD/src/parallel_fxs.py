# Parallel Processing f(x)s
def run_parallel(testSet,get_delivery_combo,get_combo_vars):
    ppservers=()
    #ppservers = ("192.168.5.2",)
    num_processes=2
    job_server = pp.Server(ppservers=ppservers)
    #print job_server.get_ncpus()
    jobs=[]
    for i in range(0,num_processes):
        runSet=testSet.iloc[(len(testSet.index)*i)/num_processes:(len(testSet.index)*(i+1))/num_processes,:].reset_index(drop=True)
        jobs.append(job_server.submit(get_delivery_combo,(runSet,get_combo_vars,True), (Assumption,), ('pd','np','get_delivery_combo',)))
    #print job_server.print_stats()
    results,travel_times,start,pt=[],[],False,0
    for job in jobs:
        res = job()
        #print res
        if type(res) != NoneType:
            results.append(res)
            travel_times.append(sum(res.travel_time.tolist()))
    if len(travel_times)!=0:
        print 'why return:\n'
        print results[travel_times.index(min(travel_times))]
        systemError()
    return results[travel_times.index(min(travel_times))]
