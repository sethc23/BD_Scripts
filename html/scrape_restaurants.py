# add encoding?
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

# Libraries
import pandas as pd
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
np = pd.np
np.set_printoptions(linewidth=200,threshold=np.nan)
import geopandas as gd
from types import NoneType
from time import sleep as delay
from sqlalchemy import create_engine
from logging import getLogger
from logging import INFO as logging_info
getLogger('sqlalchemy.dialects.postgresql').setLevel(logging_info)
engine = create_engine(r'postgresql://postgres:postgres@192.168.3.52:8800/routing',
                       encoding='utf-8',
                       echo=False)


# import HTML and codecs
from datetime import datetime
from os.path import abspath
fpath = abspath(__file__)
work_dir = abspath(fpath[:fpath.rfind('/')])+'/'
from sys import path as py_path
from HTML_API import getTagsByAttr,getAllTag,getInnerElement,getTagContents
from HTML_API import google,safe_url,getInnerHTML,FindAllTags,getSoup
from webpage_scrape import scraper
import codecs
from time import sleep
import datetime as dt
from urllib import quote_plus,unquote
from re import findall as re_findall
from re import sub as re_sub
py_path.append(abspath(work_dir+'../files_folders'))
from API_system import beep,get_input

import psycopg2
conn = psycopg2.connect("dbname='routing' user='postgres' host='192.168.3.52' password='' port=8800");
cur = conn.cursor()

# SEAMLESS FUNCTIONS
#   seamless: [ base f(x) ]
def update_pgsql_with_seamless_page_content(br):
    html = codecs.encode(br.source(),'utf8','ignore')
    seamless_link = br.get_url()
    if seamless_link.find('http')!=0: seamless_link='http://www.seamless.com/food-delivery/'+seamless_link
    vendor_id = int(seamless_link[seamless_link[:-2].rfind('.')+1:-2])

    t = getTagsByAttr(html, 'span', {'id':'VendorName'},contents=False)
    if len(t)==0:
        try:
            a = getTagsByAttr(html, 'div', {'id':'Bummer'},contents=False)
            b = a[0].text.replace('\n','').replace('Bummer!','').strip()
            vend_name = b[:b.find('(')].strip()
            addr = re_findall(r'[(](.*)[)]',b)[0]
            T = {'vendor_id':vendor_id,'vend_name':vend_name,'addr':addr}
            cmd =   """
                    update seamless
                    set
                        inactive = true,
                        vend_name = %(vend_name)s,
                        address = %(addr)s,
                        upd_vend_content = 'now'::timestamp with time zone
                    where vend_id = %(vendor_id)s
                    """%T
        except:
            T = {'vendor_id':vendor_id}
            cmd =   """
                    update seamless
                    set
                        inactive = true,
                        upd_vend_content = 'now'::timestamp with time zone
                    where vend_id = %(vendor_id)s
                    """%T
        conn.set_isolation_level(0)
        cur.execute(cmd)
    else:
        vend_name = t[0].getText().replace('\n','').strip()

    addr = getTagsByAttr(html, 'span', {'itemprop':'streetAddress'},contents=False)[0].contents[0]
    addr = addr[:addr.find('(')].strip()
    z = getTagsByAttr(html, 'span', {'itemprop':'postalCode'},contents=False)[0].contents[0]

    if z.find('-')!=-1:
        zipcode = int(z[:z.find('-')])
    else:
        zipcode = int(z)
    p = getTagsByAttr(html, 'span', {'itemprop':'telephone'},contents=False)[0].contents[0]
    excl_chars = ['(',')','-','x','/',',',' ']
    for it in excl_chars: p = p.replace(it,'')
    phone = int(p.strip()[:10])
    if len(str(phone))!=10:
        beep()
        raise SystemError()
    try:
        price = int(getTagsByAttr(html, 'span', {'class':'price-text'},contents=False)[0].getText().count('$'))
    except:
        price = -1
    try:
        rating = int(getTagsByAttr(html, 'a', {'class':'user-rating'},contents=False)[0].img.attrs['alt'].split(' ')[0])
        rating_total = int(getTagsByAttr(html, 'span', {'itemprop':'ratingCount',
                                          'id':'TotalRatings'},contents=False)[0].getText().replace('ratings','').strip())
        rating_perc = rating_total/rating
        reviews = int(getTagsByAttr(html, 'span', {'itemprop':'reviewCount',
                                                 'id':'TotalReviews'},contents=False)[0].getText())
    except:
        rating = rating_total = rating_perc = -1
        reviews = 0
    v = html.find('Delivery Estimate:')
    deliv_est = '-'.join(re_findall(r'\d+', html[v:v+len('Delivery Estimate:')+100] ))
    v = html.find('Delivery Minimum:')
    deliv_min = float('.'.join(re_findall(r'\d+', html[v:v+len('Delivery Minimum:')+100] )[:2]))
    pickup_est = '-'.join(re_findall(r'\d+', getTagsByAttr(html, 'span', {'class':'ready-time'},contents=False)[0].getText()))
    v = getTagsByAttr(html, 'div', {'class':'estimates',
                         'id':'RestaurantDetails'},contents=False)[0]
    estimates_blob = re_sub(r'\s+', ' ', v.findAll('span')[3].getText().replace('\n',''))
    description = getTagsByAttr(html, 'meta', {'property':'og:description'},contents=False)[0].attrs['content']
    try:
        cuisine = getTagsByAttr(html, 'li', {'itemprop':'servesCuisine'},contents=False)[0].contents[0]
    except:
        cuisine = None

    page_vars = [seamless_link,vendor_id,vend_name,addr,zipcode,phone,price,
                 rating,rating_total,rating_perc,description,reviews,
                 deliv_est,deliv_min,pickup_est,cuisine,estimates_blob]
    a = 'sl_link,vend_id,vend_name,address,zipcode,phone,price'.split(',')
    b = 'rating,rating_total,rating_perc,description'.split(',')
    c = 'reviews,deliv_est,deliv_min,pickup_est,cuisine,estimates_blob'.split(',')
    var_names = a + b + c
    conn.set_isolation_level(0)
    cur.execute('drop table if exists tmp')
    pd.DataFrame([page_vars],columns=var_names).to_sql('tmp',engine)

    # upsert to seamless
    cmd = """
        with upd as (
            update seamless s
            set
                vend_name = t.vend_name,
                address = t.address,
                zipcode = t.zipcode,
                phone = t.phone,
                price = t.price,
                rating = t.rating,
                rating_total = t.rating_total,
                rating_perc = t.rating_perc,
                description = t.description,
                reviews = t.reviews,
                deliv_est = t.deliv_est,
                deliv_min = t.deliv_min,
                pickup_est = t.pickup_est,
                cuisine = t.cuisine,
                estimates_blob = t.estimates_blob,
                upd_vend_content = 'now'::timestamp with time zone now
            from tmp t
            where s.vend_id = t.vend_id
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
                               upd_vend_content)
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
            'now'::timestamp with time zone now
        from
            tmp t,
            (select array_agg(f.vend_id) upd_vend_ids from upd f) as f1
        where (not upd_vend_ids && array[t.vend_id]
            or upd_vend_ids is null);"""
    conn.set_isolation_level(0)
    cur.execute(cmd)
    conn.set_isolation_level(0)
    cur.execute("drop table tmp;")
    return
