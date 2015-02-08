-- Function: z_new_order(character varying)

-- DROP FUNCTION z_new_order(character varying);

CREATE OR REPLACE FUNCTION z_new_order(pdf_id character varying)
  RETURNS text AS
$BODY$
    import requests
    from json import dumps as j_dumps
    from post_json import post_it
    
    user_id = '544963fce4b00f942bc97027'
    satellite_id = '544963fce4b00f942bc9702e'
    
    p = """
            select
                    '%s' satellite_id,
                    p.cust_name cust_name,
                    p.cust_tel cust_tel,
                    p.cust_addr cust_addr,
                    p.cust_cross_st cust_cross_st,
                    to_char(p.order_price, '990D99') price,
                    to_char(p.order_tip, '990D99') tip,
                    p.pdf_id order_uuid,
                    concat(to_char(p.created, 'YYYYMMDDHH24:MI:SS'),'-0400') order_time,
                    p.order_tag order_tag,
                    v.name vend_name,
                    v.addr vend_addr,
                    v.recipient_emails recipient_emails
                from app_pdf p
                inner join app_vendors v on v.id = p.vendor_id
                WHERE pdf_id = '%s';
        """%(satellite_id,pdf_id)
    res = plpy.execute(p)[0]
    json_data = j_dumps([res]).encode('utf-8')
    
    post_url = 'http://admin.gnamgnamapp.it/ws/v2/'+user_id+'/aporoOrders'
    headers = {'Content-type': 'application/json'}
    response = requests.post(post_url, data=json_data, headers=headers)
    
    
    post_it(post_url,json_data)

    return str(str(response.status_code)+'\n\t'+response.content+'\n\n'+response.request.body)


$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION z_new_order(character varying)
  OWNER TO postgres;
