import numpy as np
import os

def aList(c):
    return list(c)

def copyList(orig_list):
    c=[x for x in orig_list]
    d=[str(type(it)) for it in orig_list]
    if len(c) == (d.count("<type 'str'>") + d.count("<type 'int'>")): return list(c)
    elif isinstance(c, list):
        for topsublist in [c]:
            for i, L in enumerate(topsublist):
                topsublist[i] = list(L)
        return c 
    return ""

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
                    row_vars.append(eval(row))
                except:
                    row_vars.append(row)
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

def arrayFin(F_in,delimiter="\t"):
    #return np.loadtxt(F_in)
    return np.genfromtxt(F_in, delimiter="\t",autostrip=True) 
#     nameF = str(F_in)
#     nameS = nameF.replace(".txt", '')
#     batchFiles = []
#     dirContents = []
#     workingDir = os.getcwd()
#     dirContents = os.listdir(workingDir)
#     for i, item in enumerate(dirContents):
#         if nameS in item:
#             batchFiles.append(dirContents[i])
#     loop = len(batchFiles)
#     batchFiles.sort()
#     print 'files to process :'
#     print batchFiles
#     A_out = np.array([])
#     length = len(listFin(batchFiles[0]))
#     A_out.resize(loop, length)
#     for t in range(0, loop):
#         fileF = str(batchFiles[t])
#         fileS = fileF.rstrip(nameF)
#         fileS = fileS.lstrip(nameS)
#         listData = listFin(batchFiles[t])
#         rows = len(listData)
#         A_out[t] = listData
#     return A_out

def arrayFout(A_in, F_out):
    try:
        np.savetxt(F_out,A_in)
    except:
        np.savetxt(F_out, A_in, delimiter="\t", fmt="%s") 
#     col = np.shape(A_in)[0]
#     row = np.shape(A_in)[1]    
#     nameF = str(F_out)
#     nameS = nameF.rstrip('.txt')
#     for column in range(0, col):
#         name = nameS
#         name = name + str(column) + '.txt'
#         cutArray = A_in[column].tolist()
#         listFout(cutArray, name)

"""
np.reshape(a, (3,-1))  # the unspecified value is inferred to be 2


 # Get the integer indices of the rows that sum up to 3
 # and the columns that sum up to 3.
 bad_rows = np.nonzero(M.sum(axis=1) == 3)
 bad_cols = np.nonzero(M.sum(axis=0) == 3)

 # Now use the numpy.delete() function to get the matrix
 # with those rows and columns removed from the original matrix.
 P = np.delete(M, bad_rows, axis=0)
 P = np.delete(P, bad_cols, axis=1)
"""

def randomNum(start_num,end_num,float_num=False):
    from random import randint,random
    if float_num == False: 
        if type(start_num) == float:
            a=str(start_num)
            b=a.find('.')
            c=len(a)-1
            start_num=int(start_num*c*10)
            end_num=int(end_num*c*10)
            x=randint(start_num,end_num)
            x=x/(c*10.0)
            return x
        else: return randint(start_num,end_num)
    else: return random()