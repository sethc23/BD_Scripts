#! /bin/bash -l

source ~/.bashrc

cd $BD/real_estate/autoposter/vpns
sudo ./hma_grabber.sh

cd $HOME/.scripts
source ENV/bin/activate

python -c "import os;\
from sys                            import path; \
path.append(                     '/home/ub2/BD_Scripts/real_estate/autoposter'); \
from auto_poster import Auto_Poster; \
x=Auto_Poster(); \
x.VPN.update_db_with_server_info()"