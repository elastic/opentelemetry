#!/bin/bash
python3 -m flask run &
while :
do
  sleep 1
  curl -s http://localhost:5000/ > /dev/null
done
