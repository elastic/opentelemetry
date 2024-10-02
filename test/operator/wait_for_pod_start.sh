#!/bin/bash

set -euxo pipefail

MAX_WAIT_SECONDS=60
NAMESPACE=$1
POD_NAME=$2
GREP=$3
COUNT_PODS=$4

echo "Waiting up to $MAX_WAIT_SECONDS seconds for the $NAMESPACE pods called $POD_NAME to be ready"
count=0
while [ $count -lt $MAX_WAIT_SECONDS ]
do
  count=`expr $count + 1`
  STARTED=$(kubectl get pod -n $NAMESPACE | (grep "$POD_NAME" || true) | (grep "$GREP" || true) | wc -l)
  if [ $STARTED -eq $COUNT_PODS ]
  then
    exit 0
  fi
  sleep 1
done

echo "error: the $NAMESPACE pods called $POD_NAME failed to be ready within $MAX_WAIT_SECONDS seconds"
echo "-- pod info:"
kubectl get pod -A
echo "--"
exit 1
