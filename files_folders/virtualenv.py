import os
# def add_paths_to_virtualenv():
def getFilesFolders(workDir, full=False):
    x = os.listdir(workDir)
    try: a = x.pop(x.index('.DS_Store'))
    except: pass
    popList, y = [], []
    for i in range(0, len(x)):
        if os.path.isdir(x[i]):
            popList.append(i)
        else: y.append(workDir.rstrip('/')+'/'+x[i])
    popList.reverse()
    for it in popList: x.pop(it)
    if full == False: return x
    else:
        return y
workDir='/opt/local/Library/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages/'
envDir='/Users/admin/SERVER2/BD_Scripts/RD/ENV/lib/python2.7/site-packages/'
x = getFilesFolders(workDir, full=True)
for it in x:
    cmd='ln -s '+it+' '+envDir+it[it.rfind('/')+1:]
    os.system(cmd)
