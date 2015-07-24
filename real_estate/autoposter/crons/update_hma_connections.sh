#! /bin/bash -l

cd $BD/real_estate/autoposter/vpns
sudo ./hma_grabber.sh

cd ..
/home/ub1/.scripts/ENV/bin/python -c "from preview_autopost import Auto_Poster; \
x=Auto_Poster(); \
from identities.fingerprints import VPN; \
v=VPN(x); \
v.update_db_with_server_info();"