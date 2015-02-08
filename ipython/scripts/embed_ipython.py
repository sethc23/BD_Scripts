from sys import path as py_path
py_path.append('/home/ub2/SERVER2/BD_Scripts/ipython/ipython')
from IPython import embed_kernel as embed
#from ipdb import set_trace as i_trace


# Usage:  import embed_ipython as I; I.embed()


# Starts a new instance .... 
# To run QT from on the current workstation:
# import IPython as IP; IP.start_ipython(argv=["qtconsole","--profile=nbserver"]);
argv=["--profile=nbserver"]

