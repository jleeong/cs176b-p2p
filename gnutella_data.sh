#!/bin/bash

if [ ! -d output ]
then
  mkdir output
fi

for i in 20 50 100 500 1000;
do
  echo $i nodes:
  python3 append_nodes.py $i
  python3 deploydocker.py -f -m g
  sleep 5
  python3 test.py -m g $i 50
  echo Tearing down containers...
  docker stop $(docker ps -q)
done
