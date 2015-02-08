After getting into postgres utility:

	psql -U postgres -h localhost routing

####Calculate the Distance Between Two Points

	psql -U postgres -h localhost routing -c "SELECT * FROM ways_vertices_pgr ORDER BY the_geom <-> ST_GeometryFromText('POINT(40.745290 -73.99279)') LIMIT 1;"

	
	
	import psycopg2
	conn = psycopg2.connect('dbname=routing user=postgres')
	cur=conn.cursor()
	cur.execute("SELECT * FROM ways_vertices_pgr ORDER BY the_geom <-> ST_GeometryFromText('POINT(40.745290 -73.99279)') LIMIT 1;"

####Converting NYC Gov Data (.shp) to OSM format (.osm)

	python /Users/sethchase/Dropbox/BD_Scripts/geolocation/ogr2osm/ogr2osm.py /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp -o /Users/sethchase/Projects/GIS/NYC_gov_data/MNMapPLUTO.osm -e 2263 -v

####Converting to WSG84

Tried this but segmentation fault:

	ogr2ogr -f "PostgreSQL" /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/manh1.shp /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp

This did not work:

	ogr2ogr -f "PGDump" /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/manh1.dump /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp
	
	pg_restore -C -d postgres /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/manh1.dump

This worked:

	python /Users/sethchase/Dropbox/BD_Scripts/geolocation/shape2osm-master/shape2osm.py /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.osm
	
Trying to insert into DB:
	
	osm2pgrouting -file "/Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.osm" \
                          -conf "/Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp.xml" \
                          -dbname routing \
                          -user postgres \
                          -clean

Some error with geometry of "the_geom".  Moving on…

	ogr2ogr -f "CSV" /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.csv /Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.shp
	
Then import into DB:
	
	osm2pgrouting -file "/Users/sethchase/Projects/GIS/NYC_gov_data/Manhattan/MNMapPLUTO.csv" \
                          -conf "/Users/sethchase/Projects/GIS/mapconfig.xml" \
                          -dbname routing \
                          -user postgres \
                          -clean

Got this:

    ...
    Nodes table created
    2create ways failed: 
    ...
    Creating topology...
    NOTICE:  PROCESSING:
    NOTICE:  pgr_createTopology('ways',1e-05,'the_geom','gid','source','target','true')
    NOTICE:  Performing checks, pelase wait .....
    NOTICE:  ERROR: Can not determine the srid of the geometry "the_geom" in table public.ways
    Create Topology success
	#########################
	size of streets: 0
	size of splitted ways : 0
	finished

Convert lion.gdb to ogr

	ogr2ogr -f "DXF" /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion4.dxf /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion.gdb
	
	ogr2ogr -update -append -f PostgreSQL PG:dbname=routing /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion.dxf
	
	ogr2ogr -update -append -f PostgreSQL PG:dbname=routing -f DXF /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion.dxf
	
That didn't work.

Trying to load shp file:

	-- osm2pgrouting -file "/Users/sethchase/Projects/GIS/NYC_gov_data/lion4.dxf" \
		-conf "/Users/sethchase/Projects/GIS/mapconfig.xml" \
		-dbname routing \
		-user postgres \
		-clean	
                          
	-- osm2pgrouting -file "/Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion4.dxf" \
                          -conf "/Users/sethchase/Projects/GIS/mapconfig.xml" \
                          -dbname routing \
                          -user postgres \
                          -clean
                          
                          


	-- gpsbabel -i gdb -f /Users/sethchase/Projects/GIS/NYC_gov_data/lion/lion.gdb -o osm -F /Users/sethchase/Projects/GIS/NYC_gov_data/lion.osm
	
	
####API for NYC_BYTES Data

lion.StreetCode 

	a numeric code that represents the names of New York city streets. The first digit is a borough code; the subsequent five digits are the 5-digit street code.
	
	 "Street"  IS upper( "madison avenue"  )  AND  
	
#####Use pad14b from NYC BYTES to verify address and tag node

#####To Do List:

1. make buildings the nodes (block,lot,bin)
2. 

