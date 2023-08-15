#!/bin/bash

TODAY=$(date +'%d-%m-%Y-%H-%M-%S')

git add .
git commit -m "$TODAY"
git push origin main
echo Success