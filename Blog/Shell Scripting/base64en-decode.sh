#!/bin/bash
read -p "Please enter Mode 1.Encode / 2.Decode: " modes
if [ "$modes" == "1" ]; then
    read -p "Enter Your Customer name: " product
    encode=$(echo $product | base64)
    echo "License Key : $encode"
else
    read -p "Enter Your License Keys: " product
    encode=$(echo $product | base64 --decode)
    echo "Customer Name : $encode"
fi
