
from time import time,sleep
import datetime as dt
import pandas as pd
pd.set_option('expand_frame_repr',False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width',180)
np = pd.np
np.set_printoptions(linewidth=200,threshold=np.nan)
from sqlalchemy import create_engine
# from logging import getLogger
# from logging import INFO as logging_info
# getLogger('sqlalchemy.dialects.postgresql').setLevel(logging_info)
engine = create_engine(r'postgresql://postgres:postgres@192.168.2.50:8800/routing',
                       encoding='utf-8',
                       echo=False)
from sys import argv
import sys
import codecs
reload(sys)
sys.setdefaultencoding('UTF8')
from re import findall as re_findall
from re import sub as re_sub

from os import getcwd
workDir = getcwd()+'/'
from os.path import abspath
from sys import path as py_path
# py_path.append(abspath(workDir+'/..'))
# import embed_ipython as I; I.embed()
py_path.append(abspath(workDir+'/../../../html'))
from HTML_API import getTagsByAttr,getAllTag,getInnerElement,getTagContents
from HTML_API import google,safe_url,getInnerHTML
from webpage_scrape import scraper
py_path.append(abspath(workDir+'/../../../files_folders'))
from API_system import beep,get_input

def get_vendor_links_on_seamless():
    br=scraper('firefox').browser
    url = 'http://www.seamless.com/'
    br.open_page(url)
    br.window.find_element_by_id("fancybox-close").click()

    # TODO:  when searching addresses, the update should include scrape_lattice.gid

    d = pd.read_sql('select address,zipcode from scrape_lattice',engine)
    for i in range(len(d)):
        street,zipcode = d.ix[i,:].astype(str)
        address = street.title() + ', New York, NY, ' + zipcode
        br.window.find_element_by_id("DeliveryOptionSelection").click()
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

        # 2 update pgsql with seamless address search results
        html = codecs.encode(br.source(),'utf8','ignore')
        z=getTagsByAttr(html, 'div', {'class':'restaurant-name'},contents=False)
        h = pd.Series(map(lambda a: a.a.attrs['href'],z))
        t = pd.Series(map(lambda a: a.a.attrs['title'],z))
        engine.execute( """drop table if exists tmp;""")
        pd.DataFrame({'seamless_link':h,'search_link_blob':t}).to_sql('tmp',engine)
        engine.execute("""
            alter table tmp add column id serial;
            update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
            alter table tmp add primary key (id);
            """)
        engine.execute("""
                            with upd as (
                                update seamless s
                                set
                                    search_link_blob = t.search_link_blob,
                                    updated_links = now
                                from tmp t
                                left join (select 'now'::timestamp now) as f1 on true is true
                                where s.seamless_link = t.seamless_link
                                returning s.seamless_link seamless_link
                            )
                            insert into seamless (  seamless_link,
                                        search_link_blob,
                                        updated_links )
                            select t.seamless_link,t.search_link_blob,now
                            from
                                tmp t,
                                (select 'now'::timestamp now) as f1,
                                (select array_agg(f.seamless_link) all_seamless_links from seamless f) as f2
                            where not all_seamless_links @> array[t.seamless_link];

                            drop table if exists tmp;
                        """)

        # 3 update pgsql:seamless_closed with seamless address search results
        br.window.find_element_by_id("ShowClosedVendorsLink").click()
        sleep(5)
        html = codecs.encode(br.source(),'utf8','ignore')
        z=getTagsByAttr(html, 'div', {'class':'closed1'},contents=False)
        tmp = map(lambda a: [a.contents[2].replace('\n','').replace('\t','').strip()]+
                             a.span.contents[0].lower().replace('\n','').replace('\t','').replace('open','').strip().split('-'),z)
        T = {'day':dt.datetime.strftime(dt.datetime.now(),'%a').lower()}
        cols = str('vend_name,opens_%(day)s,closes_%(day)s'%T).split(',')
        x = pd.DataFrame(tmp,columns=cols)
        x[cols[1]] = x[cols[1]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
        x[cols[2]] = x[cols[2]].map(lambda s: dt.datetime.strftime(dt.datetime.strptime(s,'%I:%M %p'),'%H:%M'))
        engine.execute( """drop table if exists tmp;""")
        x.to_sql('tmp',engine)
        engine.execute("""
            alter table tmp add column id serial;
            update tmp set id = nextval(pg_get_serial_sequence('tmp','id'));
            alter table tmp add primary key (id);
            """)
        # upsert
        check = pd.read_sql('select count(*) cnt from seamless_closed',engine).cnt[0]
        if check == 0:
            engine.execute("""
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
            engine.execute("""
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
        # put in new address -- repeat
        addresses=br.window.find_element_by_xpath("//select[@id='Address']")
        last_option=len(addresses.find_elements_by_tag_name('option'))-1
        addresses.find_elements_by_tag_name('option')[last_option].click()
        sleep(8)
    br.quit()
def get_vendor_page_content_on_seamless():
    from urllib import quote_plus
    import psycopg2
    conn = psycopg2.connect("dbname='routing' user='postgres' host='192.168.2.50' password='' port=8800");
    cur = conn.cursor()


    def update_pgsql_with_seamless_page_content(br):
        html=br.source()

        # get:  seamless_link,vendor_id,vend_name,addr,zipcode,phone,price,
        #       rating,rating_total,rating_perc,reviews,
        #       deliv_est,deliv_min,pickup_est,cuisine

        seamless_link = br.get_url()
        vendor_id = int(seamless_link[seamless_link[:-2].rfind('.')+1:-2])
        try:
            vend_name = getTagsByAttr(html, 'span', {'id':'VendorName'},contents=False)[0].getText().replace('\n','').strip()
        except:
            conn.set_isolation_level(0)
            cur.execute("""
                        update seamless
                        set
                        inactive = true,
                        upd_vend_content = 'now'::timestamp with time zone
                        where vend_id = %s"""%vendor_id)
            return
        addr = getTagsByAttr(html, 'span', {'itemprop':'streetAddress'},contents=False)[0].contents[0]
        addr = addr[:addr.find('(')].strip()
        zipcode = int(getTagsByAttr(html, 'span', {'itemprop':'postalCode'},contents=False)[0].contents[0])
        phone = getTagsByAttr(html, 'span', {'itemprop':'telephone'},contents=False)[0].contents[0]
        phone = int(phone[:10].strip().replace('(','').replace(')','').replace('-','').replace(' ',''))
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
                    upd_vend_content = now
                from tmp t
                left join (select 'now'::timestamp with time zone now) as f1 on true is true
                where s.vend_id = t.vend_id
                returning t.vend_id vend_id
            )
            insert into seamless ( sl_link,
                                   vend_id,
                                   sl_vend_name,
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
                now
            from
                tmp t,
                (select 'now'::timestamp with time zone now) as f1,
                (select array_agg(f.vend_id) upd_vend_ids from upd f) as f2
            where (not upd_vend_ids && array[t.vend_id]
                or upd_vend_ids is null);"""
        conn.set_isolation_level(0)
        cur.execute(cmd)
        conn.set_isolation_level(0)
        cur.execute("""drop table tmp;""")
        return

    def get_open_vendor_pages(sl_links):
        br=scraper('firefox').browser
        base_url='http://www.seamless.com/food-delivery/'
        first_link = sl_links[0]
        url=base_url+first_link.replace(base_url,'')
        br.open_page(url)
        br.window.find_element_by_id("fancybox-close").click()
        update_pgsql_with_seamless_page_content(br)
        sleep(5)
        for it in sl_links[1:]:
            url=base_url+it.replace(base_url,'')
            br.open_page(url)
            update_pgsql_with_seamless_page_content(br)

    def get_closed_vendor_pages(x):
        stop=False
        if type(x)!=list: x=[x]
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
                    z=br.get_url()
                else:
                    q=br.source()
                    a=google()
                    url=a.get_results(q)[0].url
                    br.open_page(url)
                    z=br.get_url()
            vendor_id = int(z[z[:-2].rfind('.')+1:-2])
            if pd.read_sql("""
                    select count(*) c from seamless
                    where vend_id = '%(v_id)s'
                    """%{'v_id':vendor_id},engine).c[0] > 0:
                conn.set_isolation_level(0)
                cur.execute("""
                        update seamless_closed sc
                        set upd_seamless = true
                        from seamless s
                        where s.sl_vend_name ilike sc.vend_name
                        and s.vend_id = '%(v_id)s'
                            """%{'v_id':vendor_id})
            else:
                try: br.window.find_element_by_id("fancybox-close").click()
                except: pass
                update_pgsql_with_seamless_page_content(br)


    br=scraper('firefox').browser
    #br=scraper('phantom').browser

    #d = pd.read_sql('select id,seamless_link,seamless_vendor_name vend_name from seamless',engine)
    #get_open_vendor_pages(d)

    # A. scrape all closed vendors already existing in seamless (should reverse and use urls...)
    # d = pd.read_sql("""
    #                     select vend_name from seamless_closed sc
    #                     inner join seamless s
    #                     on s.sl_vend_name = sc.vend_name
    #                     where s.sl_vend_name = sc.vend_name
    #                     and s.upd_vend_content is null
    #                     and sc.upd_seamless is false
    #                     """,engine)
    # tmp = d.vend_name.map(lambda x: get_closed_vendor_pages(x))

    # B. scrape all known vendor urls (not already updated)
    d = pd.read_sql("""
                        select sl_link from seamless
                        where upd_vend_content is null
                        """,engine)
    tmp = d.sl_link.map(lambda x: get_open_vendor_pages(x))

    # C. scrape remaining closed/unknown vendors

    br.quit()


def get_yelp_data(openFile='yelp-info.txt',
                  saveFile='yelp'):
    openPath    = workDir+openFile
    savePath    = workDir+saveFile
    f           = open(openPath,'r')
    x           = f.read()
    f.close()
    x           = x.split('\r')

    vendor,searchFind,searchNear=[],[],[]
    for it in x:
        a,b,c   = it.split('\t')
        #if (str(vendorIDs)!='' and vendorIDs.count(a)!=0) or str(vendorIDs)=='':
        vendor.append(a)
        searchFind.append(b)
        searchNear.append(c)

    base='http://www.yelp.com'
    for i in range(0,len(vendor)):
        br=scraper('phantom').browser
        # br=scraper('firefox').browser
        url=base+'/search?find_desc='+safe_url(searchFind[i])+'&find_loc='+safe_url(searchNear[i]+', New York, NY')
        br.open_page(url)

        if getTagsByAttr(br.source(), 'div', {'class':'no-results'},contents=False): pass
        else:

            a=getTagsByAttr(br.source(), 'ul', {'class':'ylist ylist-bordered search-results'},contents=False)
            try:
                b=a[0].li.a['href']
            except:
                print a
                print br.get_url()
                br.screenshot()
                b=a[0].li.a['href']
            br.open_page(base+b)

            f=open(savePath+'/'+vendor[i]+'.html','w')
            f.write(br.source().encode('utf8'))
            f.close()
            sleep(5)

def get_yelp_vendor_info_from_vendor_pages(vendorIDs,workDir='/Users/admin/Desktop/vendor_data/yelp/set1',
                                      savePath='/Users/admin/Desktop/seamless/vendor_info.txt',
                                      set=1):

    # TODO: need to error check these results
    if vendorIDs[0].find('.html')==-1:
        for i in range(0,len(vendorIDs)):
            vendorIDs[i] = vendorIDs[i]+'.html'
    s='vendor\thours'
    D = {'Mon':0,
         'Tue':1,
         'Wed':2,
         'Thu':3,
         'Fri':4,
         'Sat':5,
         'Sun':6,
         }
    Dkeys = D.keys()

    def set2(a,b):
        totalHours,hrInfo = 0,[]
        for hr in a:
            day = hr.th.contents[0]
            c=hr.findAll('span')
            d=str(hr.findAll('td')[0].contents[0].replace('\n','').strip())
            if d=='Open 24 hours':
                totalHours += 24
                hrInfo.append(str(hr.th.contents[0])+' 24 hr.')
            elif len(c)==0: pass
            else:
                s_hr,s_am_pm = c[0].contents[0].split(' ')
                e_hr,e_am_pm = c[1].contents[0].split(' ')
                hrsInfo = day+' '+c[0].contents[0]+' to '+c[1].contents[0]

                if s_hr.find(":")!=-1:
                    h,m=s_hr.split(':')
                    s_hr = eval(h)+round((eval(m)/60.0),2)
                    if s_am_pm.strip() == 'pm':
                        if eval(str(s_hr)[:str(s_hr).find('.')])!=12: s_hr+=12
                else:
                    if s_am_pm.strip() == 'pm' and eval(s_hr)!=12: s_hr = eval(s_hr)+12
                    else: s_hr = eval(s_hr)

                if e_hr.find(":")!=-1:
                    h,m=e_hr.split(':')
                    e_hr = eval(h)+round((eval(m)/60.0),2)
                    if e_am_pm.strip() == 'pm':
                        if eval(str(e_hr)[:str(e_hr).find('.')])!=12: e_hr+=12
                else:
                    if e_am_pm.strip() == 'pm' and eval(e_hr)!=12: e_hr = eval(e_hr)+12
                    else: e_hr = eval(e_hr)

                hrs = e_hr-s_hr
                if hrs<0:
                    if s_hr<12 and e_hr<12:
                        hrs += 24
                    elif s_hr>=12 and e_hr<12:
                        hrs = (24-s_hr) + e_hr
                    elif s_hr==24 and e_hr==0:
                        hrs = 24
                        print vendorIDs.index(it),'check below'
                    elif s_hr>=12 and e_hr == 12:
                        hrs = 24 - s_hr
                    else:
                        print vendorIDs.index(it),'help here'
                elif hrs==0:
                    hrs = 12
                totalHours += hrs
                hrInfo.append(hrsInfo)
        return totalHours,hrInfo

    def set1(a,b):
        totalHours,hrInfo = 0,[]
        for hr in a:

            info = hr.contents[0]
            for i in range(0,len(info)):
                if info[i].isdigit()==True:
                    day_s,hr_s = info[:i-1],info[i:]
                    break

            days=0
            if day_s.find('-')!=-1 and day_s.find(',')!=-1:
                day_s = day_s[:day_s.find(',')]
                days += 1
                day_s = day_s.replace('-','\t')
                items = day_s.split('\t')
                for col in items:
                    _col = col.strip()
                    if Dkeys.count(_col)!=0:
                        day_s=day_s.replace(_col,str(D[_col]))
                n = day_s.split('\t')
                days += (eval(str(n[1]))+1)-eval(str(n[0]))

            elif day_s.find('-')!=-1:
                day_s = day_s.replace('-','\t')
                items = day_s.split('\t')
                for col in items:
                    _col = col.strip()
                    if Dkeys.count(_col)!=0:
                        day_s=day_s.replace(_col,str(D[_col]))
                n = day_s.split('\t')
                days += (eval(str(n[1]))+1)-eval(str(n[0]))

            elif day_s.find(',')!=-1:
                day_s = day_s.replace(',','\t')
                items = day_s.split('\t')
                for col in items:
                    _col = col.strip()
                    if Dkeys.count(_col)!=0:
                        day_s=day_s.replace(_col,str(D[_col]))
                if days==0: days = 2
                else: days+=1

            elif len(day_s)==3:
                days = 1


            hrs_split = hr_s.strip().split('-')
            s_hr,s_am_pm=hrs_split[0].strip().split(' ')
            e_hr,e_am_pm=hrs_split[1].strip().split(' ')
            if s_hr.find(":")!=-1:
                h,m=s_hr.split(':')
                s_hr = eval(h)+round((eval(m)/60.0),2)
                if s_am_pm.strip() == 'pm':
                    if eval(str(s_hr)[:str(s_hr).find('.')])!=12: s_hr+=12
            else:
                if s_am_pm.strip() == 'pm' and eval(s_hr)!=12: s_hr = eval(s_hr)+12
                else: s_hr = eval(s_hr)

            if e_hr.find(":")!=-1:
                h,m=e_hr.split(':')
                e_hr = eval(h)+round((eval(m)/60.0),2)
                if e_am_pm.strip() == 'pm':
                    if eval(str(e_hr)[:str(e_hr).find('.')])!=12: e_hr+=12
            else:
                if e_am_pm.strip() == 'pm' and eval(e_hr)!=12: e_hr = eval(e_hr)+12
                else: e_hr = eval(e_hr)

            hrs = e_hr-s_hr
            if hrs<0:
                if s_hr<12 and e_hr<12:
                    hrs += 24
                elif s_hr>=12 and e_hr<12:
                    hrs = (24-s_hr) + e_hr
                elif s_hr==24 and e_hr==0:
                    hrs = 24
                    print vendorIDs.index(it),'check below'
                elif s_hr>=12 and e_hr == 12:
                    hrs = 24 - s_hr
                else:
                    print vendorIDs.index(it),'help here'
            elif hrs==0:
                hrs = 12
            totalHours += days*hrs
            hrInfo.append(hr.contents[0])

        return totalHours,hrInfo

    skipped=[]
    for it in vendorIDs:
        s+=it[:-5]+'\t'
        # try:
        # f=codecs.open(workDir+'/'+it+'.html','r','utf-8')
        f=codecs.open(workDir+'/'+it,'r','utf-8')
        html=f.read()
        f.close()
        if html.find('Redirecting...')!=-1:
            print 'redirected\t'+str(vendorIDs.index(it))+'\t'+it
            skipped.append(it)
        else:
            if set==1:
                c=getTagsByAttr(html, 'dd', {'class':'attr-BusinessHours'},contents=False)
                if len(c)!=0:
                    a = c[0].findAll('p')
                    b = getTagsByAttr(html, 'h1', {'itemprop':'name'},contents=False)[0].contents[0].strip('\n\t')
                    totalHours,hrInfo = set1(a,b)
                    new=str(vendorIDs.index(it))+'\t'+it.replace('.html','')+'\t'+b+'\t'+str(totalHours)+'\t'+str(hrInfo)
                    s+=new
                    print new
                else:
                    print 'skipped\t'+str(vendorIDs.index(it))+'\t'+it
                    skipped.append(it)
            elif set==2:
                c=getTagsByAttr(html, 'table', {'class':'table table-simple hours-table'},contents=False)
                if len(c)!=0:
                    a = c[0].findAll('tr')
                    b = getTagsByAttr(html, 'h1', {'itemprop':'name'},contents=False)[0].contents[0].strip('\n').strip()
                    totalHours,hrInfo = set2(a,b)
                    new=str(vendorIDs.index(it))+'\t'+it.replace('.html','')+'\t'+b+'\t'+str(totalHours)+'\t'+str(hrInfo)
                    s+=new
                    print new
                else:
                    print 'hours not provided\t'+str(vendorIDs.index(it))+'\t'+it
                    skipped.append(it)

    f=open(savePath,'w')
    f.write(s)
    f.close()
    return skipped
def get_vendor_info_from_vendor_pages(workDir='/Users/admin/Desktop/seamless/vendor_pages',
                                      savePath='/Users/admin/Desktop/seamless/vendor_info.txt'):
    path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
    from API_system import getFilesFolders
    x=getFilesFolders(workDir,full=False)

    s='vendor\taddress\tphone\r'
    #it=x[0]
    for it in x:
        s+=it[:-5]+'\t'
        f=codecs.open(workDir+'/'+it,'r','utf-8')
        html=f.read()
        f.close()
        try:
            s+=getTagsByAttr(html, 'span', {'itemprop':'name'},contents=False)[0].contents[0].replace('\r','').strip()+'\t'
            s+=getTagsByAttr(html, 'span', {'itemprop':'streetAddress'},contents=False)[0].contents[0].strip()+'\t'
            s+=getTagsByAttr(html, 'span', {'itemprop':'telephone'},contents=False)[0].contents[0].strip()+'\r'
        except:
            s+='error\terror\terror\r'

    f=open(savePath,'w')
    f.write(s)
    f.close()
def get_yelp_vendor_info_from_vendor_pages_set2(vendorIDs,workDir='/Users/admin/Desktop/vendor_data/yelp/',
                                      savePath='/Users/admin/Desktop/seamless/vendor_info.txt'):

    if vendorIDs[0].find('.html')==-1:
        for i in range(0,len(vendorIDs)):
            vendorIDs[i] = vendorIDs[i]+'.html'
    s='vendor\thours'
    #it=x[0]
    for it in vendorIDs:
        s+=it[:-5]+'\t'
        # try:
            # f=codecs.open(workDir+'/'+it+'.html','r','utf-8')
        f=codecs.open(workDir+'/'+it,'r','utf-8')
        html=f.read()
        f.close()
        try:
            a = getTagsByAttr(html, 'table', {'class':'table table-simple hours-table'},contents=False)[0].findAll('tr')
            b = getTagsByAttr(html, 'h1', {'itemprop':'name'},contents=False)[0].contents[0].strip('\n').strip()
            for hr in a:
                new=it[:-5]+'\t'+b+'\t'+hr.th.contents[0]+'\t'+str(hr.findAll('span')[0].contents[0])+'\t'+str(hr.findAll('span')[1].contents[0])
                # new=it+'\t'+hr.contents[0]
                s+=new
                print new
                    # s+=getTagsByAttr(html, 'span', {'itemprop':'name'},contents=False)[0].contents[0].replace('\r','').strip()+'\t'
                    # s+=getTagsByAttr(html, 'span', {'itemprop':'streetAddress'},contents=False)[0].contents[0].strip()+'\t'
                    # s+=getTagsByAttr(html, 'span', {'itemprop':'telephone'},contents=False)[0].contents[0].strip()+'\r'
                # except:
                #     s+='error\terror\t'
        except:
            print 'missing file\t'+it

    f=open(savePath,'w')
    f.write(s)
    f.close()

def scrape_seamless():
    f=open('/Users/admin/Desktop/NYC-addresses.txt','r')
    x=f.read()
    f.close()
    addresses=x.split('\r')
    get_restaurants(addresses,delivery=True)

def get_open_vendor_data(htmlFiles):
    vendors=[]
    name_d,hours_d,address_d,price_d=[],[],[],[]
    rating_d,reviews_d,deliveryTime_d,deliveryMinimum_d=[],[],[],[]
    distance_d,block_id_d=[],[]

    f=open('/Users/admin/Desktop/nyc.txt','r')
    x=f.read()
    f.close()
    y=x.split('\r')
    ids,adds=[],[]
    for it in y:
        ids.append(it.split('\t')[0])
        adds.append(it.split('\t')[1])

    for htmlFilePath in htmlFiles:
        filename=htmlFilePath[htmlFilePath.rfind('/'):-5].replace('/open-','')
        block_id=ids[adds.index(filename)]
        f=codecs.open(htmlFilePath,'r','utf-8')
        html=f.read()
        f.close()
        t=getTagsByAttr(html, 'table', { 'id':'VendorsTable'})
        table=[]
        t_header=getAllTag(t, 'thead')[0]
        t_header_col=getAllTag(t_header, 'th')
        row=[]
        for it in t_header_col:
            row.append(getInnerElement(it, 'a','title'))
        table.append(row)
        t_body=getAllTag(t, 'tbody')[0]
        t_body_rows=getAllTag(t_body, 'tr')
        #save html table to python list
        for it in t_body_rows:
            row=[]
            r=getAllTag(it, 'td')
            for col in r:
                row.append(col)
            table.append(row)
        #print s
        for i in range(1,len(table)-1): # picture column
            #process by columns
            #------
            it=table[i][1]
            vend_link = getInnerElement(table[i][1], 'a','href')
            a=getInnerElement(it, 'a','title')
            name=a[:a.find('|')]
            hours=getAllTag(a, 'em')[0]
            address=getAllTag(it, 'p')[0].strip()
            #------
            it=table[i][2]
            price=it.count('$')
            #------
            it=table[i][3]
            if it.find('Too Few') != -1: rating,reviews=0,0
            else:
                a=getAllTag(it, 'a')[0]
                b=getInnerElement(a, 'img','src')
                rating=b.replace('img/rating','').replace('.png','')
                a=getAllTag(it, 'a')[1]
                reviews=getTagContents(a, 'p','text')[0].strip('()')
            #------
            it=table[i][5]
            if it.find('mins') != -1:
                deliveryTime=it.replace('mins','')
                deliveryTime=deliveryTime.strip()+' mins'
            else: deliveryTime=it.strip()
            #------
            it=table[i][6]
            deliveryMinimum=it.strip()
            #------
            it=table[i][7]
            distance=it.strip()
            #------
            if vendors.count(vend_link) != 0:
                d_index=vendors.index(vend_link)
                # max distance
                if eval(distance_d[d_index].replace('mi','').strip())<eval(distance.replace('mi','').strip()):
                    distance_d[d_index]=distance
                # supp blocks
                a=block_id_d[d_index]
                a.append(block_id)
                block_id_d[d_index]=a
            elif vendors.count(vend_link) == 0:
                vendors.append(vend_link)
                name_d.append(name)
                hours_d.append(hours)
                address_d.append(address)
                price_d.append(price)
                rating_d.append(rating)
                reviews_d.append(reviews)
                deliveryTime_d.append(deliveryTime)
                deliveryMinimum_d.append(str(deliveryMinimum))
                distance_d.append(distance)
                block_id_d.append([block_id])

    open_data=[vendors,
                 name_d,
                 hours_d,
                 address_d,
                 price_d,
                 rating_d,
                 reviews_d,
                 deliveryTime_d,
                 deliveryMinimum_d,
                 distance_d,
                 block_id_d]
    s= ('vend_link'+'\t'+
       'name'+'\t'+
       'hours'+'\t'+
       'address'+'\t'+
       'price'+'\t'+
       'rating'+'\t'+
       'reviews'+'\t'+
       'deliveryTime'+'\t'+
       'deliveryMinimum'+'\t'+
       'distance'+'\t'+
       'id #')+'\r'
    for i in range(0,len(vendors)):
        t=''
        for j in range(0,len(open_data)):
            t+=str(open_data[j][i])+'\t'
        s+=t+'\r'

    f=open('/Users/admin/Desktop/open_vendors2.txt','w')
    f.write(s)
    f.close()

def get_closed_vendor_data(htmlFiles):
    closed_data,vendors=[],[]
    sf=open('/Users/admin/Desktop/closed_vendors.txt','w')
    sf.writelines('name'+'\t'+'hours'+'\r')
    for htmlFilePath in htmlFiles:
        f=codecs.open(htmlFilePath,'r','utf-8')
        html=f.read()
        f.close()
        div=getTagsByAttr(html, 'div', { 'id':'ClosedVendorListContent'})
        try:
            sub_divs=getAllTag(div, 'div')
        except:
            sub_divs=getAllTag(unicode(div,errors='ignore'), 'div')
        for it in sub_divs:
            a=getAllTag(it,'span')[0].replace('Open','')
            hours=a.replace('\n','').replace('\t','')
            c=it[it.find('/span>')+6:].replace('\n','').replace('\t','')
            name=c.strip()
            if vendors.count(name) == 0:
                vendors.append(name)
                closed_data.append([name,hours])
                sf.writelines(str(name)+'\t'+str(hours)+'\r')
    sf.close()

def get_vendor_files(check=True):
    path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
    from API_system import getFilesFolders

    workDir='/Users/admin/Desktop/seamless'
    x=getFilesFolders(workDir,full=True)
    a,b=[],[]
    c,d=[],[]
    for it in x:
        if it.find('open-') != -1:
            a.append(it)
            b.append(it[it.rfind('/')+1:].replace('open-','').replace('.html',''))
        elif it.find('closed-') != -1:
            c.append(it)
            d.append(it[it.rfind('/')+1:].replace('closed-','').replace('.html',''))

    if len(a)!=len(c):
        print 'ERROR -- different open/closed'
        print 'open but not closed'
        for it in b:
            if d.count(it)==0:
                print it
        print 'closed but not open'
        for it in d:
            if b.count(it)==0:
                print it
        raise SystemExit

    #compare files with database text file
    if check==True:
        f=open('/Users/admin/Desktop/nyc.txt','r')
        x=f.read()
        f.close()

        rows=x.split('\r')
        ids,addresses=[],[]
        for it in rows:
            ids.append(it.split('\t')[0])
            addresses.append(it.split('\t')[1])

        if len(b)!=len(addresses):
            print 'addresses',len(addresses)
            print 'files',len(b)
            # for it in b:
            #     if it.find('256') != -1:
            #         print b.index(it),'\t',it

            z=[]
            if len(addresses) > len(b):
                print '---printing addresses'
                for it in addresses:
                    #print str(b.index(it))+'\t'+it
                    if b.count(it) == 0:
                        print it
                        z.append(addresses[addresses.index(it)])
                print len(z)
                print z[0]
            z=[]
            if len(addresses) > len(b):
                print '---printing files'
                for it in b:
                    print str(addresses.index(it))+'\t'+it
                    if addresses.count(it) == 0:
                        print it
                        z.append(b[b.index(it)])
                print len(z)
                print z[0]
    return a,b,c,d

def get_coord_from_blockIds():

    f=open('/Users/admin/desktop/nyc1.txt','r')
    x=f.read()
    f.close()
    x=x.split('\r')

    blockId,gpsLat,gpsLong=[],[],[]
    for it in x:
        a,b,c=it.split('\t')
        blockId.append(a)
        gpsLat.append(b)
        gpsLong.append(c)

    f=open('/Users/admin/desktop/nyc2.txt','r')
    x=f.read()
    f.close()
    x=x.split('\r')

    vendor,idNum=[],[]
    for it in x:
        a,b=it.split('\t')
        vendor.append(a)
        idNum.append(b)

    s='vendor'+'\t'+'minLat'+'\t'+'maxLat'+'\t'+'minLong'+'\t'+'maxLong'+'\r'

    for i in range(0,len(vendor)):

        matched=eval(idNum[i])

        minLat=gpsLat[blockId.index(matched[0])]
        maxLat=minLat

        minLong=gpsLong[blockId.index(matched[0])]
        maxLong=minLong

        for j in range(1,len(matched)):
            idLat,idLong=gpsLat[j],gpsLong[j]
            if idLat<minLat: minLat=idLat
            if idLat>maxLat: maxLat=idLat
            if idLong<minLong: minLong=idLong
            if idLong>minLong: maxLong=idLong
        s+=vendor[i]+'\t'+minLat+'\t'+maxLat+'\t'+minLong+'\t'+maxLong+'\r'

    f=open('/Users/admin/Desktop/vend_coord.txt','w')
    f.write(s)
    f.close()

def COLLECT_DATA():
    path.append('/Users/admin/SERVER2/BD_Scripts/files_folders')
    from API_system import getFilesFolders


    workDir=getcwd()+'/vendor_data'
    savePath=workDir+'/vendor_info.txt'

    f=open(workDir+'/vendorIDs.txt')
    x=f.readlines()[0]
    # vendorIDs=x.split('\r')

    getIDs=x.split('\r')

    # ids,vals=[],[]
    # for it in vendorIDs:
    #     a,b = it.split('\t')
    #     if ids.count(a)==0:
    #         ids.append(a)
    #         vals.append(eval(b))
    #     else:
    #         ind = ids.index(a)
    #         vals[ind] += eval(b)
    # for it in ids:
    #     print it+'\t'+str(vals[ids.index(it)])
        # if it=="": print ""
        # else: print D[it]
        # for i in range(0,len(it)):
        #     if it[i].isdigit()==True:
        #         print it[:i-1]+'\t'+it[i:]
        #         break

    # f.close()

    # workDir='/Users/admin/Desktop/vendor_data/yelp/set1'

    # vendorIDs=getFilesFolders(workDir,full=False)
    # savedIDs=getFilesFolders(workDir,full=False)

    #
    # popList=[]
    # for it in getIDs:
    #     if savedIDs.count(it+'.html')==0:
    #         popList.append(getIDs.index(it))
    # popList.reverse()
    # nextList=[]
    # for it in popList:
    #     x=getIDs.pop(it)
    #     print 'not checked\t'+str(x)
    #     nextList.append(x)
    #
    # vendorIDs = getIDs
    # # get_yelp_data()
    # skipped = get_vendor_info_from_vendor_pages(vendorIDs,workDir,savePath)

    workDir='/Users/admin/Desktop/vendor_data/yelp/set2'
    # savedIDs=getFilesFolders(workDir,full=False)
    # # savedIDs.extend(skipped)
    #
    # popList=[]
    # for it in getIDs:
    #     if savedIDs.count(it+'.html')==0:
    #         popList.append(getIDs.index(it))
    # popList.reverse()
    # nextList=[]
    # for it in popList:
    #     x=getIDs.pop(it)
    #     nextList.append(x)
    #     print 'not checked\t'+str(x)


    vendorIDs = getIDs
    # vendorIDs = nextList
    print 'checking',len(vendorIDs),'IDs'
    # get_yelp_data(vendorIDs=vendorIDs)
    get_vendor_info_from_vendor_pages(vendorIDs,workDir,savePath,set=2)
    #get_closed_vendor_pages()

    pass


if __name__ == '__main__':
    # from sys import argv
    try:
        cmd = []
        for i in range(0, len(argv)): cmd.append(argv[i])
            # cmd[0] == current working directory
            # cmd[1] == function to apply
            # cmd[2] == variable for the function
        stop = False
    except:
        cmd = []
        stop = True
    # print cmd
    if stop == False:
        if cmd[1]   == 'get_yelp':                  get_yelp_data()
        elif cmd[1] == 'vendor_info_from_pages':    get_vendor_info_from_vendor_pages()
        elif cmd[1] == 'closed_vendor_info':        get_closed_vendor_pages()
        elif cmd[1] == 'open_vendor_info':          get_open_vendor_pages()
        elif cmd[1] == 'get_vendor_links':          get_vendor_links_on_seamless()            # STEP ONE
        elif cmd[1] == 'get_vendor_page_content_on_seamless':
            get_vendor_page_content_on_seamless()                                             # STEP TWO