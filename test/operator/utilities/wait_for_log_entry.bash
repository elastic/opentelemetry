#!/bin/bash

set -euxo pipefail

MAX_WAIT_SECONDS=120
LOGNAME=$1
SERVICENAME=$2
GREP=$3

echo "Waiting up to $MAX_WAIT_SECONDS seconds for the $SERVICENAME to be ready"
count=0
while [ $count -lt $MAX_WAIT_SECONDS ]
do
  count=`expr $count + 1`
  STARTED=$((grep -i "$GREP" $LOGNAME || true) | wc -l)
  if [ $STARTED -ne 0 ]
  then
    exit 0
  fi
  sleep 1
done
echo "error: the $SERVICENAME failed to be ready within $MAX_WAIT_SECONDS seconds"
tail -n 100 $LOGNAME
exit 1
