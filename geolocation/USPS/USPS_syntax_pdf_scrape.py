

from os                             import environ          as os_environ
from os                             import path             as os_path
from sys                            import path             as py_path
from bs4                            import BeautifulSoup    as soup
import                                  pandas              as pd
pd.set_option(                          'display.max_rows', 1000)
from re                             import findall          as re_findall
from subprocess                     import Popen            as sub_popen
from subprocess                     import PIPE             as sub_PIPE



def extract_pdf_contents_from_stdout(fpath_pdf):
    cmd                                 =   'pdftohtml -i -stdout -xml %s' % fpath_pdf
    p                                   =   sub_popen(cmd,stdout=sub_PIPE,shell=True)
    (_out,_err)                         =   p.communicate()
    assert _err==None
    return _out

def extract_pdf_contents_as_xml(fpath_pdf,fpath_xml):
    cmd                                 =   'pdftohtml -i -stdout -xml %s %s' % (fpath_pdf,fpath_xml)
    p                                   =   sub_popen(cmd,stdout=sub_PIPE,shell=True)
    (_out,_err)                         =   p.communicate()
    assert _err==None
    return _out

def make_dataframe_with_contents(_file_contents):
    html                                =   soup(t)
    pages                               =   html.findAll('page')
    d = []
    for pg in pages:
        idx                             =   pages.index(pg)
        pg                              =   str(pg)

        for it in pg.split('\n')[1:-1]:
            line_var_names              =   re_findall(r'([a-zA-Z]+)+\=',it)
            line_var_vals               =   re_findall(r'[a-zA-Z]+\=\"(.*?)\"',it)
            line_text                   =   re_findall(r'<text.*?>(.*?)</text>',it)

            a                           =   ['page_num'] + line_var_names + ['text']
            b                           =   [idx] + line_var_vals + line_text
            d.append(                       dict(zip(a,b)))
    g                                   =   pd.DataFrame(d)
    return g

def street_abbrs_checks(A):
    print 'add rows to adjust for cases where prim_suff was not included as common_use'
    a = A.prim_suff.unique().tolist()
    b = A.common_use.unique().tolist()
    z = pd.DataFrame({'all_u':a})
    z['cnt'] = z.all_u.map(lambda s: b.count(s))
    z['common_use'] = a
    suff_idx_map = dict(zip(A.prim_suff.tolist(),A.index.tolist()))
    z['usps_abbr'] = z.all_u.map(lambda s: A.ix[suff_idx_map[s],'usps_abbr'])
    z = z[z.cnt==0].drop(['cnt'],axis=1).rename(columns={'all_u':'prim_suff'})
    print len(z),'rows added'
    print '\n',z,'\n'
    A = A.append(z,ignore_index=True).sort('prim_suff').reset_index(drop=True)


    print len(A),'before haircut, e.g., remove nulls, dupes'
    erroneous = A[(A.prim_suff.isnull()==True)|
      (A.common_use.isnull()==True)|
      (A.usps_abbr.isnull()==True)].reset_index(drop=True)
    print '\nErroneous Rows:\n\n',erroneous
    err_idx = erroneous.index.tolist()
    A = A[A.index.isin(err_idx)==False]
    print len(A),'after erroneous'
    A['dupes'] = A.apply(lambda s: s[1]==s[2],axis=1)
    dupe_idx = A[A.dupes==True].index.tolist()
    prim_suff_list = A.prim_suff.tolist()
    A['cnt'] = A.prim_suff.map(lambda s: prim_suff_list.count(s))
    print '\n',A[(A.index.isin(dupe_idx)==True)].sort('cnt'),'\n'
    A = A[A.index.isin(dupe_idx)==False].reset_index(drop=True)
    print len(A),'after dupes'

