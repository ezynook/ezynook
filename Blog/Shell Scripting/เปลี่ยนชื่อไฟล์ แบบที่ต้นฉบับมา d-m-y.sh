#!/bin/bash
<<Readme
        - เอาไฟล์ Script ไปวางในตำแหน่งเดียวกับไฟล์ CSV
        - ชื่อไฟล์ตั้นฉบับต้องเป็น _all_topics_custom-data- เท่านั้น หากมีการเปลี่ยน Format
          ให้มาเปลี่ยนชื่อไฟล์ที่ #2
        - #1 คือตัดเอาเฉพสะวันที่มาแปลงเป็นรูปแบบ d/m/Y_2359
Readme

#Find Only CSV files
FILES=$(ls *.csv | grep -Eo '[[:digit:]]{4}[[:digit:]]{2}[[:digit:]]{2}-[[:digit:]]{4}[[:digit:]]{2}[[:digit:]]{2}') #1

for i in $FILES; do
        FILENAME="custom-data-"$i".csv" #2
        FILE2=$(echo $i | tr -dc '[:alnum:]\n\r' | tr '[:upper:]' '[:lower:]')
        sudo cp $FILENAME "custom_data_${FILE2}_2359.csv"
        echo "Export Success -> custom_data_${FILE2}_2359.csv"
done
echo "==============================="
echo "    Export to Successfully"
echo "==============================="
