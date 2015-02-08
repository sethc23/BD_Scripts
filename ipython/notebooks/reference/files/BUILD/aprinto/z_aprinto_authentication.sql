
-- Function: z_aprinto_authentication(text, text)

drop function if exists public.z_aprinto_authentication(text,text);

create or replace function z_aprinto_authentication(ip_addr text,machine_id text)
returns text
as $$

    def new_contact():
        # known user
        # unknown user

        if machine_id != '':  a_cnt,v_cnt = get_machine_id_count()
        else:                 a_cnt,v_cnt = 0,0

        if a_cnt+v_cnt>0:   
            tmp_insert =  """
                          machine_id,
                          known_user, 
                          blacklist, 
                          status_changed,
                          """
            tmp_values =  "%(machine_id)s,True,False,'now'::timestamp with time zone,"%T
            return_var = 'ok'
        elif machine_id != '':
            tmp_insert =  "machine_id,"
            tmp_values =  "%(machine_id)s,"%T
            return_var = 'marked'
        else:
            tmp_insert,tmp_values,return_var = '','','marked'

        T["insert"] = tmp_insert.replace('	','')
        T["values"] = tmp_values.replace('	','')
        
        insert="""
            insert into ip_addresses (
                    ip_addr,
                    access_cnt,
                    %(insert)s
                    updated
                    )
            SELECT %(ip_addr)s::cidr,1, %(values)s 'now'::timestamp with time zone;
            """%T

        plpy.execute(insert)
        return return_var

    def get_machine_id_count():
        p = "SELECT count(*) cnt from aprinto_vendor WHERE machine_id = '%s'"%(machine_id)
        v_cnt = plpy.execute(p)[0]['cnt']
        p = "SELECT count(*) cnt from aprinto_admin WHERE machine_id = '%s'"%(machine_id)
        a_cnt = plpy.execute(p)[0]['cnt']
        return a_cnt,v_cnt

    def machine_id_check():
        a_cnt,v_cnt = get_machine_id_count()

        if a_cnt+v_cnt==0:
            return
        else:   
            tmp_set = """
                      machine_id = %(machine_id)s,
                      known_user = True, 
                      blacklist=False, 
                      status_changed='now'::timestamp with time zone
                      """.replace('	','')%T
        
            T["set"]=tmp_set

            update = """
                    UPDATE ip_addresses 
                    SET 
                        %(set)s
                    WHERE 
                        ip_addr::cidr = %(ip_addr)s::cidr
                        %(where)s
                    """%T
            plpy.execute(update)
            return 'ok'


    def update_contact():
        if machine_id != '':    t = ", machine_id = '%s'"%machine_id
        else:                   t = ''
        T["set"]=t
        update = """
                UPDATE ip_addresses 
                SET 
                    access_cnt = access_cnt+1,
                    updated = 'now'::timestamp with time zone
                    %(set)s
                WHERE 
                    ip_addr::cidr = %(ip_addr)s::cidr
                    %(where)s;
                """%T
        plpy.execute(update)

    def final_check():
        if machine_id != '':
            if machine_id_check() == 'ok':
                return 'ok'

        p = """
            SELECT access_cnt,machine_id 
            FROM ip_addresses 
            WHERE 
                ip_addr::cidr = %(ip_addr)s::cidr
                %(where)s
            """%T
        t = plpy.execute(p)[0]
        current_access_cnt = t['access_cnt']
        current_machine_id = t['machine_id']
        
        if ( (str(current_machine_id) != "None" and current_access_cnt >= 5)
          or (str(current_machine_id) == "None" and current_access_cnt >= 3) ):

            blacklist = """
                        UPDATE ip_addresses 
                        SET 
                            blacklist=True,
                            status_changed='now'::timestamp with time zone
                        WHERE 
                            ip_addr::cidr = %(ip_addr)s::cidr
                            %(where)s;
                        """%T

            plpy.execute(blacklist)
            return "blacklisted"
            
        else:
            return "marked"


    ## <<<<<<<<<<< ---------------------------- >>>>>>>>>>>

    T={}
    T["ip_addr"]="'"+ip_addr+"'::cidr"

    if machine_id != '':
        T["machine_id"]="'"+machine_id+"'"
        m_def = "machine_id = %(machine_id)s"%T
        t = "AND %s"%m_def
    else:
        T["machine_id"]=None
        m_def = "machine_id is null"
        t = "AND %s"%m_def
        
    T["where"]=t
        
    p = """
        SELECT count(*) cnt 
        FROM ip_addresses 
        WHERE 
            ip_addr::cidr = %(ip_addr)s::cidr
            %(where)s;
        """%T
    res_cnt = plpy.execute(p)[0]['cnt']

    if res_cnt == 0:
        return new_contact()
    else:
        # known ip, known machine_id
        # known ip, unknown machine_id
        # known machine_id, unknown ip

        update_contact()

        p = """
            SELECT * 
            FROM ip_addresses 
            WHERE 
                ip_addr::cidr = %(ip_addr)s::cidr
                %(where)s;
            """%T
        res_info = plpy.execute(p)[0]
        
        if res_info['blacklist'] == True:
            if machine_id == '':
                return 'blacklisted'
            else:
                return final_check()
        elif res_info['known_user'] == True:
            return 'ok'
        else:
            return final_check()   

$$ language plpythonu;


