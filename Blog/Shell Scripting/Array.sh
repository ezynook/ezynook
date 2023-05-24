#!/bin/sh

#$Arr[*] = แสดงทั้งหมด
Arr=('nook' 'pasit' 'yodsoi')
Arr[3]='xxx'
echo ${Arr[*]}