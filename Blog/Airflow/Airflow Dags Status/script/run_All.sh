#!/bin/bash

for py in ls /home/script/*
do
	python "$py"
	#echo "$py"
done
