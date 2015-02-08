
def mnt_shares(SYS,folders=[''],local=True):
    t       =   SYS.mnt_shares(folders)
    return True
def umnt_shares(SYS,folders=['all'],local=True):
    t       =   SYS.umnt_shares(folders)
    return True

from sys import argv
if __name__ == '__main__':
    from System_Control import System_Servers
    SYS             =   System_Servers()
    if   len(argv)  == 1        :               mnt_shares(SYS)
    elif argv[1]    == 'mnt_all':               mnt_shares(SYS)
    elif argv[1]    == 'umnt_all':              umnt_shares(SYS)
    else:                                       mnt_shares(SYS,[argv[1]])


