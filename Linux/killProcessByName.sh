#!/bin/bash

if [ $1 != "" ]
then
  get_proc=`ps -e -o pid,command | grep $1`
  get_pid=`echo ${get_proc%% /*}`
  kill -9 $get_pid
fi