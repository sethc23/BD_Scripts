#! /bin/bash

origDir=`echo pwd`
cd /Users/admin/SERVER2/BD_Scripts/crons
source /Users/admin/.bash_profile

cmd=""
if [ "$1" != "" ]
then
  cmd=$cmd$1
fi
if [ "$2" != "" ]
then
  cmd=$cmd' '$2
fi
if [ "$3" != "" ]
then
  cmd=$cmd' '$3
fi

#echo $cmd
python $cmd

cd `$origDir`