def get_street_abbrs(g):
    pgs_grp                                 =   g.groupby('page_num')
    cols                                    =   ['prim_suff','common_use','usps_abbr']
    A                                       =   pd.DataFrame(columns=cols)
    for k in range(0,len(pages)):

        pg = g.ix[pgs_grp.indices[k],:]

        top_list = pg.top.tolist()
        left_list = pg.left.tolist()
        pg['top_cnt'] = pg.top.map(lambda s: top_list.count(s))
        pg['left_cnt'] = pg.left.map(lambda s: left_list.count(s))
        pg['is_alpha'] = pg.text.map(lambda s: str(s).isalpha())
        pg = pg[pg.is_alpha==True]
        pg['all_caps'] = pg.text.map(lambda s: s.isupper())
        tops = pg[pg.top_cnt==3]

        a=tops.groupby('top')
        z=(a.idxmax()-a.idxmin()).left
        top_rows = z[z==2].keys().tolist()
        first_row = pg[pg.top==top_rows[0]].index.min()
        pg = pg.ix[first_row:,:]
        last_row = pg[pg.all_caps==True].index.max()
        pg = pg.ix[:last_row,:].reset_index(drop=True)
        pg['top_st'] = pg.top.map(lambda s: True if top_rows.count(s)!=0 else False)

        a = pg[(pg.top_cnt==3)&(pg.top_st==True)].groupby('top')
        b = pd.np.array(a.groups.values()).T
        prim_suff_idx = sorted(b[0].tolist())
        primary_suffixes = pg.ix[prim_suff_idx,'text']
        usps_abbr = pg.ix[sorted(b[2].tolist()),'text']
        usps_abbr_idx = usps_abbr.index.tolist()

        d = []
        for i in range(0,len(prim_suff_idx)-1):
            this_set = range(prim_suff_idx[i]+1,prim_suff_idx[i+1])
            dump = this_set.pop(1)
            for c in this_set:
                d.append(dict(zip(cols,[prim_suff_idx[i],c,usps_abbr_idx[i]])))

            if i==len(prim_suff_idx)-2:
                a = range(prim_suff_idx[i+1],pg.index.max()+1)
                this_set = [a[1]]+a[3:]
                for c in this_set:
                    d.append(dict(zip(cols,[prim_suff_idx[i+1],c,usps_abbr_idx[i+1]])))

        df = pd.DataFrame(d)
        df = df.ix[:,['prim_suff','common_use','usps_abbr']]
        df['prim_suff'] = pg.ix[df.prim_suff,'text'].tolist()
        df['common_use'] = pg.ix[df.common_use,'text'].tolist()
        df['usps_abbr'] = pg.ix[df.usps_abbr,'text'].tolist()
    #     print pg.ix[this_set,:].drop(['is_alpha','all_caps','width','font','height','page_num'],axis=1)
    #     print A.append(df,ignore_index=True)
    #     z=raw_input('hit enter...')
    #     if z==0:
    #         pdb.set_trace()
        A = A.append(df,ignore_index=True)

    print 'add rows to adjust for cases where prim_suff was not included as common_use'
    a = A.prim_suff.unique().tolist()
    b = A.common_use.unique().tolist()
    z = pd.DataFrame({'all_u':a})
    z['cnt'] = z.all_u.map(lambda s: b.count(s))
    z['common_use'] = a
    suff_idx_map = dict(zip(A.prim_suff.tolist(),A.index.tolist()))
    z['usps_abbr'] = z.all_u.map(lambda s: A.ix[suff_idx_map[s],'usps_abbr'])
    z = z[z.cnt==0].drop(['cnt'],axis=1).rename(columns={'all_u':'prim_suff'})
    print len(z),'rows added'
    print '\n',z,'\n'
    A = A.append(z,ignore_index=True).sort('prim_suff').reset_index(drop=True)


    print len(A),'before haircut, e.g., remove nulls, dupes'
    erroneous = A[(A.prim_suff.isnull()==True)|
      (A.common_use.isnull()==True)|
      (A.usps_abbr.isnull()==True)].reset_index(drop=True)
    print '\nErroneous Rows:\n\n',erroneous
    err_idx = erroneous.index.tolist()
    A = A[A.index.isin(err_idx)==False]
    print len(A),'after erroneous'
    A['dupes'] = A.apply(lambda s: s[1]==s[2],axis=1)
    dupe_idx = A[A.dupes==True].index.tolist()
    prim_suff_list = A.prim_suff.tolist()
    A['cnt'] = A.prim_suff.map(lambda s: prim_suff_list.count(s))
    print '\n',A[(A.index.isin(dupe_idx)==True)].sort('cnt'),'\n'
    A = A[A.index.isin(dupe_idx)==False].reset_index(drop=True)
    print len(A),'after dupes'

    street_abbrs_checks(A)

    print '\n','Save Path:\n\n\t\t',save_csv_path,'\n'
    z=raw_input('type "y" to confirm save...')
    if z=='y':
        A.to_csv(save_csv_path)


def parse_USPS_sytax_pdf(content_type='street_abbr'):
    assert ['street_abbr','business_abbr'].count(content_type)>0
    columns_on_page                     =   3 if content_type=='street_abbr' else 2

