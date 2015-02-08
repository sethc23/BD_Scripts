def cleanStatute(x):
    q = []
    s_var = '\r\n-'
    e_var = '-'
    pt = x.find(s_var)
    keep = ['CITE', 'EXPCITE', 'HEAD', 'STATUTE']
    del_s_var = 0
    for i in range(0, x.count(s_var)):
        n_pt = x.find(s_var, pt) + len(s_var)
        e_pt = x.find(e_var, n_pt)
        pt = e_pt
        n_var = x[n_pt:e_pt]
        if keep.count(n_var) == 0:
            if del_s_var == 0:
                del_s_var = n_pt
        else:
            if del_s_var != 0:
                del_e_var = n_pt
                # print x[del_s_var:del_e_var]
                # x=x[:del_s_var]+x[del_e_var:]
                del_s_var = 0
                # break
    return x

def getHeaders(x):
    q = []
    s_var = '\r\n-'
    e_var = '-'
    pt = x.find(s_var)
    keep = ['CITE', 'EXPCITE', 'HEAD', 'STATUTE']
    del_s_var = 0
    for i in range(0, x.count(s_var)):
        n_pt = x.find(s_var, pt) + len(s_var)
        e_pt = x.find(e_var, n_pt)
        pt = e_pt
        n_var = x[n_pt:e_pt]
        if n_var == 'HEAD':
            if del_s_var == 0:
                del_s_var = x.find('    ', n_pt) + len('    ')
        else:
            if del_s_var != 0:
                del_e_var = x[:n_pt].rfind('\r') - 2
                
                q.append(x[del_s_var:del_e_var])
                # print x[del_s_var:del_e_var]
                # x=x[:del_s_var]+x[del_e_var:]
                del_s_var = 0
                # break

    for i in range(0, len(q)):
        print q[i]




f = open('/Users/admin/Desktop/Title_15.txt', 'r')
x = f.read()
f.close()

cleanStatute(x)
getHeaders(x)

# '''
f = open('/Users/admin/Desktop/Title_15_clean.txt', 'w')
f.write(x)
f.close()
# '''
