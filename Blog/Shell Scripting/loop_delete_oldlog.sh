#!/bin/bash

tdate=$(date -d "90 days ago" "+%Y-%m-%d")
path="/root/nook/"

find ${path} -type d -maxdepth 1 -printf "%P\n" |
while ps= read -r LOG; do
    if [ "${tdate}" ">" "${LOG%.*}" ]; then
        rm -rf ${path}${LOG}
    fi
done




# Generate the date in the proper format
discriminant=$(date -d "30 days ago" "+%Y_%m_%d")

# Find files based on the filename pattern and test against the date.
find . -type f -maxdepth 1 -name "*_*_*.txt" -printf "%P\n" |
while IFS= read -r FILE; do
    if [ "${discriminant}" ">" "${FILE%.*}" ]; then
        echo "${FILE}";
    fi
done