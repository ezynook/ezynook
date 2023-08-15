#!/bin/bash

service apache2 start
uvicorn main:app --reload --port 3000 --log-level debug --host "0.0.0.0" --reload