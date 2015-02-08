#!/bin/bash

HERE=`pwd`
GROUP=jail
BASE=/home/$GROUP
USER=serv

sudo userdel $USER
sudo groupdel $GROUP
sudo rm -R $BASE

sudo mkdir $BASE
sudo mkdir -p $BASE/{dev,etc,lib,usr,bin}
sudo mkdir -p $BASE/usr/bin
sudo chown root.root $BASE
# OpenSSH apparently requires this... (not confirmed)
sudo chmod go-w $BASE
sudo mknod -m 666 $BASE/null c 1 3

cd $BASE/etc
sudo cp -R /etc/ld.so.conf .
sudo cp -R /etc/ld.so.conf.d/ .
sudo cp -R /etc/ld.so.cache .
sudo cp -R /etc/nsswitch.conf .
sudo cp -R /etc/hosts .
sudo cp -R /etc/passwd .
sudo cp -R /etc/group .
sudo cp -R /etc/resolv.conf .


cd $BASE/bin
sudo cp -R /bin/bash .
sudo cp -R /bin/ls .
sudo cp -R /bin/cp .
sudo cp -R /bin/mv .
sudo cp -R /bin/mkdir .
sudo cp -R /bin/ls .
sudo cp -R /bin/bash .
sudo cp -R /bin/cat .
sudo cp -R /bin/chmod .
sudo cp -R /bin/cp .
sudo cp -R /bin/date .
sudo cp -R /bin/df .
sudo cp -R /bin/echo .
sudo cp -R /bin/grep .
#sudo cp -R /bin/gunzip .
#sudo cp -R /bin/gzip .
sudo cp -R /bin/hostname .
sudo cp -R /bin/ln .
sudo cp -R /bin/mkdir .
sudo cp -R /bin/mv .
sudo cp -R /bin/rm .
sudo cp -R /bin/rmdir .
sudo cp -R /bin/tar .
sudo cp -R /bin/touch .
#sudo cp -R /bin/uncompress .
sudo cp -R /bin/mount .

cd $BASE/usr/bin
sudo cp -R /usr/bin/clear .
sudo cp -R /usr/bin/emacs .
sudo cp -R /usr/bin/ssh .
sudo cp -R /usr/bin/git .

#cd ~/SERVER1/BUILD
chmod +x $HERE/chroot.sh

sudo $HERE/chroot.sh /bin/bash 
sudo $HERE/chroot.sh /bin/ls 
sudo $HERE/chroot.sh /bin/cp 
sudo $HERE/chroot.sh /bin/mv 
sudo $HERE/chroot.sh /bin/mkdir 
sudo $HERE/chroot.sh /bin/ls 
sudo $HERE/chroot.sh /bin/bash 
sudo $HERE/chroot.sh /bin/cat 
sudo $HERE/chroot.sh /bin/chmod 
sudo $HERE/chroot.sh /bin/cp 
sudo $HERE/chroot.sh /bin/date 
sudo $HERE/chroot.sh /bin/df 
sudo $HERE/chroot.sh /bin/echo 
sudo $HERE/chroot.sh /bin/grep 
#sudo $HERE/chroot.sh /bin/gunzip 
#sudo $HERE/chroot.sh /bin/gzip 
sudo $HERE/chroot.sh /bin/hostname 
sudo $HERE/chroot.sh /bin/ln 
sudo $HERE/chroot.sh /bin/mkdir 
sudo $HERE/chroot.sh /bin/mv 
sudo $HERE/chroot.sh /bin/rm 
sudo $HERE/chroot.sh /bin/rmdir 
sudo $HERE/chroot.sh /bin/tar 
sudo $HERE/chroot.sh /bin/touch 
#sudo $HERE/chroot.sh /bin/uncompress 
sudo $HERE/chroot.sh /usr/bin/emacs
sudo $HERE/chroot.sh /usr/bin/ssh
sudo $HERE/chroot.sh /usr/bin/clear
sudo $HERE/chroot.sh /usr/bin/git

cd $BASE/lib
sudo cp -r /lib/terminfo .

sudo groupadd jail
sudo mkdir $BASE/home
sudo useradd -d $BASE/home/$USER -m $USER
sudo passwd $USER
