#!/bin/bash

set -euxo pipefail

MAX_WAIT_SECONDS=120
URL=$1

echo "Waiting up to $MAX_WAIT_SECONDS seconds for the elasticsearch server to be ready by checking $URL"
count=0
while [ $count -lt $MAX_WAIT_SECONDS ]
do
  count=`expr $count + 1`
  STARTED=$((curl -m 2 "$URL" || true) | (grep build_hash || true) | wc -l)
  if [ $STARTED -ne 0 ]
  then
    exit 0
  fi
  sleep 1
done
echo "error: the elasticsearch server failed to be ready within $MAX_WAIT_SECONDS seconds"
curl -v "$URL"
exit 1
