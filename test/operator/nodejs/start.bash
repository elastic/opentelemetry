#!/bin/bash
node app.js &
while :
do
  sleep 1
  curl -s http://127.0.0.1:8080/ > /dev/null
done