#   seamless: 1 of 3
def scrape_sl_search_results():
    """
    get results from seamless address search and update pgsql -- worked 2014.11.16
    """
    def get_sl_addr_search_results(src):

        # br=scraper('firefox').browser
        br=scraper('phantom').browser
        only_delivery=True

        #------------goto main page, identify PDF-page url, goto PDF-page url
        base_url='http://www.seamless.com/food-delivery/'
        url = 'http://www.seamless.com/'
        br.open_page(url)
        br.window.find_element_by_id("fancybox-close").click()

        d = pd.read_sql(src,engine)

        #i=0
        for i in range(len(d)):
            street,zipcode,gid = d.ix[i,['address','zipcode','gid']].astype(str)
            address = street.title() + ', New York, NY, ' + zipcode
            if only_delivery == True: br.window.find_element_by_id("DeliveryOptionSelection").click()
            sleep(10)
            br.window.find_element_by_name("singleAddressEntry").send_keys(address)
            br.window.find_element_by_name("singleAddressEntry").send_keys(u'\ue007')
            sleep(20)
            if br.window.find_element_by_id("MessageArea").text.find('Your exact address could not be located by our system.') != -1:
                br.window.find_element_by_name("singleAddressEntry").clear()
            elif br.window.find_element_by_class_name("error-header").text.find('Your exact address could not be located by our system.') != -1:
                br.window.find_element_by_name("singleAddressEntry").clear()
            elif br.window.find_element_by_class_name("error-header").text.find("We can't find your address.") != -1:
                br.window.find_element_by_id("fancybox-close").click()
                br.window.find_element_by_name("singleAddressEntry").clear()
            else:
                a=br.window.execute_script('return document.body.scrollHeight;')
                br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                b=br.window.execute_script('return document.body.scrollHeight;')
                br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                while a != b:
                    a=br.window.execute_script('return document.body.scrollHeight;')
                    br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(5)
                    b=br.window.execute_script('return document.body.scrollHeight;')
            # --- 2. update pgsql:seamless with address search results
            html = codecs.encode(br.source(),'utf8','ignore')
            z = getTagsByAttr(html, 'div', {'class':'restaurant-name'},contents=False)
            open_res_total = len(z)
            h = pd.Series(map(lambda a: a.a.attrs['href'],z))
            h = h.map(lambda s: base_url + s if s.find('http')==-1 else s)
            t = pd.Series(map(lambda a: a.a.attrs['title'],z))
            conn.set_isolation_level(0)
            cur.execute( """drop table if exists tmp;""")
            pd.DataFrame({'sl_link':h,'search_link_blob':t}).to_sql('tmp',engine)

            conn.set_isolation_level(0)
            cur.execute("""
                alter table tmp add column id serial;
                update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
                alter table tmp add primary key (id);

                alter table tmp add column vend_id bigint;

                update tmp
                set vend_id = substring(sl_link from '[[:punct:]]([[:digit:]]*)[[:punct:]][r]$')::bigint
                where vend_id is null;
                """)
            conn.set_isolation_level(0)
            cur.execute("""
                                with upd as (
                                    update seamless s
                                    set
                                        search_link_blob = t.search_link_blob,
                                        upd_search_links = 'now'::timestamp with time zone
                                    from tmp t
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
                                    tmp t,
                                    (select array_agg(f.vend_id) all_vend_id from seamless f) as f2
                                where not all_vend_id @> array[t.vend_id];

                                drop table if exists tmp;
                            """)
            # --- 3. update pgsql:seamless_closed with seamless address search results
            br.window.find_element_by_id("ShowClosedVendorsLink").click()
            sleep(5)
            html = codecs.encode(br.source(),'utf8','ignore')
            z=getTagsByAttr(html, 'div', {'class':'closed1'},contents=False)
            closed_res_total = len(z)
            tmp = map(lambda a: [a.contents[2].replace('\n','').replace('\t','').strip()]+
                                 a.span.contents[0].lower().replace('\n','').replace('\t','').replace('open','').strip().split('-'),z)
            T = {'day':dt.datetime.strftime(dt.datetime.now(),'%a').lower()}
            cols = str('vend_name,opens_%(day)s,closes_%(day)s'%T).split(',')
            x = pd.DataFrame(tmp,columns=cols)
            x[cols[1]] = x[cols[1]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
            x[cols[2]] = x[cols[2]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
            conn.set_isolation_level(0)
            cur.execute( """drop table if exists tmp;""")
            x.to_sql('tmp',engine)
            conn.set_isolation_level(0)
            cur.execute("""
                alter table tmp add column id serial;
                update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
                alter table tmp add primary key (id);
                """)
            # upsert
            check = pd.read_sql('select count(*) cnt from seamless_closed',engine).cnt[0]
            if check == 0:
                conn.set_isolation_level(0)
                cur.execute("""
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
                                    tmp t;

                                drop table if exists tmp;
                            """%T)
            else:
                conn.set_isolation_level(0)
                cur.execute("""
                                with upd as (
                                    update seamless_closed s
                                    set
                                        opens_%(day)s = t.opens_%(day)s::time with time zone,
                                        closes_%(day)s = t.closes_%(day)s::time with time zone,
                                        last_updated = 'now'::timestamp with time zone
                                    from
                                        tmp t
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
                                    tmp t,
                                    (select array_agg(f.vend_name) all_vend_names from seamless_closed f) as f2
                                where not all_vend_names @> array[t.vend_name];

                                drop table if exists tmp;
                            """%T)
            # --- 4. update pgsql:scrape_lattice
            conn.set_isolation_level(0)
            cur.execute("""  update scrape_lattice
                                set
                                    sl_open_cnt=%s,
                                    sl_closed_cnt=%s,
                                    sl_updated='now'::timestamp with time zone
                            where gid=%s"""%(open_res_total,
                                             closed_res_total,
                                             gid))
            # --- 5. put in new address -- repeat
            addresses=br.window.find_element_by_xpath("//select[@id='Address']")
            last_option=len(addresses.find_elements_by_tag_name('option'))-1
            addresses.find_elements_by_tag_name('option')[last_option].click()
            sleep(8)
        br.quit()

    src = """   select gid,address,zipcode from scrape_lattice
                where address is null
                or sl_updated is null
                or age('now'::timestamp with time zone,seamless_updated) > interval '1 day'
          """

    try:
        get_sl_addr_search_results()
        beep()
        beep()
        print 'done!'
    except:
        beep()
        # br=scraper('firefox').browser
        br=scraper('phantom').browser
        only_delivery=True

        #------------goto main page, identify PDF-page url, goto PDF-page url
        base_url='http://www.seamless.com/food-delivery/'
        url = 'http://www.seamless.com/'
        br.open_page(url)
        br.window.find_element_by_id("fancybox-close").click()

        d = pd.read_sql(src,engine)

        #i=0
        for i in range(len(d)):
            street,zipcode,gid = d.ix[i,['address','zipcode','gid']].astype(str)
            address = street.title() + ', New York, NY, ' + zipcode
            if only_delivery == True: br.window.find_element_by_id("DeliveryOptionSelection").click()
            sleep(10)
            br.window.find_element_by_name("singleAddressEntry").send_keys(address)
            br.window.find_element_by_name("singleAddressEntry").send_keys(u'\ue007')
            sleep(20)
            if br.window.find_element_by_id("MessageArea").text.find('Your exact address could not be located by our system.') != -1:
                br.window.find_element_by_name("singleAddressEntry").clear()
            elif br.window.find_element_by_class_name("error-header").text.find('Your exact address could not be located by our system.') != -1:
                br.window.find_element_by_name("singleAddressEntry").clear()
            elif br.window.find_element_by_class_name("error-header").text.find("We can't find your address.") != -1:
                br.window.find_element_by_id("fancybox-close").click()
                br.window.find_element_by_name("singleAddressEntry").clear()
            else:
                a=br.window.execute_script('return document.body.scrollHeight;')
                br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                b=br.window.execute_script('return document.body.scrollHeight;')
                br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                while a != b:
                    a=br.window.execute_script('return document.body.scrollHeight;')
                    br.window.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(5)
                    b=br.window.execute_script('return document.body.scrollHeight;')
            # --- 2. update pgsql:seamless with address search results
            html = codecs.encode(br.source(),'utf8','ignore')
            z = getTagsByAttr(html, 'div', {'class':'restaurant-name'},contents=False)
            open_res_total = len(z)
            h = pd.Series(map(lambda a: a.a.attrs['href'],z))
            h = h.map(lambda s: base_url + s if s.find('http')==-1 else s)
            t = pd.Series(map(lambda a: a.a.attrs['title'],z))
            conn.set_isolation_level(0)
            cur.execute( """drop table if exists tmp;""")
            pd.DataFrame({'sl_link':h,'search_link_blob':t}).to_sql('tmp',engine)

            conn.set_isolation_level(0)
            cur.execute("""
                alter table tmp add column id serial;
                update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
                alter table tmp add primary key (id);

                alter table tmp add column vend_id bigint;

                update tmp
                set vend_id = substring(sl_link from '[[:punct:]]([[:digit:]]*)[[:punct:]][r]$')::bigint
                where vend_id is null;
                """)
            conn.set_isolation_level(0)
            cur.execute("""
                                with upd as (
                                    update seamless s
                                    set
                                        search_link_blob = t.search_link_blob,
                                        upd_search_links = now
                                    from tmp t
                                    left join (select 'now'::timestamp now) as f1 on true is true
                                    where s.vend_id = t.vend_id
                                    returning s.vend_id vend_id
                                )
                                insert into seamless (
                                    sl_link,
                                    vend_id,
                                    search_link_blob,
                                    upd_search_links
                                    )
                                select t.sl_link,t.vend_id,t.search_link_blob,now
                                from
                                    tmp t,
                                    (select 'now'::timestamp now) as f1,
                                    (select array_agg(f.vend_id) all_vend_id from seamless f) as f2
                                where not all_vend_id @> array[t.vend_id];

                                drop table if exists tmp;
                            """)
            # --- 3. update pgsql:seamless_closed with seamless address search results
            br.window.find_element_by_id("ShowClosedVendorsLink").click()
            sleep(5)
            html = codecs.encode(br.source(),'utf8','ignore')
            z=getTagsByAttr(html, 'div', {'class':'closed1'},contents=False)
            closed_res_total = len(z)
            tmp = map(lambda a: [a.contents[2].replace('\n','').replace('\t','').strip()]+
                                 a.span.contents[0].lower().replace('\n','').replace('\t','').replace('open','').strip().split('-'),z)
            T = {'day':dt.datetime.strftime(dt.datetime.now(),'%a').lower()}
            cols = str('vend_name,opens_%(day)s,closes_%(day)s'%T).split(',')
            x = pd.DataFrame(tmp,columns=cols)
            x[cols[1]] = x[cols[1]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
            x[cols[2]] = x[cols[2]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
            conn.set_isolation_level(0)
            cur.execute( """drop table if exists tmp;""")
            x.to_sql('tmp',engine)
            conn.set_isolation_level(0)
            cur.execute("""
                alter table tmp add column id serial;
                update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
                alter table tmp add primary key (id);
                """)
            # upsert
            check = pd.read_sql('select count(*) cnt from seamless_closed',engine).cnt[0]
            if check == 0:
                conn.set_isolation_level(0)
                cur.execute("""
                                insert into seamless_closed (
                                    vend_name,
                                    opens_%(day)s,
                                    closes_%(day)s,
                                    last_updated )
                                select
                                    t.vend_name,
                                    t.opens_%(day)s::time with time zone,
                                    t.closes_%(day)s::time with time zone,
                                    now
                                from
                                    tmp t,
                                    (select 'now'::timestamp with time zone now) as f1;

                                drop table if exists tmp;
                            """%T)
            else:
                conn.set_isolation_level(0)
                cur.execute("""
                                with upd as (
                                    update seamless_closed s
                                    set
                                        opens_%(day)s = t.opens_%(day)s::time with time zone,
                                        closes_%(day)s = t.closes_%(day)s::time with time zone,
                                        last_updated = now
                                    from
                                        tmp t,
                                        (select 'now'::timestamp now) as f1
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
                                    now
                                from
                                    tmp t,
                                    (select 'now'::timestamp with time zone now) as f1,
                                    (select array_agg(f.vend_name) all_vend_names from seamless_closed f) as f2
                                where not all_vend_names @> array[t.vend_name];

                                drop table if exists tmp;
                            """%T)
            # --- 4. update pgsql:scrape_lattice
            conn.set_isolation_level(0)
            cur.execute("""  update scrape_lattice
                                set
                                    sl_open_cnt=%s,
                                    sl_closed_cnt=%s,
                                    sl_updated='now'::timestamp with time zone
                            where gid=%s"""%(open_res_total,
                                             closed_res_total,
                                             gid))
            # --- 5. put in new address -- repeat
            addresses=br.window.find_element_by_xpath("//select[@id='Address']")
            last_option=len(addresses.find_elements_by_tag_name('option'))-1
            addresses.find_elements_by_tag_name('option')[last_option].click()
            sleep(8)
    return True
#   seamless: 2 of 3
def scrape_previously_closed_vendors():
    """
    get url and html for closed vendors -- worked 2014.11.18
    """

    # new SL vendors not yet added to seamless DB
    cmd =   """
            select vend_name from seamless_closed sc
            where upd_seamless is false
            """
    d = pd.read_sql(cmd,engine)

    x = d.vend_name.tolist()
    base_url='http://www.seamless.com/food-delivery/'

    br=scraper('phantom').browser
    # br=scraper('firefox').browser

    stop=False
    for it in x:
        url='http://www.google.com/search?as_q='+quote_plus(it)+'&as_sitesearch=www.seamless.com&as_occt=any&btnI=1'
        br.open_page(url)
        z=br.get_url()
        if z.find('google')!=-1:
            if z.find('/sorry/') != -1:
                beep()
                end=False
                while end == False:
                    z=get_input("Captcha code?")
                    end=True
            else:
                q=codecs.encode(br.source(),'utf8','ignore')
                a=google()
                url=a.get_results(q)[0].url
                br.open_page(url)  # added this last -- does it work correctly?  NEED TO TEST

        z=url
        if z.find('http')==0: sl_link = z
        else: sl_link = base_url + z

        vendor_id = int(z[z[:-2].rfind('.')+1:-2])
        html = codecs.encode(br.source(),'utf8','ignore')
        try:
            vend_name = getTagsByAttr(html, 'span', {'id':'VendorName'},contents=False)[0].getText().replace('\n','').strip()
            continue_processing = True
        except:
            conn.set_isolation_level(0)
            cur.execute("""
                        update seamless_closed
                        set
                            inactive = true,
                            inactive_on = 'now'::timestamp with time zone,
                            sl_link = '%s'
                        where vend_name ilike concat('%%','%s','%%')"""%(sl_link,it[:it.find("'")]))
            continue_processing = False

        if continue_processing == True:

            if pd.read_sql("""
                    select count(*) c from seamless
                    where vend_id = '%(vend_id)s'
                    """%{'vend_id':vendor_id},engine).c[0] > 0:
                pass

            else:
                try:    br.window.find_element_by_id("fancybox-close").click()
                except: pass

                update_pgsql_with_seamless_page_content(br)

            conn.set_isolation_level(0)
            cur.execute("""
                    update seamless_closed sc
                    set
                        upd_seamless = true,
                        sl_link = '%(sl_link)s'
                    from seamless s
                    where s.vend_id = '%(v_id)s'
                        """%{'v_id':vendor_id,
                            'sl_link':sl_link})

        conn.set_isolation_level(0)
        cur.execute("""
            update seamless_closed sc
            set
                last_updated = 'now'::timestamp with time zone,
                sl_link = '%s'
            where vend_name ilike concat('%%','%s','%%')"""%(sl_link,it[:it.find("'")]))

    print 'done!'
    beep()
    return True
#   seamless: 3 of 3
def scrape_known_sl_vendors():
    d = pd.read_sql(""" select id,sl_link from seamless
                        where upd_vend_content is null
                        or address is null
                        or age('now'::timestamp with time zone,upd_vend_content) > interval '1 day'
                    """,engine)


    sl_links = d.sl_link.tolist()

    br=scraper('phantom').browser
    # br=scraper('firefox').browser

    base_url='http://www.seamless.com/food-delivery/'
    first_link = sl_links[0]
    url=base_url+first_link.replace(base_url,'')
    br.open_page(url)
    try:
        br.window.find_element_by_id("fancybox-close").click()
    except:
        pass
    update_pgsql_with_seamless_page_content(br)
    sleep(5)
    skipped=0
    for it in sl_links[1:]:
        url=base_url+it.replace(base_url,'')
        br.open_page(url)
        try:
            update_pgsql_with_seamless_page_content(br)
        except:
            beep()
            current_url = "'"+br.get_url()+"'"
            conn.set_isolation_level(0)
            cur.execute("update seamless set inactive=true where sl_link = %s"%current_url)
            skipped+=1

    beep()
    beep()
    print skipped,'skipped'
    print 'done!'


# YELP FUNCTIONS
#   yelp:     0 of 2
def scrape_yelp_search_results():
    """
    get results from yelp address search and update pgsql
    """

    import sys
    reload(sys)
    sys.setdefaultencoding('UTF8')

    # s = pd.read_sql(""" select gid,address,zipcode from scrape_lattice
    #                     where yelp_updated is null
    #                     or age('now'::timestamp with time zone,yelp_updated) > interval '1 day'
    #                 """,engine)
    s = pd.read_sql(""" select gid,address,zipcode from scrape_lattice where yelp_updated > '2014-11-24 18:22:59.045361-05'::timestamp with time zone;
                    """,engine)

    p = map(lambda s: str(s[0].title()+', New York, NY '+str(s[1])),zip(s.address,s.zipcode))

    br=scraper('phantom').browser
    #!pkill -f firefox
    # br=scraper('firefox').browser

    d_cols = ['vend_name','url','phone']
    base_url='http://www.yelp.com'
    for i in range(len(p)):
        gid = s.ix[i,'gid']
        search_addr = p[i]

        url = base_url+'/search?find_desc='+safe_url('restaurant')+'&find_loc='+safe_url(search_addr)
        br.open_page(url)

        if getTagsByAttr(br.source(), 'div', {'class':'no-results'},contents=False): pass
        else:
            html = codecs.encode(br.source(),'utf8','ignore')
            if html.find('ylist')==-1:
                res_num = 0
                conn.set_isolation_level(0)
                cur.execute("""  update scrape_lattice
                                    set yelp_cnt=%s,
                                    yelp_updated='now'::timestamp with time zone
                                where gid=%s
                           """%(str(res_num),gid))
            else:
                a = getTagsByAttr(html, 'span', {'class':'pagination-results-window'},contents=True)
                res_num = int(re_findall(r'\d+', str(a[a.find('of')+3:]))[0])
                conn.set_isolation_level(0)
                cur.execute("""  update scrape_lattice
                                    set yelp_cnt=%s,
                                    yelp_updated='now'::timestamp with time zone
                                 where gid=%s
                           """%(str(res_num),gid))
                d = pd.DataFrame(columns=d_cols)
                first_page,last_page = True,False

                while last_page == False:

                    a = getTagsByAttr(html, 'ul', {'class':'ylist ylist-bordered search-results'},contents=False)
                    names = a[0].findAll('a',attrs={'class':'biz-name'})
                    names_proper = map(lambda s: str(s.contents[0]).replace('\xe2\x80\x99',"'")
                                        if len(s.contents)>0 else '',names)
                    links = map(lambda s: base_url+str(s.attrs['href']),names)
                    phones = a[0].findAll('span',attrs={'class':'biz-phone'})
                    phones_proper = map(lambda s: ''.join(re_findall(r'\d+', str(s))),phones)

                    z = {'vend_name':pd.Series(names_proper),
                         'url':pd.Series(links),
                         'phone':pd.Series(phones_proper)}
                    d = d.append(pd.DataFrame(data=z,columns=d_cols),ignore_index=True)

                    next_page = getSoup(html).findAll('a', {'class':'page-option prev-next'})
                    if first_page==True and len(next_page)==1:
                        next_page_link = base_url + next_page[0].attrs['href']
                        br.open_page(next_page_link)
                        html = codecs.encode(br.source(),'utf8','ignore')
                        first_page = False
                    elif len(next_page)==2:
                        next_page_link = base_url + next_page[1].attrs['href']
                        br.open_page(next_page_link)
                        html = codecs.encode(br.source(),'utf8','ignore')
                    else:
                        last_page = True
                        break

                # upsert to yelp
                conn.set_isolation_level(0)
                cur.execute('drop table if exists tmp')
                d['id'] = d.url.map(lambda s: s[s.find('/biz/')+5:])
                d['phone_as_text'] = d.phone.map(str)
                d.to_sql('tmp',engine)

                cmd = """
                    with upd as (
                        update yelp y
                        set
                            id = t.id,
                            vend_name = t.vend_name,
                            url = t.url,
                            phone_as_text = t.phone_as_text,
                            upd_search_links = 'now'::timestamp with time zone
                        from tmp t
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
                        tmp t,
                        (select array_agg(f.url) upd_vend_urls from upd f) as f2
                    where (not upd_vend_urls && array[t.url]
                        or upd_vend_urls is null);"""
                conn.set_isolation_level(0)
                cur.execute(cmd)
                conn.set_isolation_level(0)
                cur.execute("drop table tmp;")

    beep()
    return True
#   yelp:     1 of 2
def scrape_yelp_api():
    """
    get results from yelp Search API with scape lattice addresses and update pgsql -- worked 2014.11.17
    """

    from rauth import OAuth1Session
    from json import dumps as j_dump
    CONSUMER_KEY = 'QzH1O3EktEQt89kegeaUxQ'
    CONSUMER_SECRET = 'Q_GtZiKGtRvqQSTjGOSgsuogkTE'
    TOKEN = '6T7dDEQhf41FA2DIajIDZxsm4RwvBdM9'
    TOKEN_SECRET = 'YNaWq3LCjlQu9ir4Ibo-Zp6ELKI'
    def yelp_search_api(location,radius_in_meters):
        params = {}
        params["term"] = "restaurant"
        params['location'] = location
        params["radius_filter"] = str(radius_in_meters)
        api_url = 'http://api.yelp.com/v2/search'
        return get_results(params,api_url)
    def get_results(params,url):
        session = OAuth1Session(
                    consumer_key = CONSUMER_KEY
                    ,consumer_secret = CONSUMER_SECRET
                    ,access_token = TOKEN
                    ,access_token_secret = TOKEN_SECRET)
        request = session.get(url,params=params)
        data = request.json()
        session.close()
        return data

    s = pd.read_sql(""" select gid,address,zipcode from scrape_lattice
                        where yelp_updated is null
                        or age('now'::timestamp with time zone,yelp_updated) > interval '1 day'
                    """,engine)

    p = map(lambda s: str(s[0].title()+', New York, NY '+str(s[1])),zip(s.address,s.zipcode))

    # (from scrape_lattice creation function) [ADD TO SETTINGS DB]
    pt_buff_in_miles = 0.2
    lattice_table_name = 'scrape_lattice'
    # 1 miles = 1609.34 meters
    radius_in_meters = 1600 * pt_buff_in_miles

    for i in range(len(p)):
        gid = s.ix[i,'gid']
        search_addr = p[i]
        d = yelp_search_api(search_addr,radius_in_meters)
        # try:
        conn.set_isolation_level(0)
        cur.execute("""  update scrape_lattice
                                set yelp_cnt=%s,
                                yelp_updated='now'::timestamp with time zone
                            where gid=%s
                       """%(d['total'],gid))
        df = pd.read_json(j_dump(d['businesses']))

        if len(df)>0:
            all_res_cols = df.columns.tolist()
            df['vend_name'] = df.name
            if all_res_cols.count('phone')>0:
                df['phone'] = df.phone.map(lambda s: int(s) if str(s)[0].isdigit() else None)
            else:
                df['phone'] = None
            df['address'] = df.location.map(lambda s:
                                            None if len(s['address'])==0
                                            else s['address'][0])
            df['display_address'] = df.location.map(lambda s:
                                            None if s.keys().count('display_address')==0
                                            else ','.join(s['display_address']))
            df['neighborhoods'] = df.location.map(lambda s:
                                            None if s.keys().count('neighborhoods')==0
                                            else s['neighborhoods'][0])
            df['city'] = df.location.map(lambda s:
                                         None if s.keys().count('city')==0
                                         else s['city'])
            df['state_code'] = df.location.map(lambda s:
                                               None if s.keys().count('state_code')==0
                                               else s['state_code'])
            df['postal_code'] = df.location.map(lambda s:
                                                None if s.keys().count('postal_code')==0
                                                else int(s['postal_code']))
            df['latitude'] = df.location.map(lambda s:
                                               None if (s.keys().count('coordinate')==0 or
                                                        s['coordinate'].keys().count('latitude')==0)
                                               else s['coordinate']['latitude'])
            df['longitude'] = df.location.map(lambda s:
                                               None if (s.keys().count('coordinate')==0 or
                                                        s['coordinate'].keys().count('longitude')==0)
                                               else s['coordinate']['longitude'])
            df['geo_accuracy'] = df.location.map(lambda s:
                                                 None if s.keys().count('geo_accuracy')==0
                                                 else int(s['geo_accuracy']))
            if df.columns.tolist().count('menu_date_updated')==0:
                df['menu_date_updated'] = None
            else:
                df['menu_date_updated'] = df.menu_date_updated.map(lambda x:
                    None if str(x)[0].isdigit()==False
                    else datetime.fromtimestamp(  int(x)  ).strftime('%Y-%m-%d %H:%M:%S')
                                                                    )
            df = df.ix[:,[   'id',
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

            conn.set_isolation_level(0)
            cur.execute( """drop table if exists tmp;""")
            df.to_sql('tmp',engine)

            conn.set_isolation_level(0)
            cur.execute("""

                alter table tmp add column gid serial primary key;
                update tmp set gid = nextval(pg_get_serial_sequence('tmp','gid'));

                update tmp set phone = null where phone::text = 'NaN';
                update tmp set postal_code = null where postal_code::text = 'NaN';

                """)

            # upsert 'tmp' to 'yelp'
            cmd="""
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
                from tmp t
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
                tmp t,
                (select array_agg(f.id) upd_ids from upd f) as f1
            where (not upd_ids && array[t.id]
                or upd_ids is null);


            drop table tmp;

            """
            conn.set_isolation_level(0)
            cur.execute(cmd)

    print 'done!'
    beep()
#   yelp:     2 of 2
def scrape_yelp_vendor_pages():
    """
    use yelp.url to get hours from each page and update pgsql
    """

    d = pd.read_sql(""" select gid,url from yelp
                        where hours_updated is null
                        or age(hours_updated,'now'::timestamp with time zone) > interval '1 day'
                    """,engine)

    y_links = d.url.tolist()
    br=scraper('phantom').browser
    # br=scraper('firefox').browser

    for it in y_links:
        br.open_page(it)
        html = codecs.encode(br.source(),'utf8','ignore')

        # extract yelp page data
        vend_data = {'url':it}

        # biz info
        try:
            s=getSoup(html).find('h3',text='More business info').find_parent()
            t=s.find('div', {'class':'short-def-list'},contents=False)
            d_keys=map(lambda x: str(x.get_text().strip('\n ')),t.findAll('dt'))
            d_vals=map(lambda x: str(x.get_text().strip('\n ')),t.findAll('dd'))
            d = dict(zip(d_keys,d_vals))
            vend_data.update({'extra_info':str(d).replace("'",'"')})
        except:
            vend_data.update({'extra_info':None})

        # hours info
        t=getTagsByAttr(html, 'table', {'class':'table table-simple hours-table'},contents=False)
        if len(t)!=0:
            t=t[0]
            days = map(lambda s: str(s.get_text()),t.findAll('th',attrs={'scope':'row'}))
            hours = map(lambda s: str(s.get_text().strip('\n ')),t.findAll('td',attrs={'class':''}))
            h = str(zip(days,hours)).replace("'",'"')
            vend_data.update({'hours':h})
        else:
            vend_data.update({'hours':None})

        # biz website
        t=getTagsByAttr(html, 'div', {'class':'biz-website'},contents=False)
        if len(t)!=0:
            t = t[0].a.attrs['href']
            s =t.find('url=')+4
            e = t.find('&',s)
            biz_website = str(unquote(t[s:e]))
            vend_data.update({'website':biz_website})
        else:
            vend_data.update({'website':None})

        # non-yelp menu link
        t=getTagsByAttr(html, 'a', {'class':'i-wrap ig-wrap-common i-external-link-common-wrap ig-wrap-common-r external-menu'},contents=False)
        if len(t)!=0:
            t = t[0].attrs['href']
            s = t.find('url=')+4
            biz_menu_page = str(unquote(t[s:]))
            vend_data.update({'menu_page':biz_menu_page.replace("'","''")})
        else:
            vend_data.update({'menu_page':None})

        # price range
        try:
            price_range = str(getTagsByAttr(html, 'dd', {'class':'nowrap price-description'},contents=False)[0].get_text().strip('\n $'))
            vend_data.update({'price_range':price_range})
        except:
            vend_data.update({'price_range':None})

        # online ordering?
        t=getTagsByAttr(html, 'div', {'data-ro-mode-action':'place an order'},contents=False) # null return
        online_ordering = len(t)!=0
        #t=getTagsByAttr(html, 'div', {'class':'island platform yform js-platform no-js-hidden'},contents=False)
        vend_data.update({'online_ordering':online_ordering})

        # push to pgsql
        cmd =   """
                update yelp set
                    extra_info = '%(extra_info)s',
                    hours = '%(hours)s',
                    hours_updated = 'now'::timestamp with time zone,
                    menu_page = '%(menu_page)s',
                    online_ordering=%(online_ordering)s,
                    price_range='%(price_range)s',
                    website = '%(website)s'
                where url = '%(url)s'

                """%(vend_data)
        conn.set_isolation_level(0)
        cur.execute(cmd)

    print 'done!'
    beep()
    return True

from sys import argv
if __name__ == '__main__':
    if   argv[1]=='yelp0':            scrape_yelp_search_results()