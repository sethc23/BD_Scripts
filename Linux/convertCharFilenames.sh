#!/bin/sh

folder=/Users/admin/Desktop/McCarthy_on_TM/web_archives/*
echo "" > test.txt


for f in $folder
do

  #test first
  old_file_name=`echo $f`
  new_file_name=`echo $old_file_name | tr -d "§"`
  echo $f >> test.txt
  echo $new_file_name >> test.txt
  echo "" >> test.txt



  #run
  #mv "$f" "$new_file_name"

done