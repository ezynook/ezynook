#!/bin/bash
#   _____         _____ _____ _______  __     __
#  |  __ \ /\    / ____|_   _|__   __| \ \   / /
#  | |__) /  \  | (___   | |    | |     \ \_/ /
#  |  ___/ /\ \  \___ \  | |    | |      \   /
#  | |  / ____ \ ____) |_| |_   | |       | |_
#  |_| /_/    \_\_____/|_____|  |_|       |_(_)

if [ -z "$(sudo netstat -tupln | grep 10050)" ]; then
    echo "Closed"
else
    echo "Open"
fi
