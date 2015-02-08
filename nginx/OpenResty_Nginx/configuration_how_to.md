#OpenResty Install/Setup

#### Macports:

	sudo port install boost pcre openssl
	sudo port install libmpc libiconv
	sudo port install intltool libgcrypt protobuf-c protobuf-cpp

	wget http://openresty.org/download/drizzle7-2011.07.21.tar.gz

	tar xzvf drizzle7-2011.07.21.tar.gz
	cd drizzle7-2011.07.21/
	./configure --without-server
	sudo make libdrizzle-1.0 && sudo make install-libdrizzle-1.0

## OpenResty

###### Download latest version:

	wget http://openresty.org/download/ngx_openresty-1.7.7.1.tar.gz

###### Misc. Libraries

	sudo yum install postgresql-libs postgresql-devel

###### Run Config:
sudo ./configure \
--with-pcre-jit \
--with-ipv6 \
--with-debug \
--with-luajit \
--without-http_redis2_module \
--with-http_drizzle_module \
--with-http_iconv_module \
--with-libdrizzle=/usr/local \
--with-http_postgres_module \
--with-select_module \
--add-module=mods/nginx-http-rdns-master \
--add-module=mods/ngx_aws_auth-master \
--add-module=mods/ngx_http_lower_upper_case-master \
--add-module=mods/ngx_http_internal_redirect-master \
--add-module=mods/ngx_upstream_jdomain-master \
--with-http_sub_module \
--with-http_addition_module \
--without-lua_redis_parser \
--with-http_spdy_module \
--with-http_ssl_module \
--with-pg_config=/opt/local/lib/postgresql93/bin/pg_config \
--error-log-path=logs/ngx_error.log
	
	--with-pg_config=/usr/bin/pg_config
	
	

###### Install:

	sudo make && sudo make install

###### Add Lua-resty-logger-socket:

	git clone --recursive https://github.com/cloudflare/lua-resty-logger-socket.git
	sudo rm -fR /usr/local/openresty/lualib/resty_logger
	sudo mkdir /usr/local/openresty/lualib/resty_logger
	sudo mv lua-resty-logger-socket/lib/resty/logger/socket.lua /usr/local/openresty/lualib/resty_logger/

###### Reset Settings:

	mv -f ~/SERVER3/nginx/setup/conf/nginx.conf ~/SERVER3/nginx/
	mv ~/SERVER3/nginx/setup/nginx/sites-available ~/SERVER3/nginx/
	
	rm -R ~/SERVER3/nginx/setup/nginx
	
	cp -R /usr/local/openresty/nginx  ~/SERVER3/nginx/setup
	rm -R ~/SERVER3/nginx/setup/nginx/sites-available
	
	mv -f ~/SERVER3/nginx/nginx.conf ~/SERVER3/nginx/setup/nginx/conf/
	mv -f ~/SERVER3/nginx/sites-available ~/SERVER3/nginx/setup/nginx/


###### Other Mods Considered:

	--add-module=openresty_mods/gnosek-nginx-upstream-fair-a18b409 \
	--add-module=/Users/sethchase/Desktop/OPENRESTY/openresty_mods/nginx-http-sysguard-master \
	--add-module=/Users/sethchase/Desktop/OPENRESTY/openresty_mods/nginx-backtrace-master \

