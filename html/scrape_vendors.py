# add encoding?
#   see SL_previously_closed_vendors


# import HTML and codecs
import                                      datetime        as dt
import                                      codecs
from time                           import sleep
from urllib                         import quote_plus,unquote
from re                             import findall          as re_findall       # re_findall('patt','str','flag')
from re                             import sub              as re_sub           # re_sub('patt','repl','str','cnt')
from re                             import search           as re_search        # re_search('patt','str')
from subprocess                     import Popen            as sub_popen
from subprocess                     import PIPE             as sub_PIPE
from traceback                      import format_exc       as tb_format_exc
from sys                            import exc_info         as sys_exc_info
import                                      inspect         as I
from os                             import environ          as os_environ
from uuid                           import uuid4            as get_guid
from os                             import path             as os_path
from sys                            import path             as py_path
py_path.append(                             os_path.join(os_environ['BD'],'html'))
from HTML_API                       import getTagsByAttr,getAllTag,getInnerElement,getTagContents
from HTML_API                       import google,safe_url,getInnerHTML,FindAllTags,getSoup
from webpage_scrape                 import scraper
from selenium.webdriver.support.select import Select
py_path.append(                             os_path.join(os_environ['BD'],'files_folders'))
from API_system                     import get_input
py_path.append(                             os_path.join(os_environ['HOME'],'.scripts'))
from system_settings                import *
from System_Control                 import System_Reporter
SYS_r                                   =   System_Reporter()
py_path.append(                             os_path.join(os_environ['BD'],'geolocation'))
from f_postgres                     import pgSQL_Functions,ST_Parts
PGFS                                    =   pgSQL_Functions()

import                                      pandas              as pd
pd.set_option(                              'expand_frame_repr', False)
pd.set_option(                              'display.max_columns', None)
pd.set_option(                              'display.max_rows', 1000)
pd.set_option(                              'display.width', 180)
np = pd.np
np.set_printoptions(                        linewidth=200,threshold=np.nan)
import                                      geopandas           as gd
from types                          import NoneType
from time                           import sleep                as delay
from sqlalchemy                     import create_engine
from logging                        import getLogger
from logging                        import INFO                 as logging_info
from psycopg2                       import connect              as pg_connect

getLogger(                                  'sqlalchemy.dialects.postgresql').setLevel(logging_info)
routing_eng                             =   create_engine(r'postgresql://postgres:postgres@%s:%s/%s'
                                                        %(DB_HOST,DB_PORT,'routing'),
                                                        encoding='utf-8',
                                                        echo=False)

conn                                    =   pg_connect( "dbname='routing' "+
                                                        "user='postgres' "+
                                                        "host='%s' password='' port=8800" % DB_HOST);
cur                                     =   conn.cursor()


# from ipdb import set_trace as i_trace; i_trace()

class Scrape_Vendors:
    """

        Usage:

            # -- SEAMLESS --

            python scrape_vendors.py sl 1
            python scrape_vendors.py sl search_results

            python scrape_vendors.py sl 2
            python scrape_vendors.py sl prev_closed_v

            python scrape_vendors.py sl 3
            python scrape_vendors.py sl v_pgs


            # -- YELP --
            python scrape_vendors.py y 0
            python scrape_vendors.py y search_results

            python scrape_vendors.py y 1
            python scrape_vendors.py y api

            python scrape_vendors.py y 2
            python scrape_vendors.py y v_pgs


    """

    def __init__(self):
        T                           =   {'user'                 :   os_environ['USER'],
                                         'guid'                 :   str(get_guid().hex)[:7],
                                         'today'                :   dt.datetime.now(),
                                         'oldest_comments'      :   str(9*30),                      # in days
                                         'transcation_cnt'      :   '100',
                                         'growl_notice'         :   True,
                                         'debug'                :   True}
        T.update(                       {'tmp_tbl'              :   'tmp_' + T['guid']})
        self.T                      =   T
        self.SL                     =   Seamless(self)
        self.Yelp                   =   Yelp(self)
        self.Yelp_API               =   Yelp_API()
        self.SF                     =   Scrape_Functions(self)
        self.SV                     =   self

    def post_screenshot(self,br):
        fpath                           =   '/home/ub2/SERVER2/aprinto/static/phantom_shot'
        if THIS_PC=='ub2':
            br.screenshot(                  fpath )
        else:
            br.screenshot(                  '/tmp/phantom_shot' )
            cmds                        =   ['scp /tmp/phantom_shot %(host)s@%(serv)s:%(fpath)s;'
                                             % ({ 'host'                :   'ub2',
                                                  'serv'                :   'ub2',
                                                  'fpath'               :   fpath }),
                                             'rm -f /tmp/phantom_shot;']
            p                           =   sub_popen(cmds,stdout=sub_PIPE,shell=True)
            (_out,_err)                 =   p.communicate()
            assert _out                ==   ''
            assert _err                ==   None
        return