def get_business_abbr(g):

    g = g.drop(['color','family','id','size'],axis=1)

    g = g[g.font.isnull()==False].copy()
    g['font'] = g.font.map(int)

    g['height'] = g.height.map(int)
    g['left'] = g.left.map(int)
    g['page_num'] = g.page_num.map(int)
    g['top'] = g.top.map(int)
    g['width'] = g.width.map(int)

    pgs_grp = g.groupby('page_num')

    # cols = ['prim_suff','common_use','usps_abbr']
    cols = ['common_use','usps_abbr']
    col_cnt=len(cols)
    A = pd.DataFrame(columns=cols)
    for k in range(len(pages)):

        pg = g.ix[pgs_grp.indices[k],:]

        # Sort to Stay Consistent
        pg = pg.sort(['top','left'],ascending=[True,False]).reset_index(drop=True)

        # Categorized Content
        top_list = pg.top.tolist()
        left_list = pg.left.tolist()
        pg['top_cnt'] = pg.top.map(lambda s: top_list.count(s))
        pg['left_cnt'] = pg.left.map(lambda s: left_list.count(s))
        pg['is_upper'] = pg.text.map(lambda s: True if ['&','&&'].count(s)!=0 else
                                     True if (str(s)[0].isdigit()
                                              and str(s)[-1:].isalpha())
                                     else str(s).isupper())
        left_max = int(pg[pg.is_upper==True].left.max())
        left_min = int(pg[ pg.is_upper==True ].left.min())
        pg = pg[ (left_min<= pg.left) & (pg.left<=left_max) ].copy()

        pg = pg[ pg.text.map(lambda s: True if (['&amp;','&amp;&amp;'].count(s)>0
                                                or (str(s)[0].isdigit() and str(s)[-1:].isalpha()) )
                                                 else str(s).isupper()) ].copy()

        pg = pg[ pg.text.map(lambda s: True if (['&amp;','&amp;&amp;'].count(s)>0
                                                or (str(s)[0].isdigit() and str(s)[-1:].isalpha()) )
                                                 else str(s).isalpha()) ].copy()

        tops = pg[pg.left==left_max]

        a=tops.groupby('top')
        z=(a.idxmax()-a.idxmin()).left

        # boxing in the important stuff
        top_rows = z.keys().tolist()
        first_row = pg[pg.top==top_rows[0]].index.min()
        pg = pg.ix[first_row:,:]
        last_row = pg[pg.is_upper==True].index.max()
        pg = pg.ix[:last_row,:].reset_index(drop=True)
        pg['top_st'] = pg.top.map(lambda s: True if top_rows.count(s)!=0 else False)

        # Normalize the 'top' variable
        pg = pg.sort('top',ascending='True').reset_index(drop=True)
        all_tops = sorted(pg.top.tolist())
        pg['top-diff']=pg.index.map(lambda s: 0 if s==0 else all_tops[s]-all_tops[s-1])
        pg['top'] = pg[['top','height','top-diff']].apply(lambda s: s[0] if (s[2]==0
                                                                             or s[2]>=s[1])
                                                            else s[0]-s[2],axis=1)
        all_tops = sorted(pg.top.tolist())
        pg['top-diff']=pg.index.map(lambda s: 0 if s==0 else all_tops[s]-all_tops[s-1])
        top_diff_std_dev = pg[pg['top-diff'].isin([0])==False]['top-diff'].std()
        skip_pages = [13,45,57]
        # Should this apply only to non-abbr rows?
        if skip_pages.count(k)==0:
            assert top_diff_std_dev<5

        # Sort Again
        pg = pg.sort(['top','left'],ascending=[True,False]).reset_index(drop=True)

        # Categorize Parts Affected Again
        top_list = pg.top.tolist()
        pg['top_cnt'] = pg.top.map(lambda s: top_list.count(s))

        a=tops.groupby('top')
        z=(a.idxmax()-a.idxmin()).left

        # Re-box
        top_rows = z.keys().tolist()
        first_row = pg[pg.top==top_rows[0]].index.min()
        pg = pg.ix[first_row:,:]
        last_row = pg[pg.is_upper==True].index.max()
        pg = pg.ix[:last_row,:].reset_index(drop=True)
        pg['top_st'] = pg.top.map(lambda s: True if top_rows.count(s)!=0 else False)

        # Split up values as among top_cnt and top_st
        a = pg[(pg.top_cnt==2)&(pg.top_st==True)].groupby('top')
        b = pd.np.array(a.groups.values()).T

        # Pull indicies
        usps_abbr_rows = pg.ix[sorted(b[0].tolist()),'text']
        usps_abbr_rows_idx = usps_abbr_rows.index.tolist()

        leftover_index = sorted(pg[pg.index.isin(usps_abbr_rows_idx)==False].index.tolist())
        common_use_top_rows = pg.ix[sorted(b[1].tolist()),'text']
        common_use_top_rows_idx = common_use_top_rows.index.tolist()

        # Map the indicies to abbr values
        use_idx_abbr_D = dict(zip(common_use_top_rows_idx,usps_abbr_rows))
        D = dict(zip(leftover_index,range(len(leftover_index))))
        for k,v in D.iteritems():
            if common_use_top_rows_idx.count(k):
                new_abbr = use_idx_abbr_D[k]
            elif usps_abbr_rows_idx.count(k):
                raise SystemError
            D[k] = new_abbr

        df = pd.DataFrame({'common_use':pg[pg.index.isin(leftover_index)].ix[:,'text'],
                           'usps_abbr':map(lambda s: D[s],leftover_index)})

        A = A.append(df,ignore_index=True)
    return A

