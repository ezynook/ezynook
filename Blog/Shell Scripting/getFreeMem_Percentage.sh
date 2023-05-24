#!/bin/bash

secondLine=$(free -g | sed -n '2p')

read -ra ADDR <<< "$secondLine"

totalRam="${ADDR[1]}"

usedRam="${ADDR[2]}"

pct="$(($usedRam*100/$totalRam))"
echo "$pct%"