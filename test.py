

import pyximport
pyximport.install(build_in_temp=False,inplace=True)
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import numpy as np
from test1 import c_test,c_test_result_workaround

a =  np.ascontiguousarray(np.array([ [1,2,3],[1,2,3],[1,2,3] ], dtype=np.long), dtype=np.long)
print '\nStart Value:\n',a

a_transposed = a.T
ai = a_transposed[0]
i = ai[0]
j = ai[1]
k = ai[2]
print '\nExpected Value:\n',[i,j,k]

b =  np.ascontiguousarray(np.empty((3,), dtype=np.long,order='C'))
x = c_test(a,b)
print '\nProblem Result:\n',np.asarray(x)


y = c_test_result_workaround(a,b)
print '\nWork-Around Result:\n',np.asarray(y)