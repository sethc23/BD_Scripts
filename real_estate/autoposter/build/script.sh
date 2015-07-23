#!/bin/bash

sudo -u postgres psql postgres -h 0.0.0.0 --port=8800 -c 'CREATE DATABASE autoposter'
sudo -u postgres psql -h 0.0.0.0 --port=8800 --dbname=autoposter -c '\i pgsql_functions.sql'
