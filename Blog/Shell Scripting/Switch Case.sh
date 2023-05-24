#!/bin/bash

read -p "Enter Your Age: " AGE

case "$AGE" in
   "20") echo "You are Young." 
   ;;
   "30") echo "You are old Young." 
   ;;
   "40") echo "You are old." 
   ;;
    *)
   echo "Another Age" 
    ;;
esac