#!/bin/bash
                                                                                           
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 90 ]; then
    echo "
   _____  ____  ______ _______ _   _ _______   __
  / ____|/ __ \|  ____|__   __| \ | |_   _\ \ / /
 | (___ | |  | | |__     | |  |  \| | | |  \ V / 
  \___ \| |  | |  __|    | |  | . ` | | |   > <  
  ____) | |__| | |       | |  | |\  |_| |_ / . \ 
 |_____/ \____/|_|       |_|  |_| \_|_____/_/ \_\     
            Disk Space is Full: $usep
    "
  else
    echo "
   _____  ____  ______ _______ _   _ _______   __
  / ____|/ __ \|  ____|__   __| \ | |_   _\ \ / /
 | (___ | |  | | |__     | |  |  \| | | |  \ V / 
  \___ \| |  | |  __|    | |  | . ` | | |   > <  
  ____) | |__| | |       | |  | |\  |_| |_ / . \ 
 |_____/ \____/|_|       |_|  |_| \_|_____/_/ \_\     
            Disk Space is Normal: $usep
    "
  fi
done