def generate_regex_from_parsed_data(A,common_use_col='common_use',abbrev_col='usps_abbr'):
    """

    Also, common_use_col = 'prim_suff'

    """

    g                                       =   A.groupby(common_use_col)
    df                                      =   pd.DataFrame({common_use_col:g.groups.keys()}
                                                      ).sort(common_use_col).reset_index(drop=True)

    use_abbr_map                            =   dict(zip(A[common_use_col].tolist(),A[abbrev_col].tolist()))
    df['usps_abbr']                         =   df[common_use_col].map(use_abbr_map)

    f                                       =   lambda s: str(g.get_group(s).common_use.map(
                                                lambda s: s.lower()).tolist()
                                                ).strip(' ').replace(', ',' | ').replace("'",'').strip('[]')
    df['pattern']                           =   df[common_use_col].map(f)
    df['combined']                          =   df.ix[:,['pattern','usps_abbr']].apply(
                                                    lambda s: (s[0],s[1].lower()),axis=1)
    usps_repl_list                          =   df.combined.tolist()
    return df,usps_repl_list


    # def one(fpath,the_list):
    #     with open(fpath,'w') as f:
    #         for item in the_list:
    #             print f, item
    #
    # def two(fpath,the_list):
    #     f                                   =   open(fpath,'w')
    #     for item in the_list:
    #         f.write(                            "%s\n" % item)
    #     f.close(                                )
    #
    # def three(fpath,the_list):
    #     f                                   =   open(fpath,'w')
    #     f.write(                                '%s\n' % json.dumps(Pickle.dumps(the_list)))
    #     f.close(                                )
    #
    # def four():
    #     import pickle
    #     pickle.dump(                                itemlist, outfile)
    #
    # print len(                                  df)
    # print df
    # z                                       =   raw_input('type "y" to confirm save...')
    # if z=='y':
    #     fpath                               = save_csv_path.replace('.csv','_1_regex.txt')
    #     %timeit one(fpath,usps_repl_list)
    #     %timeit range(1000)
    #     fpath = fpath.replace('1','2')
    #     %timeit two(fpath,usps_repl_list)
    #     fpath = fpath.replace('2','3')
    #     %timeit three(fpath,usps_repl_list)

    #     f = open(save_csv_path.replace('.csv','_regex.txt'),'w')
    #     f.write(usps_repl_list)
    #     f.close()

def save_to_file(A,save_csv_path):
    print '\n','Save Path:\n\n\t\t',save_csv_path,'\n'
    z                                   =   raw_input('type "y" to confirm save...')
    if z=='y':
        A.to_csv(                           save_csv_path)

def load_from_file(save_csv_path):
    return pd.read_csv(save_csv_path)


from sys import argv
if __name__ == '__main__':
    return_var                      =   None


    dir_path                                    =   os_path.join(os_environ['BD'],'geolocation/USPS')
    fpath_pdf                                   =   dir_path + '/usps_business_abbr.pdf'
    fpath_xml                                   =   dir_path + '/usps_business_abbr.xml'
    save_csv_path                               =   dir_path + '/usps_business_abbr.csv'


    if len(argv)>1:
        pass
    # t                                          =   extract_pdf_contents_from_stdout(fpath_pdf)
    # g                                          =   make_dataframe_with_contents(t)

    # A                                          =   get_street_abbrs(g)
    # A                                          =   get_business_abbr(g)

    # save_to_file(                                  A,save_csv_path)

    # A                                          =   load_from_file(save_csv_path)

    # af,usps_repl_list = make_dataframe_with_regex_params(A,common_use_col='common_use',abbrev_col='usps_abbr')
    # print 'Af',len(af)
    # bf,usps_repl_list = make_dataframe_with_regex_params(B,common_use_col='common_use',abbrev_col='usps_abbr')
    # print 'Bf',len(af)