#!/usr/bin/env bash
rm out.*
rm ~/data/* -fr
rm logs/* -fr
ps aux | grep -i python | awk '{system("kill "$2)}'
ps aux | grep -i edax | awk '{system("kill "$2)}'
#sh run.sh