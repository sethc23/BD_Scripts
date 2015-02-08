-- Function: z_fake_order(character varying)

-- DROP FUNCTION z_fake_order(character varying);

CREATE OR REPLACE FUNCTION z_fake_order(pdf_id character varying)
  RETURNS void AS
$BODY$
    
    p = """ update app_pdf 
            set 
                vendor_id = 1,
                cust_name = 'fat tony',
                cust_tel = '555-555-5555',
                cust_addr = '10 east 20th st., new york, ny 10003',
                cust_cross_st = '20th st. & 5th ave.',
                order_price = 20.00,
                order_tip = 5.00
            WHERE pdf_id = '%s'
            """%(pdf_id)
    
    plpy.execute(p)
        
$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION z_fake_order(character varying)
  OWNER TO postgres;
