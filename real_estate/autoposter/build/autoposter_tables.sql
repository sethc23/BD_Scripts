

DROP TABLE IF EXISTS properties CASCADE;
CREATE TABLE properties (
	_property_id 					        bigint,
	_address 						        text,
	_keys 							        text,
	_photos 						        text,
	_town 							        text,
	_rent 							        double precision,
	_beds 							        integer,
	_date_avail						        timestamp with time zone,
    _created_by 					        text,
	_create_date					        timestamp with time zone,
	_updated_by 					        text,
	_updated_date					        timestamp with time zone,
    _status                                 text,
    _walk_score                             double precision,
    posts                                   jsonb,
    last_postlets                           timestamp with time zone,
    last_craigslist                         timestamp with time zone,
    -- function (update_settings) populates variations of last_craigslist based on templates
    last_craigslist_id                      bigint
    pl_checked_out                          text,
    cl_checked_out                          text,
    cl_post_cnt                             integer,
    cl_last_deleted                         timestamp with time zone
);

DROP TABLE IF EXISTS identities CASCADE;
CREATE TABLE identities (
	guid 						            text,
	email 							        text,
    pw                                      text,
    details                                 jsonb
);

DROP TABLE IF EXISTS pp_settings CASCADE;
CREATE TABLE pp_settings (
    _setting                                text,
    _value                                  text
);

DROP TABLE IF EXISTS craigslist CASCADE;
CREATE TABLE craigslist (
	_status 						        text,
	_post_title						        text,
	_post_date						        timestamp with time zone,
    _post_link                              text,
	_id								        bigint,
    _manage                                 text,
    _property_id                            bigint,
);

DROP TABLE IF EXISTS pp_settings CASCADE;
CREATE TABLE pp_settings (
    _setting                                text,
    _value                                  text,
    _json                                   jsonb
);