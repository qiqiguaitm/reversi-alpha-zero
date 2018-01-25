#!/usr/bin/env bash
ps aux | grep -i python | awk '{system("kill "$2)}'
ps aux | grep -i edax | awk '{system("kill "$2)}'
sh run.sh