class Seamless:

    def __init__(self,_parent):
        self.SV                     =   _parent
        self.T                      =   _parent.T
        self.SL                     =   self

    # SEAMLESS FUNCTIONS
    #   seamless: [ base f(x) ]
    def query_seamless_directly(self,br,vend_name,sl_closed_id,scrape_gid):
        base_url                    =   'http://www.seamless.com/food-delivery/'
        url                         =   'http://www.seamless.com/'
        br.open_page(                   url)
        if br.source().count('fancybox-close')>0:
            pop_up_element      =   br.window.find_element_by_id("fancybox-close")
            if pop_up_element.is_displayed():
                pop_up_element.click()
                br.wait_for_page(       timeout_seconds=120)

        # get address from query
        address = '20 East 18th Street, New York, NY'
        new_addr_element        =   br.window.find_element_by_name("singleAddressEntry")
        if new_addr_element.is_displayed():
            new_addr_element.send_keys(address)
            new_addr_element.send_keys(u'\ue007')

        self.make_SL_search_adjustments(order_type_str='delivery')

        #------------SET SEARCH STRING
        search_element          =   br.browser.find_element_by_id('SearchType')
        assert search_element.is_displayed()==True
        search_element.send_keys(vend_name)
        search_element.send_keys(u'\ue007')
        br.wait_for_page(       timeout_seconds=120)
    def save_comments(self,br,html,vend_url):
        review_block                =   getTagsByAttr(html, 'div',
                                              {'id':'reviews'},contents=True)
        review_list                 =   getTagsByAttr(review_block, 'div',
                                              {'itemtype':'http://schema.org/Review'},contents=False)

        rev_cols                    =   ['vend_url','review_id','review_date','review_rating','review_msg']
        df                          =   pd.DataFrame(columns=rev_cols)
        for rev in review_list:
            review_date             =   getTagsByAttr(str(rev), 'input',
                                                 {'class':'ratingdate'},
                                                 contents=False)[0].attrs['value']
            dt_review_date          =   dt.datetime.utcfromtimestamp(int(review_date))

            if (self.T['today'] - dt_review_date).days > int(self.T['oldest_comments']):
                pass
            else:
                f_review_date   =   dt_review_date.isoformat()

                review_rating   =   int(getTagsByAttr(str(rev), 'input',
                                                     {'class':'rating'},
                                                     contents=False)[0].attrs['value'])
                review_msg      =   getTagsByAttr(str(rev), 'p',
                                                 {'itemprop':'reviewBody'},
                                                 contents=False)[0].contents[0].strip('\n\t ')
                author_link     =   getTagsByAttr(str(rev), 'a',
                                                 {'itemprop':'author'},
                                                 contents=False)[0].attrs['href']
                review_id       =   '_'.join([str(review_date),
                                              author_link[author_link.rfind('/')+1:]])

                df              =   df.append(dict(zip(rev_cols,
                                                       [vend_url,review_id,f_review_date,
                                                        review_rating,review_msg])),ignore_index=True)

        conn.set_isolation_level(   0)
        cur.execute(                'drop table if exists %(tmp_tbl)s;' % self.T)
        df.to_sql(                  self.T['tmp_tbl'],routing_eng,index=False)
        conn.set_isolation_level(   0)
        cmd                     =   """
                                    insert into customer_comments
                                        (vend_url,
                                        review_id,
                                        review_date,
                                        review_rating,
                                        review_msg)
                                    select t.vend_url,
                                        t.review_id,
                                        t.review_date::timestamp with time zone,
                                        t.review_rating::double precision,
                                        t.review_msg
                                    from
                                        %(tmp_tbl)s t,
                                        (  select array_agg(f.review_id) existing_review_ids
                                            from customer_comments f  ) as f1
                                    where (not existing_review_ids && array[t.review_id]
                                            or existing_review_ids is null);

                                    DROP TABLE IF EXISTS %(tmp_tbl)s;
                                    """ % self.T
        cur.execute(                cmd)
        return
    def make_SL_search_adjustments(self,order_type_str='delivery',time_str='1:00 PM'):


        #------------SET ORDER TYPE
        order_type_D            =   {'delivery'            :   '0',
                                    'pickup_20_blocks'     :   '20',
                                    'pickup_10_blocks'     :   '10',
                                    'pickup_5_blocks'      :   '5',
                                    'pickup_3_blocks'      :   '3',
                                    'pickup_1_blocks'      :   '1',}

        order_element           =   br.browser.find_element_by_id('pickupDistance')
        if order_element.get_attribute("value")!=order_type_D[ order_type_str ]:
            _select             =   Select(order_element)
            _select.select_by_value(order_type_D[ order_type_str ] )
            assert order_element.get_attribute("value")==order_type_D[ order_type_str ]

        #------------SET DELIVERY DATE
        # go to tomorrow if tmw==weekday else use today
        today_wk_day            =   int(self.T['today'].strftime('%w'))
        # want weekday (1-5), so change to tmw if 0-4
        if today_wk_day<=4:
            tmw                 =   (self.T['today'] + dt.timedelta(days=+1)).strftime('%m/%d/%Y')
            tmw_str             =   '/'.join([ it.lstrip('0') for it in tmw.split('/') ])
            date_element        =   br.browser.find_element_by_id('deliveryDate')
            _select             =   Select(date_element)
            _select.select_by_value(tmw_str)
            assert date_element.get_attribute("value")==tmw_str

        #------------SET DELIVERY TIME
        time_element            =   br.browser.find_element_by_id('deliveryTime')
        _select                 =   Select(time_element)
        _select.select_by_value(    time_str)
        assert time_element.get_attribute("value")==time_str

        return br.wait_for_page(       timeout_seconds=120)
    def update_pgsql_with_sl_page_content(self,br):



        html                            =   codecs.encode(br.source(),'utf8','ignore')
        seamless_link                   =   br.get_url()

        if seamless_link.find('http')!=0:   seamless_link='http://www.seamless.com/food-delivery/'+seamless_link
        vendor_id                       =   int(seamless_link[seamless_link[:-2].rfind('.')+1:-2])

        t                               =   getTagsByAttr(html, 'span', {'id':'VendorName'},contents=False)
        if len(t)==0:
            try:
                a                       =   getTagsByAttr(html, 'div', {'id':'Bummer'},contents=False)
                b                       =   a[0].text.replace('\n','').replace('Bummer!','').strip()
                vend_name               =   b[:b.find('(')].strip().replace("'","''")
                addr                    =   re_findall(r'[(](.*)[)]',b)[0].strip(',')
                self.T.update(              {'vendor_id':vendor_id,'vend_name':vend_name,'addr':addr} )
                cmd                     =   """
                                            update seamless
                                            set
                                                inactive                =   true,
                                                vend_name               =   '%(vend_name)s',
                                                address                 =   '%(addr)s',
                                                upd_vend_content        =   'now'::timestamp with time zone,
                                                checked_out             =   null
                                            where vend_id               =   %(vendor_id)s
                                            """%T
            except:
                self.T.update(              {'vendor_id':vendor_id})
                cmd                     =   """
                                            update seamless
                                            set
                                                inactive                =   true,
                                                upd_vend_content        =   'now'::timestamp with time zone,
                                                checked_out             =   null
                                            where vend_id               =   %(vendor_id)s
                                            """%T
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)
            return
        else:
            vend_name                   =   t[0].getText().replace('\n','').strip()

        addr                            =   getTagsByAttr(html, 'span',
                                                      {'itemprop':'streetAddress'},
                                                      contents=False)[0].contents[0]
        addr                            =   addr[:addr.find('(')].strip()
        z                               =   getTagsByAttr(html, 'span',
                                                      {'itemprop':'postalCode'},
                                                      contents=False)[0].contents[0]

        if z.find('-')!=-1:
            zipcode                     =   int(z[:z.find('-')])
        else:
            zipcode                     =   int(z)
        p                               =   getTagsByAttr(html, 'span', {'itemprop':'telephone'},contents=False)[0].contents[0]
        excl_chars                      =   ['(',')','-','x','/',',',' ']
        for it in excl_chars:      p    =   p.replace(it,'')
        phone                           =   int(p.strip()[:10])
        if len(str(phone))!=10:
            self.T.update(                  {'line_no'                  :   I.currentframe().f_back.f_lineno})
            SYS_r._growl(                   '%(line_no)s SL@%(user)s<%(guid)s>: Update Error: Phone Length Not 10.' % self.T)
            raise SystemError()
        try:
            price                       =   int(getTagsByAttr(html, 'span', {'class':'price-text'},contents=False)[0].getText().count('$'))
        except:
            price                       =   -1
        try:
            rating                      =   int(getTagsByAttr(html, 'a',
                                                        {'class':'user-rating'},
                                                        contents=False)[0].img.attrs['alt'].split(' ')[0])
            rating_total                =   int(getTagsByAttr(html, 'span',
                                                        { 'itemprop':'ratingCount',
                                                          'id':'TotalRatings'},
                                                        contents=False)[0].getText().replace('ratings','').strip())
            rating_perc                 =   rating_total/rating
            reviews                     =   int(getTagsByAttr(html, 'span',
                                                        {'itemprop':'reviewCount',
                                                         'id':'TotalReviews'},
                                                        contents=False)[0].getText())
        except:
            rating                      =   rating_total = rating_perc = -1
            reviews                     =   0
        v                               =   html.find('Delivery Estimate:')
        deliv_est                       =   '-'.join(re_findall(r'\d+', html[v:v+len('Delivery Estimate:')+100] ))
        v                               =   html.find('Delivery Minimum:')
        deliv_min                       =   float('.'.join(re_findall(r'\d+', html[v:v+len('Delivery Minimum:')+100] )[:2]))
        pickup_est                      =   '-'.join(re_findall(r'\d+', getTagsByAttr(html, 'span', {'class':'ready-time'},contents=False)[0].getText()))
        v                               =   getTagsByAttr(html, 'div',
                                                      {'class':'estimates',
                                                       'id':'RestaurantDetails'},
                                                      contents=False)[0]
        estimates_blob                  =   re_sub(r'\s+', ' ', v.findAll('span')[3].getText().replace('\n',''))
        description                     =   getTagsByAttr(html, 'meta',
                                                      {'property':'og:description'},
                                                      contents=False)[0].attrs['content']
        try:
            cuisine                     =   getTagsByAttr(html, 'li',
                                                      {'itemprop':'servesCuisine'},
                                                      contents=False)[0].contents[0]
        except:
            cuisine                     =   None

        upd_vend_content                =   self.T['today'].isoformat()
        page_vars                       =   [seamless_link,vendor_id,vend_name,addr,zipcode,phone,price,
                                             rating,rating_total,rating_perc,description,reviews,
                                             deliv_est,deliv_min,pickup_est,cuisine,estimates_blob,
                                             upd_vend_content]
        var_names                       =   ','.join( [  'sl_link,vend_id,vend_name,address,zipcode,phone,price',
                                                         'rating,rating_total,rating_perc,description,reviews',
                                                         'deliv_est,deliv_min,pickup_est,cuisine,estimates_blob',
                                                         'upd_vend_content'] ).split(',')
        conn.set_isolation_level(           0)
        cur.execute(                        'drop table if exists %(tmp_tbl)s' % self.T)
        pd.DataFrame(                       [page_vars],columns=var_names).to_sql(self.T['tmp_tbl'],routing_eng)

        # first try to update vend_id
        self.T.update(                      {'wc'             :   '%%' })
        cmd                             =   """
                                                update seamless s
                                                set
                                                    vend_id         =   t.vend_id
                                                from %(tmp_tbl)s t
                                                where
                                                    ((
                                                    concat('%(wc)s',s.address,'%(wc)s')
                                                        ilike concat('%(wc)s',t.address,'%(wc)s')
                                                    OR
                                                    concat('%(wc)s',t.address,'%(wc)s')
                                                        ilike concat('%(wc)s',s.address,'%(wc)s')
                                                    )
                                                    OR
                                                    (
                                                    concat('%(wc)s',s.vend_name,'%(wc)s')
                                                        ilike concat('%(wc)s',t.vend_name,'%(wc)s')
                                                    OR
                                                    concat('%(wc)s',t.vend_name,'%(wc)s')
                                                        ilike concat('%(wc)s',s.vend_name,'%(wc)s')
                                                    ))
                                                and   s.zipcode     =   t.zipcode
                                                and   s.phone       =   t.phone
                                                and   s.upd_vend_content < t.upd_vend_content::timestamp with time zone

                                            """ % self.T
        conn.set_isolation_level(           0)
        cur.execute(                        cmd)
        # upsert to seamless
        cmd                             =   """
                                                with upd as (
                                                    update seamless s
                                                    set
                                                        vend_name       =   t.vend_name,
                                                        address         =   t.address,
                                                        zipcode         =   t.zipcode,
                                                        phone           =   t.phone,
                                                        price           =   t.price,
                                                        rating          =   t.rating,
                                                        rating_total    =   t.rating_total,
                                                        rating_perc     =   t.rating_perc,
                                                        description     =   t.description,
                                                        reviews         =   t.reviews,
                                                        deliv_est       =   t.deliv_est,
                                                        deliv_min       =   t.deliv_min,
                                                        pickup_est      =   t.pickup_est,
                                                        cuisine         =   t.cuisine,
                                                        estimates_blob  =   t.estimates_blob,
                                                        upd_vend_content=   'now'::timestamp with time zone,
                                                        skipped         =   false,
                                                        checked_out     =   null
                                                    from %(tmp_tbl)s t
                                                    where s.vend_id     =   t.vend_id
                                                    returning t.vend_id vend_id
                                                )
                                                insert into seamless ( sl_link,
                                                                       vend_id,
                                                                       vend_name,
                                                                       address,
                                                                       zipcode,
                                                                       phone,
                                                                       price,
                                                                       rating,
                                                                       rating_total,
                                                                       rating_perc,
                                                                       description,
                                                                       reviews,
                                                                       deliv_est,
                                                                       deliv_min,
                                                                       pickup_est,
                                                                       cuisine,
                                                                       estimates_blob,
                                                                       upd_vend_content,
                                                                       skipped,
                                                                       checked_out)
                                                select
                                                    t.sl_link,
                                                    t.vend_id,
                                                    t.vend_name,
                                                    t.address,
                                                    t.zipcode,
                                                    t.phone,
                                                    t.price,
                                                    t.rating,
                                                    t.rating_total,
                                                    t.rating_perc,
                                                    t.description,
                                                    t.reviews,
                                                    t.deliv_est,
                                                    t.deliv_min,
                                                    t.pickup_est,
                                                    t.cuisine,
                                                    t.estimates_blob,
                                                    'now'::timestamp with time zone,
                                                    false,
                                                    null
                                                from
                                                    %(tmp_tbl)s t,
                                                    (select array_agg(f.vend_id) upd_vend_ids from upd f) as f1
                                                where (not upd_vend_ids && array[t.vend_id]
                                                    or upd_vend_ids is null);

                                                DROP TABLE %(tmp_tbl)s;
                                            """ % self.T
        conn.set_isolation_level(           0)
        cur.execute(                        cmd)

        if rating!=-1:

            try:
                review_url              =   getTagsByAttr(html, 'a',
                                                          {'class':'showRatingsTab'},
                                                          contents=False)[0].attrs['href']
                br.open_page(               review_url)
                self.SL.save_comments(      br,html,seamless_link)

            except Exception, err:
                print tb_format_exc()
                print sys_exc_info()[0]
                print seamless_link
                from ipdb import set_trace as i_trace; i_trace()

        # from ipdb import set_trace as i_trace; i_trace()

        return
    #   seamless: 1 of 3
    def scrape_sl_1_search_results(self,query_str=''):
        """
        get results from seamless address search and update pgsql -- worked 2014.11.16
        """
        def get_sl_addr_search_results(src):
            br                          =   scraper('phantom').browser
            only_delivery               =   True

            #------------goto main page, identify PDF-page url, goto PDF-page url
            base_url                    =   'http://www.seamless.com/food-delivery/'
            url                         =   'http://www.seamless.com/'
            br.open_page(                   url)
            if br.source().count('fancybox-close')>0:
                pop_up_element      =   br.window.find_element_by_id("fancybox-close")
                if pop_up_element.is_displayed():
                    pop_up_element.click()
                    br.wait_for_page(       timeout_seconds=120)

            d                           =   pd.read_sql(src,routing_eng)

            for i in range(len(d)):
                street,zipcode,gid      =   d.ix[i,['address','zipcode','gid']].astype(str)
                address                 =   street.title() + ', New York, NY, ' + zipcode

                new_addr_element        =   br.window.find_element_by_name("singleAddressEntry")
                if new_addr_element.is_displayed():
                    new_addr_element.send_keys(address)
                    new_addr_element.send_keys(u'\ue007')
                else:
                    if br.source().count('fancybox-close')>0:
                        pop_up_element      =   br.window.find_element_by_id("fancybox-close")
                        if pop_up_element.is_displayed():
                            pop_up_element.click()
                            br.wait_for_page(       timeout_seconds=120)
                    new_addr_element    =   br.window.find_element_by_name("singleAddressEntry")
                    if new_addr_element.is_displayed():
                        new_addr_element.send_keys(address)
                        new_addr_element.send_keys(u'\ue007')

                br.wait_for_page(           timeout_seconds=120)


                self.make_SL_search_adjustments(order_type_str='delivery')


                if br.window.find_element_by_id("MessageArea").text.find('Your exact address could not be located by our system.') != -1:
                    br.window.find_element_by_name("singleAddressEntry").clear()
                elif br.window.find_element_by_class_name("error-header").text.find('Your exact address could not be located by our system.') != -1:
                    br.window.find_element_by_name("singleAddressEntry").clear()
                elif br.window.find_element_by_class_name("error-header").text.find("We can't find your address.") != -1:
                    br.window.find_element_by_id("fancybox-close").click()
                    br.window.find_element_by_name("singleAddressEntry").clear()
                else:
                    a                   =   br.window.execute_script('return document.body.scrollHeight;')
                    br.window.execute_script("window.scrollTo(%s, document.body.scrollHeight);" % str(a))
                    br.wait_for_page(       timeout_seconds=120)
                    b                   =   br.window.execute_script('return document.body.scrollHeight;')
                    br.window.execute_script("window.scrollTo(%s, document.body.scrollHeight);" % str(b))
                    br.wait_for_page(       timeout_seconds=120)
                    while a != b:
                        a               =   br.window.execute_script('return document.body.scrollHeight;')
                        br.window.execute_script("window.scrollTo(%s, document.body.scrollHeight);" % str(a))
                        br.wait_for_page(   timeout_seconds=120)
                        b               =   br.window.execute_script('return document.body.scrollHeight;')
                        br.window.execute_script("window.scrollTo(%s, document.body.scrollHeight);" % str(b))
                        br.wait_for_page(   timeout_seconds=120)
                # --- 2. update pgsql:seamless with address search results
                html                    =   codecs.encode(br.source(),'utf8','ignore')
                z                       =   getTagsByAttr(html, 'div', {'class':'restaurant-name'},contents=False)
                open_res_total          =   len(z)
                h                       =   pd.Series(map(lambda a: a.a.attrs['href'],z))
                h                       =   h.map(lambda s: base_url + s if s.find('http')==-1 else s)
                t                       =   pd.Series(map(lambda a: a.a.attrs['title'],z))
                conn.set_isolation_level(   0)
                cur.execute(                "drop table if exists %(tmp_tbl)s;" % self.T)
                pd.DataFrame(               {'sl_link':h,'search_link_blob':t}).to_sql(self.T['tmp_tbl'],routing_eng)

                conn.set_isolation_level(0)
                cur.execute(                """
                                            alter table %(tmp_tbl)s add column vend_id bigint;

                                            update %(tmp_tbl)s
                                            set vend_id = substring(sl_link from
                                                '[[:punct:]]([[:digit:]]*)[[:punct:]][r]$')::bigint
                                            where vend_id is null;
                                            """ % self.T )
                conn.set_isolation_level(   0)
                cur.execute(                """
                                            with upd as (
                                                update seamless s
                                                set
                                                    search_link_blob = t.search_link_blob,
                                                    upd_search_links = 'now'::timestamp with time zone
                                                from %(tmp_tbl)s t
                                                where s.vend_id = t.vend_id
                                                returning s.vend_id vend_id
                                            )
                                            insert into seamless (
                                                sl_link,
                                                vend_id,
                                                search_link_blob,
                                                upd_search_links
                                                )
                                            select t.sl_link,t.vend_id,t.search_link_blob,'now'::timestamp with time zone
                                            from
                                                %(tmp_tbl)s t,
                                                (select array_agg(f.vend_id) all_vend_id from seamless f) as f2
                                            where not all_vend_id @> array[t.vend_id];

                                            drop table if exists %(tmp_tbl)s;
                                            """ % self.T)

                # --- 3. update pgsql:seamless_closed with seamless address search results
                closed_vend_element     =   br.window.find_element_by_id("ShowClosedVendorsLink")
                if closed_vend_element.is_displayed():
                    closed_vend_element.click()
                br.wait_for_page(           timeout_seconds=120)
                html                    =   codecs.encode(br.source(),'utf8','ignore')
                z                       =   getTagsByAttr(html, 'div', {'class':'closed1'},contents=False)
                closed_res_total        =   len(z)
                tmp                     =   map(lambda a: [a.contents[2].replace('\n','').replace('\t','').strip()]+
                                                a.span.contents[0].lower().replace('\n','').replace('\t','')\
                                                .replace('open','').strip().split('-'),z)

                self.T.update(              {'day':dt.datetime.strftime(dt.datetime.now(),'%a').lower()})
                cols                    =   str('vend_name,opens_%(day)s,closes_%(day)s' % self.T).split(',')
                x                       =   pd.DataFrame(tmp,columns=cols)
                x[cols[1]]              =   x[cols[1]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
                x[cols[2]]              =   x[cols[2]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
                conn.set_isolation_level(   0)
                cur.execute(                "drop table if exists %(tmp_tbl)s;" % self.T)
                x.to_sql(                   self.T['tmp_tbl'],routing_eng)
                # upsert
                check                   =   pd.read_sql('select count(*) cnt from seamless_closed',routing_eng).cnt[0]
                if check == 0:
                    conn.set_isolation_level(0)
                    cur.execute(            """
                                            insert into seamless_closed (
                                                 vend_name,
                                                 opens_%(day)s,
                                                 closes_%(day)s,
                                                 last_updated,
                                                 )
                                            select
                                                 t.vend_name,
                                                 t.opens_%(day)s::time with time zone,
                                                 t.closes_%(day)s::time with time zone,
                                                 'now'::timestamp with time zone
                                            from
                                                %(tmp_tbl)s t;

                                            drop table if exists %(tmp_tbl)s;
                                            """ % self.T)
                else:
                    conn.set_isolation_level(0)
                    cur.execute(            """
                                            with upd as (
                                                update seamless_closed s
                                                set
                                                    opens_%(day)s = t.opens_%(day)s::time with time zone,
                                                    closes_%(day)s = t.closes_%(day)s::time with time zone,
                                                    last_updated = 'now'::timestamp with time zone
                                                from
                                                    %(tmp_tbl)s t
                                                where s.vend_name = t.vend_name
                                                returning s.vend_name vend_name
                                            )
                                            insert into seamless_closed (
                                                                        vend_name,
                                                                        opens_%(day)s,
                                                                        closes_%(day)s,
                                                                        last_updated )
                                            select
                                                t.vend_name,
                                                t.opens_%(day)s::time with time zone,
                                                t.closes_%(day)s::time with time zone,
                                                'now'::timestamp with time zone
                                            from
                                                %(tmp_tbl)s t,
                                                (select array_agg(f.vend_name) all_vend_names from seamless_closed f) as f2
                                            where not all_vend_names @> array[t.vend_name];

                                            drop table if exists %(tmp_tbl)s;
                                            """ % self.T)
                # --- 4. update pgsql:scrape_lattice
                conn.set_isolation_level(   0)
                cur.execute(                """ update scrape_lattice
                                                set
                                                    sl_open_cnt=%s,
                                                    sl_closed_cnt=%s,
                                                    sl_updated='now'::timestamp with time zone
                                                where gid=%s"""%(open_res_total,
                                                                 closed_res_total,
                                                                 gid))
                # --- 5. put in new address -- repeat
                addresses               =   br.window.find_element_by_xpath("//select[@id='Address']")
                last_option             =   len(addresses.find_elements_by_tag_name('option'))-1
                addresses.find_elements_by_tag_name('option')[last_option].click()
                br.wait_for_page(           timeout_seconds=120)
            br.quit()

        print self.T['guid']



        src                             =   """ select gid,address,zipcode from scrape_lattice
                                                where address is null
                                                or sl_updated is null
                                                or age('now'::timestamp with time zone,sl_updated) > interval '1 day'
                                                limit %(transcation_cnt)s
                                            """ % self.T
        src                             =   src if not query_str else query_str
        get_sl_addr_search_results(         src )
        global T
        self.T.update(                      {'line_no'                  :   I.currentframe().f_back.f_lineno})
        msg                             =   '%(line_no)s SL@%(user)s<%(guid)s>: Search Results Scraped.' % self.T
        SYS_r._growl(                       msg )
        print msg
        return True
    #   seamless: 2 of 3
    def scrape_sl_2_previously_closed_vendors(self,query_str=''):
        """
        get url and html for closed vendors -- worked 2014.11.18
        """
        print self.T['guid']

        import sys
        reload(                             sys)
        sys.setdefaultencoding(             'UTF8')

        global T
        self.T.update(                      {'tbl_name'         :   'seamless_closed',
                                             'tbl_uid'          :   'id',
                                             'upd_var'          :   'upd_seamless',
                                             'select_vars'      :   'vend_name,id,scrape_gid'})

        # new SL vendors not yet added to seamless DB
        t                               =   """ UPDATE %(tbl_name)s t
                                                    SET checked_out         = null
                                                    WHERE checked_out       = '%(guid)s';

                                                UPDATE %(tbl_name)s t
                                                SET checked_out         =   '%(guid)s'
                                                FROM (
                                                    SELECT array_agg(%(tbl_uid)s) all_ids from %(tbl_name)s t2
                                                    WHERE ( t2.checked_out is null )
                                                    AND (
                                                        t2.%(upd_var)s  is   false
                                                    )
                                                    AND t2.inactive     is   false
                                                    GROUP BY t2.%(upd_var)s,t2.%(tbl_uid)s
                                                    ORDER BY t2.%(upd_var)s ASC,t2.%(tbl_uid)s ASC
                                                    LIMIT %(transcation_cnt)s
                                                    ) as f1
                                                WHERE all_ids && array[t.%(tbl_uid)s];

                                                SELECT %(select_vars)s from %(tbl_name)s
                                                WHERE checked_out       =   '%(guid)s';
                                            """ % self.T

        src                             =   t if not query_str else query_str

        d                               =   pd.read_sql(src,routing_eng)

        x                               =   d.vend_name.tolist()
        y                               =   d['id'].tolist()
        z                               =   d['scrape_gid'].tolist()
        vend_name_id_D                  =   dict(zip(x,y))
        vend_name_scrape_gid_D          =   dict(zip(x,z))



        base_url                        =   'http://www.seamless.com/food-delivery/'

        br                              =   scraper('phantom').browser

        stop                            =   False
        for it in x:
            url                         =   ''.join(['http://www.google.com/search?as_q=%s' % quote_plus(it.encode('utf-8')),
                                                 '&as_sitesearch=www.seamless.com&as_occt=any&btnI=1'])
            br.open_page(                   url)
            z                           =   br.get_url()
            if z.count('google')>0:
                while z.count('/sorry/')!=0:

                    K                   =   br.browser.find_elements_by_tag_name('img')[0]

                    start_location      =   br.browser.set_window_position
                    start_size          =   br.browser.set_window_size
                    br.browser.set_window_position=K.location
                    br.browser.set_window_size=K.size
                    self.SV.post_screenshot(br)
                    br.browser.set_window_position=start_location
                    br.browser.set_window_size=start_size

                    self.T.update(          {'line_no'                  :   I.currentframe().f_back.f_lineno})
                    SYS_r._growl(           '%(line_no)s SL@%(user)s<%(guid)s>: NEED CAPTCHA' % self.T,
                                            'http://demo.aporodelivery.com/phantomjs.html' )
                    captcha_input       =   get_input("Captcha code?\n")
                    br.browser.find_element_by_id("captcha").send_keys(captcha_input)
                    br.browser.find_element_by_name("submit").click()
                    z                   =   br.get_url()

            if z.count('google.com/search?')>0:
                q                       =   codecs.encode(br.source(),'utf8','ignore')
                a                       =   google()
                url                     =   a.get_results(q)[0].url
                br.open_page(               url)
                z                       =   br.get_url()

            if br.source().count('fancybox-close')>0:
                popup_element           =   br.window.find_element_by_id("fancybox-close")
                if popup_element.is_displayed():
                    popup_element.click(    )
                    br.wait_for_page(       timeout_seconds=120)
                    z                   =   br.get_url()

            if len(z)-2==len(z.rstrip('.z')):        # meaning, the page is a SL Vendor page ...
                pass
            else:
                continue_processing     =   False
                # z                       =   self.query_seamless_directly(br             =   br,
                #                                                          vend_name      =   it,
                #                                                          sl_closed_id   =   vend_name_id_D[it],
                #                                                          scrape_gid     =   vend_name_scrape_gid_D[it])

            sl_link                     =   z if z.find('http')==0 else base_url + z

            try:
                vendor_id               =   int(z[z[:-2].rfind('.')+1:-2])
                html                    =   codecs.encode(br.source(),'utf8','ignore')
                vend_name               =   getTagsByAttr(html, 'span', {'id':'VendorName'},
                                                          contents=False)[0].getText().replace('\n','').strip()
                continue_processing     =   True
            except:
                continue_processing     =   False


            if not continue_processing:

                conn.set_isolation_level(0)
                cur.execute(                """
                                            update seamless_closed
                                            set
                                                inactive = true,
                                                inactive_on = 'now'::timestamp with time zone,
                                                sl_link = '%s',
                                                last_updated = 'now'::timestamp with time zone,
                                                checked_out = null
                                            where id = %s
                                            """ % (sl_link,vend_name_id_D[it]) )
                continue_processing     =   False

            if continue_processing:

                self.SL.update_pgsql_with_sl_page_content(br)

                conn.set_isolation_level(   0)
                cur.execute(                """
                                            update seamless_closed sc
                                            set
                                                upd_seamless = true,
                                                sl_link = '%(sl_link)s',
                                                last_updated = 'now'::timestamp with time zone,
                                                checked_out = null
                                            where id = '%(id)s'
                                                """ % { 'id'           :   vend_name_id_D[it],
                                                        'sl_link'      :   sl_link} )


        self.T.update(                      {'line_no'                  :   I.currentframe().f_back.f_lineno})
        msg                             =   '%(line_no)s SL@%(user)s<%(guid)s>: Prev. Closed Updated.' % self.T
        print msg
        SYS_r._growl(                       msg)
        br.quit()
        return True
    #   seamless: 3 of 3
    def scrape_sl_3_known_vendor_pages(self,query_str=''):
        print self.T['guid']
        self.T.update(                      {'tbl_name'                     :   'seamless',
                                             'tbl_uid'                      :   'id',
                                             'upd_var'                      :   'upd_vend_content',
                                             'upd_interval'                 :   '3 days',
                                             'select_vars'                  :   'id,sl_link' })

        t                               =   """ UPDATE %(tbl_name)s t
                                                    SET checked_out         = null
                                                    WHERE checked_out       = '%(guid)s';

                                                UPDATE %(tbl_name)s t
                                                SET checked_out             =   '%(guid)s'
                                                FROM (
                                                    SELECT array_agg(%(tbl_uid)s) all_ids from %(tbl_name)s t2
                                                    WHERE ( t2.checked_out is null )
                                                    AND (
                                                        t2.%(upd_var)s      is   null
                                                        OR age('now'::timestamp with time zone,
                                                               t2.%(upd_var)s) > interval '%(upd_interval)s'
                                                    )
                                                    AND t2.inactive         is   false
                                                    AND t2.skipped          is   false
                                                    GROUP BY t2.%(upd_var)s,t2.%(tbl_uid)s
                                                    ORDER BY t2.%(upd_var)s ASC,t2.%(tbl_uid)s ASC
                                                    LIMIT %(transcation_cnt)s
                                                    ) as f1
                                                WHERE all_ids && array[t.%(tbl_uid)s];

                                                SELECT %(select_vars)s from %(tbl_name)s
                                                WHERE checked_out       =   '%(guid)s';
                                            """ % self.T

        query_str                       =   t if not query_str else query_str
        d                               =   pd.read_sql(query_str,routing_eng)
        sl_links                        =   d.sl_link.tolist()
        br                              =   scraper('phantom').browser

        base_url                        =   'http://www.seamless.com/food-delivery/'
        first_link                      =   sl_links[0]
        url                             =   base_url+first_link.replace(base_url,'')
        br.open_page(                       url)

        if br.source().count('fancybox-close')>0:
            popup_element               =   br.window.find_element_by_id("fancybox-close")
            if popup_element.is_displayed():
                popup_element.click(        )
                br.wait_for_page(           timeout_seconds=120)
                z                       =   br.get_url()

        self.SL.update_pgsql_with_sl_page_content(  br)
        sleep(                              5)
        skipped                         =   0
        for it in sl_links[1:]:
            url                         =   base_url+it.replace(base_url,'')
            br.open_page(                   url)
            try:
                self.SL.update_pgsql_with_sl_page_content(br)
            except:
                self.T.update(              {'line_no'                  :   I.currentframe().f_back.f_lineno,
                                             'current_url'              :   br.get_url()})
                msg                     =   '%(line_no)s SL@%(user)s<%(guid)s>: Issue with Known Vendors @ %(current_url)s' % self.T
                print msg
                SYS_r._growl(               msg)

                current_url             =   "'"++"'"
                conn.set_isolation_level(   0)
                cur.execute(                "update seamless set skipped=true,checked_out=null where sl_link = %s"%current_url)
                skipped                +=   1


        self.T.update(                      {'line_no'                  :   I.currentframe().f_back.f_lineno,
                                            'current_url'               :   br.get_url()})
        msg                             =   '%(line_no)s SL@%(user)s<%(guid)s>: Known Vendors Updated.' % self.T
        print msg
        SYS_r._growl(                       msg)
        br.quit()
        return True


class Yelp_API:

    def __init__(self):
        global OAuth1Session,j_dump
        from rauth                  import OAuth1Session
        from json                   import dumps            as j_dump
        self.consumer_key           =   'QzH1O3EktEQt89kegeaUxQ'
        self.consumer_secret        =   'Q_GtZiKGtRvqQSTjGOSgsuogkTE'
        self.token                  =   '6T7dDEQhf41FA2DIajIDZxsm4RwvBdM9'
        self.token_secret           =   'YNaWq3LCjlQu9ir4Ibo-Zp6ELKI'

    def yelp_business_api(self,biz_id):
        params                      =   {}
        api_url                     =   'http://api.yelp.com/v2/business/' + biz_id
        return self.get_results(        params,api_url,api_branch='business')

    def yelp_search_api(self,location,radius_in_meters):
        params                      =   {}
        #params["term"]              =   "restaurant" # optional, all returned if not included
        params["limit"]             =   '20'
        params["offset"]            =   '0'
        params["sort"]              =   1                                   # 0=Best Match, 1=Distance, 2=Highest Rated
        params['location']          =   location
        params["category_filter"]   =   'restaurants'
        params["radius_filter"]     =   str(radius_in_meters)
        api_url                     =   'http://api.yelp.com/v2/search'
        return self.get_results(        params,api_url,api_branch='search')

    def get_results(self,params,url,api_branch):
        T                           =   {'search'                   :   'businesses',
                                         'business'                 :   ''}
        session                     =   OAuth1Session(
                                            consumer_key            = self.consumer_key,
                                            consumer_secret         = self.consumer_secret,
                                            access_token            = self.token,
                                            access_token_secret     = self.token_secret)
        request                     =   session.get(url,params=params)
        d                           =   request.json()

        if d.has_key('error'):
            return self.error_handling( returned_msg=d,previous_results=None)

        df                          =   pd.read_json(j_dump(d[ T[api_branch] ]))
        while d['total']!=len(df):
            params["offset"]        =   int(params["offset"]) + int(params["limit"])
            request                 =   session.get(url,params=params)
            d                       =   request.json()

            if d.has_key('error'):
                return self.error_handling(returned_msg=d,previous_results=df)

            t                       =   pd.read_json(  j_dump(  d[  T[api_branch]  ]  )  )
            df                      =   df.append(t,ignore_index=True)

            if d['total']==len(df):
                break

        assert d['total']==len(df)
        status                      =   'OK'
        session.close(                  )
        return df,status

    def error_handling(self,returned_msg,previous_results=None):
        if returned_msg['error']['description']=='The maximum number of accessible results is 1000':
            status                  =   'max results reached'
        else:
            status                  =   returned_msg['error']['description']
        return previous_results,status


class Yelp:

    def __init__(self,_parent):
        self.SV                     =   _parent
        self.T                      =   _parent.T
        self.Yelp                   =   self

    # YELP FUNCTIONS
    #   yelp:     0 of 2
    def scrape_yelp_0_search_results(self,query_str=''):
        """
        get results from yelp address search and update pgsql
        """
        print self.T['guid']
        import sys
        reload(sys)
        sys.setdefaultencoding(         'UTF8')

        t                               =   """ select gid,address,zipcode
                                                from scrape_lattice
                                                where yelp_updated > '2014-11-24 18:22:59.045361-05'::timestamp with time zone;
                                                limit %(transcation_cnt)s
                                            """ % self.T

        query_str                       =   t if not query_str else query_str
        s                               =   pd.read_sql( query_str,routing_eng )

        p                               =   map(lambda s: str(s[0].title()+', New York, NY '+str(s[1])),
                                                zip(s.address,s.zipcode))

        br                              =   scraper('phantom').browser

        d_cols                          =   ['vend_name','url','phone']
        base_url                        =   'http://www.yelp.com'
        for i in range(len(p)):
            gid                         =   s.ix[i,'gid']
            search_addr                 =   p[i]

            url                         =   base_url+'/search?find_desc='+safe_url('restaurant')+'&find_loc='+safe_url(search_addr)
            br.open_page(                   url)


            from ipdb import set_trace as i_trace; i_trace()


            if getTagsByAttr(br.source(), 'div', {'class':'no-results'},contents=False): pass
            else:
                html                =   codecs.encode(br.source(),'utf8','ignore')
                if html.find('ylist')==-1:
                    res_num         =   0
                    conn.set_isolation_level(0)
                    cur.execute(        """ update scrape_lattice
                                            set yelp_cnt=%s,
                                            yelp_updated='now'::timestamp with time zone
                                            where gid=%s
                                        """%(str(res_num),gid))
                else:
                    a               =   getTagsByAttr(html, 'span', {'class':'pagination-results-window'},contents=True)
                    res_num         =   int(re_findall(r'\d+', str(a[a.find('of')+3:]))[0])
                    conn.set_isolation_level(0)
                    cur.execute(        """ update scrape_lattice
                                            set yelp_cnt=%s,
                                            yelp_updated='now'::timestamp with time zone
                                            where gid=%s
                                        """%(str(res_num),gid))
                    d               =   pd.DataFrame(columns=d_cols)
                    first_page,last_page = True,False

                    while last_page == False:

                        a           =   getTagsByAttr(html, 'ul',
                                                      {'class':'ylist ylist-bordered search-results'},
                                                      contents=False)
                        names       =   a[0].findAll('a',attrs={'class':'biz-name'})
                        names_proper=   map(lambda s: str(s.contents[0]).replace('\xe2\x80\x99',"'")
                                            if len(s.contents)>0 else '',names)
                        links       =   map(lambda s: base_url+str(s.attrs['href']),names)
                        phones      =   a[0].findAll('span',attrs={'class':'biz-phone'})
                        phones_proper = map(lambda s: ''.join(re_findall(r'\d+', str(s))),phones)

                        z           =   {'vend_name':pd.Series(names_proper),
                                         'url':pd.Series(links),
                                         'phone':pd.Series(phones_proper)}
                        d           =   d.append(pd.DataFrame(data=z,columns=d_cols),ignore_index=True)

                        next_page   =   getSoup(html).findAll('a', {'class':'page-option prev-next'})
                        if first_page==True and len(next_page)==1:
                            next_page_link = base_url + next_page[0].attrs['href']
                            br.open_page(next_page_link)
                            html    =   codecs.encode(br.source(),'utf8','ignore')
                            first_page= False
                        elif len(next_page)==2:
                            next_page_link = base_url + next_page[1].attrs['href']
                            br.open_page(next_page_link)
                            html    =   codecs.encode(br.source(),'utf8','ignore')
                        else:
                            last_page=  True
                            break

                    # upsert to yelp
                    conn.set_isolation_level(0)
                    cur.execute(        'drop table if exists %(tmp_tbl)s' % self.T)
                    d['id']         =   d.url.map(lambda s: s[s.find('/biz/')+5:])
                    d['phone_as_text'] = d.phone.map(str)
                    d.to_sql(           self.T['tmp_tbl'],routing_eng)

                    cmd             =   """
                                        with upd as (
                                            update yelp y
                                            set
                                                id = t.id,
                                                vend_name = t.vend_name,
                                                url = t.url,
                                                phone_as_text = t.phone_as_text,
                                                upd_search_links = 'now'::timestamp with time zone
                                            from %(tmp_tbl)s t
                                            where y.url = t.url
                                            returning t.url url
                                        )
                                        insert into yelp ( id,
                                                           vend_name,
                                                           url,
                                                           phone_as_text,
                                                           upd_search_links)
                                        select
                                            t.id,
                                            t.vend_name,
                                            t.url,
                                            t.phone_as_text,
                                            'now'::timestamp with time zone
                                        from
                                            %(tmp_tbl)s t,
                                            (select array_agg(f.url) upd_vend_urls from upd f) as f2
                                        where (not upd_vend_urls && array[t.url]
                                            or upd_vend_urls is null);

                                        drop table %(tmp_tbl)s;

                                        """ % self.T
                    conn.set_isolation_level(0)
                    cur.execute(        cmd)



        self.T.update(                      {'line_no'                  :   I.currentframe().f_back.f_lineno})
        msg                             =   '%(line_no)s Yelp@%(user)s<%(guid)s>: Search Results Scraped.' % self.T
        print msg
        SYS_r._growl(                       msg)
        br.quit()
        return True
    #   yelp:     1 of 2
    def scrape_yelp_1_api(self,query_str='',scrape_lattice='scrape_lattice'):
        """
        get results from yelp Search API with scape lattice addresses and update pgsql -- worked 2014.11.17
        """
        print self.T['guid']
        YELP                            =   Yelp_API()

        self.T.update(                      { 'latt_tbl'         :   scrape_lattice,})

        t                               =   """ select gid,address,zipcode from %(latt_tbl)s
                                                where yelp_updated is null
                                                or age('now'::timestamp with time zone,yelp_updated)
                                                > interval '1 day'
                                                limit %(transcation_cnt)s
                                            """ % self.T

        query_str                       =   t if not query_str else query_str

        s                               =   pd.read_sql( query_str,routing_eng )

        p                               =   map(lambda s: str(s[0].title()+', New York, NY '+str(s[1])),
                                                zip(s.address,s.zipcode))

        # (from scrape_lattice creation function) [ADD TO SETTINGS DB]
        buffer_in_miles                 =   0.2
        meters_in_one_mile              =   1609.34
        radius_in_meters                =   buffer_in_miles * meters_in_one_mile
        last_run                        =   False
        msg                             =   'Yelp@%s: API Scrape Complete' % os_environ['USER']
        for i in range(len(p)):
            search_addr                 =   p[i]
            df,status                   =   YELP.yelp_search_api(search_addr,radius_in_meters)

            self.T.update(                  {'line_no'                  :   I.currentframe().f_back.f_lineno,
                                             'status'                   :   status})
            if type(df)==NoneType:
                msg                     =   '%(line_no)s Yelp@%(user)s<%(guid)s>: API Scrape -- ABORTED b/c %(status)s' % self.T
                print msg
                SYS_r._growl(               msg)
                return

            if not status=='OK':
                last_run                =   True
                msg                     =   '%(line_no)s Yelp@%(user)s<%(guid)s>: API Scrape -- ABORTED b/c %(status)s' % self.T
            else:
                self.T.update(              {'gid'                  :   s.ix[i,'gid'],
                                             'api_res_cnt'          :   len(df)})

                conn.set_isolation_level(   0)
                cur.execute(                """ update %(latt_tbl)s
                                                set yelp_cnt        =   %(api_res_cnt)s,
                                                yelp_updated        =   'now'::timestamp with time zone
                                                where gid           =   %(gid)s;
                                            """ % self.T )

            if len(df)>0:
                all_res_cols            =   df.columns.tolist()
                df['vend_name']         =   df.name
                if all_res_cols.count('phone')>0:
                    df['phone']         =   df.phone.map(lambda s: int(s) if str(s)[0].isdigit() else None)
                else:
                    df['phone']         =   None
                df['address']           =   df.location.map(lambda s:
                                                    None if len(s['address'])==0
                                                    else s['address'][0])
                df['display_address']   =   df.location.map(lambda s:
                                                    None if s.keys().count('display_address')==0
                                                    else ','.join(s['display_address']))
                df['neighborhoods']     =   df.location.map(lambda s:
                                                    None if s.keys().count('neighborhoods')==0
                                                    else s['neighborhoods'][0])
                df['city']              =   df.location.map(lambda s:
                                                    None if s.keys().count('city')==0
                                                    else s['city'])
                df['state_code']        =   df.location.map(lambda s:
                                                    None if s.keys().count('state_code')==0
                                                    else s['state_code'])
                df['postal_code']       =   df.location.map(lambda s:
                                                    None if s.keys().count('postal_code')==0
                                                    else int(s['postal_code']))
                df['latitude']          =   df.location.map(lambda s:
                                                    None if (s.keys().count('coordinate')==0 or
                                                            s['coordinate'].keys().count('latitude')==0)
                                                    else s['coordinate']['latitude'])
                df['longitude']         =   df.location.map(lambda s:
                                                    None if (s.keys().count('coordinate')==0 or
                                                            s['coordinate'].keys().count('longitude')==0)
                                                    else s['coordinate']['longitude'])
                df['geo_accuracy']      =   df.location.map(lambda s:
                                                    None if s.keys().count('geo_accuracy')==0
                                                    else int(s['geo_accuracy']))
                if df.columns.tolist().count('menu_date_updated')==0:
                    df['menu_date_updated'] = None
                else:
                    df['menu_date_updated'] = df.menu_date_updated.map(lambda x:
                        None if str(x)[0].isdigit()==False
                        else dt.datetime.fromtimestamp(  int(x)  ).strftime('%Y-%m-%d %H:%M:%S')
                                                                        )
                df                      =   df.ix[:,['id',
                                                     'vend_name',
                                                     'phone',
                                                     'address',
                                                     'display_address',
                                                     'neighborhoods',
                                                     'city',
                                                     'state_code',
                                                     'postal_code',
                                                     'display_phone',
                                                     'is_claimed',
                                                     'is_closed',
                                                     'menu_date_updated',
                                                     'menu_provider',
                                                     'rating',
                                                     'review_count',
                                                     'categories',
                                                     'url',
                                                     'latitude',
                                                     'longitude',
                                                     'geo_accuracy']]

                conn.set_isolation_level(   0)
                cur.execute(                "drop table if exists %(tmp_tbl)s;" % self.T)
                df.to_sql(                  self.T['tmp_tbl'],routing_eng)

                # upsert 'tmp' to 'yelp'
                cmd                     =   """

                                            update %(tmp_tbl)s set phone = null where phone::text = 'NaN';
                                            update %(tmp_tbl)s set postal_code = null where postal_code::text = 'NaN';

                                            with upd as (
                                                update yelp y
                                                set
                                                    id = t.id,
                                                    vend_name = t.vend_name,
                                                    phone = t.phone::bigint,
                                                    address = t.address,
                                                    display_address = t.display_address,
                                                    neighborhoods = t.neighborhoods,
                                                    city = t.city,
                                                    state_code = t.state_code,
                                                    postal_code = t.postal_code::bigint,
                                                    display_phone = t.display_phone,
                                                    is_claimed = t.is_claimed,
                                                    is_closed = t.is_closed,
                                                    menu_date_updated = t.menu_date_updated,
                                                    menu_provider = t.menu_provider,
                                                    rating = t.rating,
                                                    review_count = t.review_count,
                                                    categories = t.categories,
                                                    url = t.url,
                                                    latitude = t.latitude,
                                                    longitude = t.longitude,
                                                    geo_accuracy = t.geo_accuracy,
                                                    last_api_update = 'now'::timestamp with time zone
                                                from %(tmp_tbl)s t
                                                where y.id = t.id
                                                returning t.id id
                                            )
                                            insert into yelp (  id,
                                                                vend_name,
                                                                phone,
                                                                address,
                                                                display_address,
                                                                neighborhoods,
                                                                city,
                                                                state_code,
                                                                postal_code,
                                                                display_phone,
                                                                is_claimed,
                                                                is_closed,
                                                                menu_date_updated,
                                                                menu_provider,
                                                                rating,
                                                                review_count,
                                                                categories,
                                                                url,
                                                                latitude,
                                                                longitude,
                                                                geo_accuracy,
                                                                last_api_update
                                                            )
                                            select
                                                t.id,
                                                t.vend_name,
                                                t.phone::bigint,
                                                t.address,
                                                t.display_address,
                                                t.neighborhoods,
                                                t.city,
                                                t.state_code,
                                                t.postal_code::bigint,
                                                t.display_phone,
                                                t.is_claimed,
                                                t.is_closed,
                                                t.menu_date_updated,
                                                t.menu_provider,
                                                t.rating,
                                                t.review_count,
                                                t.categories,
                                                t.url,
                                                t.latitude,
                                                t.longitude,
                                                t.geo_accuracy,
                                                'now'::timestamp with time zone
                                            from
                                                %(tmp_tbl)s t,
                                                (select array_agg(f.id) upd_ids from upd f) as f1
                                            where (not upd_ids && array[t.id]
                                                or upd_ids is null);


                                            drop table %(tmp_table)s;

                                            """ % self.T
                conn.set_isolation_level(   0)
                cur.execute(                cmd)

            if last_run:
                break


        print msg
        SYS_r._growl(                       msg)
        br.quit()
        return
    #   yelp:     2 of 2
    def scrape_yelp_2_vendor_pages(self,query_str=''):
        """
        use yelp.url to get hours from each page and update pgsql
        """
        print self.T['guid']
        def save_comments(br,html,vend_url):
            stop                        =   False
            while stop!=True:
                review_list             =   getTagsByAttr(html, 'div',
                                                      {'class':'review review--with-sidebar'},
                                                      contents=False)
                rev_cols                =   ['vend_url','review_id','review_date','review_rating','review_msg']
                df                      =   pd.DataFrame(columns=rev_cols)
                for rev in review_list:
                    review_id           =   getTagsByAttr(str(rev), 'div',
                                                      {'class':'review review--with-sidebar'},
                                                      contents=False)[0].attrs['data-review-id']
                    review_date         =   getTagsByAttr(str(rev), 'meta',
                                                      {'itemprop':'datePublished'},
                                                      contents=False)[0].attrs['content']

                    dt_review_date      =   dt.datetime.strptime(review_date,'%Y-%m-%d')
                    if (self.T['today'] - dt_review_date).days > self.T['oldest_comments']:
                        stop            =   True
                        break

                    f_review_date       =   dt_review_date.isoformat()
                    review_rating       =   float(getTagsByAttr(str(rev), 'meta',
                                                            {'itemprop':'ratingValue'},
                                                            contents=False)[0].attrs['content'])
                    bs_review_msg       =   getTagsByAttr(str(rev), 'p', {'itemprop':'description'},contents=False)[0]
                    review_msg          =   codecs.encode(bs_review_msg.text,'ascii','ignore')

                    df                  =   df.append(dict(zip(rev_cols,
                                                           [vend_url,review_id,f_review_date,
                                                            review_rating,review_msg])),ignore_index=True)
                try:
                    next_pg_url         =   getTagsByAttr(html, 'a',
                                                      {'class':'page-option prev-next next'},
                                                      contents=False)[0].attrs['href']
                    br.open_page(           next_pg)
                    html                =   codecs.encode(br.source(),'utf8','ignore')
                except:
                    stop                =   True
                    break

            conn.set_isolation_level(       0)
            cur.execute(                    'drop table if exists %(tmp_tbl)s;' % self.T)
            df.to_sql(                      self.T['tmp_tbl'],routing_eng,index=False)
            conn.set_isolation_level(       0)
            cmd                         =   """
                                            insert into customer_comments
                                                (vend_url,
                                                review_id,
                                                review_date,
                                                review_rating,
                                                review_msg)
                                            select t.vend_url,
                                                t.review_id,
                                                t.review_date::timestamp with time zone,
                                                t.review_rating::double precision,
                                                t.review_msg
                                            from
                                                %(tmp_tbl)s t,
                                                (  select array_agg(f.review_id) existing_review_ids
                                                   from customer_comments f  ) as f1
                                            where (not existing_review_ids && array[t.review_id]
                                                    or existing_review_ids is null);

                                            DROP TABLE IF EXISTS %(tmp_tbl)s;
                                            """ % self.T
            cur.execute(                    cmd)
            return

        self.T.update(                      {'tbl_name'         :   'yelp',
                                             'tbl_uid'          :   'uid',
                                             'upd_var'          :   'hours_updated',
                                             'upd_interval'     :   '1 week',
                                             'select_vars'      :   'uid,url'})

        t                               =   """ UPDATE %(tbl_name)s t
                                                    SET checked_out         = null
                                                    WHERE checked_out       = '%(guid)s';

                                                UPDATE %(tbl_name)s t
                                                SET checked_out             =   '%(guid)s'
                                                FROM (
                                                    SELECT array_agg(%(tbl_uid)s) all_ids from %(tbl_name)s t2
                                                    WHERE ( t2.checked_out is null )
                                                    AND (
                                                        t2.%(upd_var)s      is   null
                                                        OR age('now'::timestamp with time zone,
                                                               t2.%(upd_var)s) > interval '%(upd_interval)s'
                                                    )
                                                    GROUP BY t2.%(upd_var)s,t2.%(tbl_uid)s
                                                    ORDER BY t2.%(upd_var)s ASC,t2.%(tbl_uid)s ASC
                                                    LIMIT %(transcation_cnt)s
                                                    ) as f1
                                                WHERE all_ids && array[t.%(tbl_uid)s];

                                                SELECT %(select_vars)s from %(tbl_name)s
                                                WHERE checked_out           =   '%(guid)s';
                                            """ % self.T

        query_str                       =   t if not query_str else query_str
        d                               =   pd.read_sql( query_str,routing_eng )

        y_links                         =   d.url.tolist()
        br                              =   scraper('phantom').browser
        comment_sort_opts               =   '?sort_by=date_desc&start=0'

        for it in y_links:

            br.open_page(                   it+comment_sort_opts)
            html                        =   codecs.encode(br.source(),'utf8','ignore')

            # extract yelp page data
            vend_data                   =   {'url':it}

            # biz info
            try:
                s                       =   getSoup(html).find('h3',text='More business info').find_parent()
                t                       =   s.find('div', {'class':'short-def-list'},contents=False)
                d_keys                  =   map(lambda x: str(x.get_text().strip('\n ')),t.findAll('dt'))
                d_vals                  =   map(lambda x: str(x.get_text().strip('\n ')),t.findAll('dd'))
                d                       =   dict(zip(d_keys,d_vals))
                vend_data.update(           {'extra_info':str(d).replace("'",'"')})
            except:
                vend_data.update(           {'extra_info':None})

            # hours info
            t                           =   getTagsByAttr(html, 'table',
                                                      {'class':'table table-simple hours-table'},
                                                      contents=False)
            if len(t)!=0:
                t                       =   t[0]
                days                    =   map(lambda s: str(s.get_text()),t.findAll('th',attrs={'scope':'row'}))
                hours                   =   map(lambda s: str(s.get_text().strip('\n ')),t.findAll('td',attrs={'class':''}))
                h                       =   str(zip(days,hours)).replace("'",'"')
                vend_data.update(           {'hours':h})
            else:
                vend_data.update(           {'hours':None})

            # biz website
            t                           =   getTagsByAttr(html, 'div',
                                                      {'class':'biz-website'},
                                                      contents=False)
            if len(t)!=0:
                t                       =   t[0].a.attrs['href']
                s                       =   t.find('url=')+4
                e                       =   t.find('&',s)
                biz_website             =   str(unquote(t[s:e]))
                vend_data.update(           {'website':biz_website})
            else:
                vend_data.update(           {'website':None})

            # non-yelp menu link
            t                           =   getTagsByAttr(html, 'a',
                                                      {'class':'i-wrap ig-wrap-common i-external-link-common-wrap ig-wrap-common-r external-menu'},
                                                      contents=False)
            if len(t)!=0:
                t                       =   t[0].attrs['href']
                s                       =   t.find('url=')+4
                biz_menu_page           =   str(unquote(t[s:]))
                vend_data.update(           {'menu_page':biz_menu_page.replace("'","''")})
            else:
                vend_data.update(           {'menu_page':None})

            # price range
            try:
                price_range             =   str(getTagsByAttr(html, 'dd',
                                                          {'class':'nowrap price-description'},
                                                          contents=False)[0].get_text().strip('\n $'))
                vend_data.update(           {'price_range':price_range})
            except:
                vend_data.update(           {'price_range':None})

            # online ordering?
            t                           =   getTagsByAttr(html, 'div',
                                                      {'data-ro-mode-action':'place an order'},
                                                      contents=False) # null return
            online_ordering             =   len(t)!=0
            #t=getTagsByAttr(html, 'div', {'class':'island platform yform js-platform no-js-hidden'},contents=False)
            vend_data.update(               {'online_ordering':online_ordering})

            # push to pgsql
            cmd                         =   """
                                            update yelp set
                                                extra_info                  =   '%(extra_info)s',
                                                hours                       =   '%(hours)s',
                                                hours_updated               =   'now'::timestamp with time zone,
                                                menu_page                   =   '%(menu_page)s',
                                                online_ordering             =   %(online_ordering)s,
                                                price_range                 =   '%(price_range)s',
                                                website                     =   '%(website)s',
                                                checked_out                 =   null
                                            where url                       =   '%(url)s'

                                            """%(vend_data)
            conn.set_isolation_level(       0)
            cur.execute(                    cmd)


            # Save Comments To Separate Table
            self.save_comments(                  br,html,vend_data['url'])


        msg                             =   '%(line_no)s Yelp@%(user)s<%(guid)s>: Known Vendors Updated.' % self.T
        print msg
        SYS_r._growl(                       msg)
        br.quit()
        return True


class Scrape_Functions:

    def __init__(self,_parent):
        self.SV                     =   _parent
        self.T                      =   _parent.T
        self.SF                     =   self

    def consolidate_yelp_urls(self):
        df                              =   pd.read_sql('select url from yelp where url is not null',routing_eng)
        all_urls                        =   df.url.tolist()
        uniq_urls                       =   df.url.unique().tolist()
        if len(all_urls)==len(uniq_urls):
            print "Fully Consolidated"
            return
        df['url_cnt']               =   df.url.map(lambda s: all_urls.count(s))

        ndf                             =   df[df.url_cnt>1].copy()

        self.T.update(                      {'tmp_tbl_2'            :   self.T['tmp_tbl'] + '_2',
                                             'tmp_tbl_3'            :   self.T['tmp_tbl']  + '_3',
                                             'src_tbl'              :   'yelp',
                                             'uid_col'              :   'id',
                                             'partition_col'        :   'url',
                                             'sort_col'             :   'last_api_update',
                                             'sort_order'           :   'DESC'} )
        conn.set_isolation_level(           0)
        cur.execute(                        'drop table if exists %(tmp_tbl)s;' % self.T)
        ndf.to_sql(                         tmp_tbl,routing_eng)

        cmd                             =   """

                                                drop table if exists %(tmp_tbl_2)s;
                                                create table %(tmp_tbl_2)s as (
                                                    select *
                                                    from
                                                        yelp y,
                                                        (select array_agg(t.url) all_urls from %(tmp_tbl)s t) as f1
                                                    where all_urls && array[y.url]
                                                    );

                                                drop table if exists %(tmp_tbl_3)s;
                                                create table %(tmp_tbl_3)s as
                                                        WITH res AS (
                                                            SELECT
                                                                t.%(uid_col)s %(uid_col)s,
                                                                ROW_NUMBER() OVER(PARTITION BY t.%(partition_col)s
                                                                                  ORDER BY %(sort_col)s %(sort_order)s) AS rk
                                                            FROM %(tmp_tbl_2)s t
                                                            )
                                                        SELECT t.*
                                                        FROM
                                                            res s,
                                                            %(tmp_tbl_2)s t
                                                        WHERE s.rk = 1
                                                        and s.%(uid_col)s = t.%(uid_col)s;

                                            """ % self.T
        conn.set_isolation_level(           0)
        cur.execute(                        cmd)

        PGF.Run.make_column_primary_serial_key(self.T['tmp_tbl_3'],'gid',True)

        cmds,table_cols                 =   [],pd.read_sql('select * from %(tmp_tbl_3)s limit 1' % self.T,
                                                           routing_eng).columns.tolist()
        pop_list,src_cols               =   [],pd.read_sql('select * from %(src_tbl)s limit 1' % self.T,
                                                           routing_eng).columns.tolist()
        for it in table_cols:
            self.T.update({'var':it})
            if src_cols.count(it)==0:
                cmds.append(                'alter table %(tmp_tbl_3)s drop column %(var)s;' % self.T)
                pop_list.append(            it)
            else:
                cmd                     =   """ update %(tmp_tbl_3)s t3 set %(var)s = t2.%(var)s
                                                from %(tmp_tbl_2)s t2
                                                where (t3.%(var)s is null or t3.%(var)s::text = 'None'::text)
                                                and not (t2.%(var)s is null or t2.%(var)s::text = 'None'::text);
                                            """ % self.T
                cmds.append(                cmd)
        for it in pop_list:
            if table_cols.count(it):
                z                       =   table_cols.pop(table_cols.index(it))

        self.T.update(                      {  'insert_cols'        :   ','.join(table_cols),
                                               'select_cols'        :   ','.join(['t.'+it for it in table_cols]) })

        conn.set_isolation_level(           0)
        cur.execute(                        '\n'.join(cmds))

        cmd                             =   """

                                                delete from yelp y
                                                using (select array_agg(t.url) all_urls from %(tmp_tbl_3)s t) as f1
                                                where all_urls && array[y.url];

                                                insert into %(src_tbl)s (
                                                    %(insert_cols)s
                                                )
                                                select %(select_cols)s from %(tmp_tbl_3)s t;

                                                drop table if exists %(tmp_tbl_3)s;
                                                drop table if exists %(tmp_tbl_2)s;
                                                drop table if exists %(tmp_tbl)s;

                                            """ % self.T
        conn.set_isolation_level(           0)
        cur.execute(                        cmd)

        cmd                             =   """
                                                select
                                                    all_%(partition_col)s   =   uniq_%(partition_col)s  a,
                                                    all_%(uid_col)s         =   uniq_%(uid_col)s        b,
                                                    uniq_%(partition_col)s  =   uniq_%(uid_col)s        c
                                                from
                                                    (select count(t1.%(partition_col)s) all_%(partition_col)s
                                                        from %(src_tbl)s t1
                                                        where t1.%(partition_col)s is not null) as f1,

                                                    (select count(distinct t2.%(partition_col)s) uniq_%(partition_col)s
                                                        from %(src_tbl)s t2
                                                        where t2.%(partition_col)s is not null) as f2,

                                                    (select count(t3.%(uid_col)s) all_%(uid_col)s
                                                        from %(src_tbl)s t3
                                                        where t3.%(uid_col)s is not null) as f3,

                                                    (select count(distinct t4.%(uid_col)s) uniq_%(uid_col)s
                                                        from %(src_tbl)s t4
                                                        where t4.%(uid_col)s is not null) as f4
                                            """ % self.T
        a,b,c                           =   pd.read_sql(cmd,routing_eng).iloc[0,:]
        assert True == a == b == c == True

    def clean_street_names(self,df,from_label,to_label):

        def remove_non_ascii(text):
            return re_sub(r'[^\x00-\x7F]+',' ', text)

        st_parts                        =   ST_Parts()

        df_ignore                       =   df[df[from_label].map(lambda s: type(s))==NoneType]
        df_ignore_idx                   =   df_ignore.index.tolist()
        if len(df_ignore_idx)>0:
            df                          =   df.ix[df[df.index.isin(df_ignore_idx)==False].index,:]

        df[to_label]                    =   df[from_label].map(lambda s: s.lower().strip())
        df[to_label]                    =   df[to_label].map(remove_non_ascii)

        # st_strip_before
        for k,v in st_parts.ST_STRIP_BEFORE_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: re_sub(k,v,s))

        # st_prefix
        for k,v in st_parts.ST_PREFIX_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: re_sub(r'^('+k+r')\s',v+r' ',s)
                                                if st_parts.ST_SUFFIX_DICT.values().count(
                                                re_sub(r'^('+k+r')\s',v+r' ',s)
                                                ) == 0 else s)

        # st_suffix
        for k,v in st_parts.ST_SUFFIX_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: re_sub(r'\s('+k+r')$'   ,r' '+v,s))

        # st_body
        for k,v in st_parts.ST_BODY_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: re_sub(k,v,s))

        # st_strip_after
        for k,v in st_parts.ST_STRIP_AFTER_DICT.iteritems():
            df[to_label]                =   df[to_label].map(lambda s: re_sub(k,v,s))

        return df.append(                   df_ignore)

    def match_vend_info_by_uniq_vars(self):
        match_var = 'vend_name'

        sl = pd.read_sql("""select vend_id,%(match_var)s,y_vend_id
                            from seamless where %(match_var)s is not null
                            and y_vend_id is null""" % {'match_var':match_var} ,engine)
        y = pd.read_sql(""" select id,%(match_var)s,sl_vend_id
                            from yelp where %(match_var)s is not null
                            and sl_vend_id is null""" % {'match_var':match_var} ,engine)

        all_y_match_var = y[match_var].tolist()
        all_sl_match_var = sl[match_var].tolist()
        match_cnt_col = '%(match_var)s_cnt' % {'match_var':match_var}
        y[match_cnt_col] = y[match_var].map(lambda s: all_y_match_var.count(s))
        sl[match_cnt_col] = sl[match_var].map(lambda s: all_sl_match_var.count(s))

        y_uniq = y[ y[match_cnt_col]==1].copy()
        sl_uniq = sl[ sl[match_cnt_col]==1 ].copy()
        y_match_D = dict(zip(y_uniq[match_var].tolist(),y_uniq.index.tolist()))
        sl_match_D = dict(zip(sl_uniq[match_var].tolist(),sl_uniq.index.tolist()))

        y_f = lambda s: '' if sl_match_D.has_key(s)==False else sl_uniq.ix[sl_match_D[s],'vend_id']
        y_uniq['sl_vend_id'] = y_uniq[match_var].map(y_f)

        sl_f = lambda s: '' if y_match_D.has_key(s)==False else y_uniq.ix[y_match_D[s],'id']
        sl_uniq['y_vend_id'] = sl_uniq[match_var].map(sl_f)
        assert len(sl_uniq[sl_uniq.y_vend_id!=''])==len(y_uniq[y_uniq.sl_vend_id!=''])

        sl_uniq.to_sql(self.T['guid'],engine,index=False)
        conn.set_isolation_level(0)
        cur.execute("""
        update seamless s set y_vend_id=t.y_vend_id
        from %(tmp)s t
        where t.vend_id = s.vend_id
        and not t.y_vend_id='';

        drop table %(tmp)s;

        """ % {'tmp':self.T['guid']} )

        y_uniq.to_sql(self.T['guid'],engine,index=False)
        conn.set_isolation_level(0)
        cur.execute("""
                update yelp y set sl_vend_id=t.sl_vend_id::bigint
                from %(tmp)s t
                where t.id = y.id
                and not t.sl_vend_id='';

                drop table %(tmp)s;

                """ % {'tmp':self.T['guid']} )

        chk="""
        select sl_cnt=y_cnt chk
        from
            (select count(*) sl_cnt from seamless where y_vend_id is not null) as f1,
            (select count(*) y_cnt from yelp where sl_vend_id is not null) as f2
        """
        assert pd.read_sql(chk,engine).chk[0]==True
        return

    def match_distinct_mnv_var(self,tbl='seamless',tbl_id='vend_id',vend_name='vend_name',match_var='vend_name'):
        """
        Matches distinct $tbl variables with distinct mn_vendor vars.

        Usages:

            match_distinct_mnv_var(tbl='yelp',tbl_id='id',vend_name='vend_name',match_var='phone')
            match_distinct_mnv_var(tbl='seamless',tbl_id='vend_id',vend_name='vend_name',match_var='vend_name')
            match_distinct_mnv_var(tbl='yelp',tbl_id='id',vend_name='vend_name',match_var='address')


            match_tables = ['seamless','yelp']
            match_vars = ['vend_name','phone','norm_addr']

            it=match_vars[1]
            match_distinct_mnv_var(tbl='seamless',tbl_id='vend_id',vend_name='vend_name',match_var=it)


        """
        T = {'tbl':tbl,
             'tbl_id':tbl_id,
             'vend_name':vend_name,
             'match_var':match_var}

        x = pd.read_sql("select * from %(tbl)s"%T,engine)

        x_var_tot = x[match_var].tolist()
        x[match_var+'_cnt'] = x[match_var].map(lambda i: x_var_tot.count(i))
        x_var_id_dict = dict(zip(x[x[match_var+'_cnt']==1][match_var].tolist(),x[x[match_var+'_cnt']==1][tbl_id].tolist()))
        x_var_id_dict_keys = x_var_id_dict.keys()

        mnv  = pd.read_sql("select * from mnv where %(tbl)s_id is null"%T,engine)
        mnv_var_tot = mnv[match_var].tolist()
        mnv[match_var+'_cnt'] = mnv[match_var].map(lambda i: mnv_var_tot.count(i))
        mnv_x = mnv[ (mnv[match_var].isin(x_var_id_dict_keys)==True)&(mnv[match_var+'_cnt']==1) ].copy()
        mnv_x['%(tbl)s_id'%T] = mnv_x[match_var].map(x_var_id_dict)

        conn.set_isolation_level(0)
        cur.execute( """drop table if exists tmp;""")
        mnv_x.to_sql('tmp',engine)
        conn.set_isolation_level(0)
        cur.execute("""
            alter table tmp add column tid serial primary key;
            update tmp set tid = nextval(pg_get_serial_sequence('tmp','tid'));
        """)
        conn.set_isolation_level(0)
        cur.execute("""
            update mnv m
            set %(tbl)s_id = t.%(tbl)s_id
            from tmp t
            where m.camis = t.camis;

            drop table tmp;
        """%T)




from sys import argv
if __name__ == '__main__':


    if   len(argv)>1:
        SV                              =   Scrape_Vendors()
        query_str                       =   '' if len(argv)<4 else argv[3]
        msg                             =   ''


        if   argv[1]=='sl':

            if   ['1','search_results'].count(argv[2])>0:
                SV.SL.scrape_sl_1_search_results(query_str)

            elif ['2','prev_closed_v'].count(argv[2])>0:
                SV.SL.scrape_sl_2_previously_closed_vendors(query_str)

            elif ['3','v_pgs'].count(argv[2])>0:
                SV.SL.scrape_sl_3_known_vendor_pages(query_str)

            else:
                msg                     =   'UNKNOWN COMMAND LINE ARGUMENTS'


        elif argv[1]=='y':

            if   ['0','search_results'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_0_search_results(query_str)

            elif ['1','api'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_1_api(query_str)

            elif ['2','v_pgs'].count(argv[2])>0:
                SV.Yelp.scrape_yelp_2_vendor_pages(query_str)

            else:
                msg                     =   'UNKNOWN COMMAND LINE ARGUMENTS'

        else:
            msg                         =   'UNKNOWN COMMAND LINE ARGUMENTS'


        if msg:
            print msg