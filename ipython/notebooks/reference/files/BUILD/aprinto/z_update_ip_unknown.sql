-- Function: z_update_ip_unknown(cidr)

-- DROP FUNCTION z_update_ip_unknown(cidr);

CREATE OR REPLACE FUNCTION z_update_ip_unknown(ip_addr_chk cidr)
  RETURNS text AS
$BODY$

    upsert="""
        with upd as (
            UPDATE ip_unknown unkn
            SET 
                access_cnt = access_cnt + 1,
                last_accessed = 'now'::timestamp with time zone
            WHERE unkn.ip_addr::cidr = '%s'::cidr
            RETURNING unkn.ip_addr unkn_ip_addr
            )
        insert into ip_unknown (
            ip_addr,
            access_cnt,
            last_accessed
            )
        SELECT t.ip_addr,1,'now'::timestamp with time zone
        FROM 
            (SELECT '%s'::cidr ip_addr) as t,
            (SELECT array_agg(unkn.ip_addr::cidr) all_unknown_ips FROM ip_unknown unkn) as f1
        WHERE not all_unknown_ips @> array[t.ip_addr]
        OR all_unknown_ips is null;
        """%ip_addr_chk

    plpy.execute(upsert)

    p = "SELECT access_cnt FROM ip_unknown WHERE ip_addr = '%s'::cidr"%ip_addr_chk
    current_access_cnt = plpy.execute(p)[0]['cnt']

    if current_access_cnt >= 5:
               
        insert = """INSERT into ip_blacklist (ip_addr,added) 
             VALUES ('%s'::cidr,'now'::timestamp with time zone)"""%ip_addr_chk
        plpy.execute(insert)
        
        delete = "DELETE from ip_unknown where ip_addr = '%s'::cidr"%ip_addr_chk
        plpy.execute(delete)
        
        return "blacklisted"
    
    else:
    
        return "marked"
        
$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION z_update_ip_unknown(cidr)
  OWNER TO postgres;
