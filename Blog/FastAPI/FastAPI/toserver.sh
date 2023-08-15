#!/bin/sh

rsync -avh --progress \
--exclude='__pycache__' \
--exclude='toserver.sh' \
. root@192.168.10.23:/home/FastAPI/
