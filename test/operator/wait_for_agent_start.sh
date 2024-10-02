#!/bin/bash

set -euxo pipefail

MAX_WAIT_SECONDS=60
NAMESPACE=$1
POD_NAME=$2
GREP=$3

echo "Waiting up to $MAX_WAIT_SECONDS seconds for the agent to start in $NAMESPACE/$POD_NAME"
count=0
while [ $count -lt $MAX_WAIT_SECONDS ]
do
  count=`expr $count + 1`
  STARTED=$(kubectl logs $POD_NAME -n $NAMESPACE | (grep "$GREP" || true) | wc -l)
  if [ $STARTED -eq 1 ]
  then
    exit 0
  fi
  sleep 1
done

echo "error: the $NAMESPACE/$POD_NAME pod failed to start an agent within $MAX_WAIT_SECONDS seconds"
echo "-- pod info:"
kubectl logs $POD_NAME -n $NAMESPACE
kubectl describe pod/$POD_NAME -n $NAMESPACE
echo "--"
exit 1
