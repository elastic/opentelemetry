#!/bin/bash

set -euxo pipefail

MAX_WAIT_SECONDS=120
URL=$1
SERVICE_NAME=$2
KUBECTL_COMMAND=$3

echo "Waiting up to $MAX_WAIT_SECONDS seconds for the elasticsearch server to show a transaction from $SERVICE_NAME by querying $URL"
count=0
while [ $count -lt $MAX_WAIT_SECONDS ]
do
  count=`expr $count + 1`
  #curl -m 2 "$URL/traces*/_search" -H "Content-Type: application/json" -d '{"query": {"range": {"@timestamp": {"gte": "now-1h","lte": "now"}}}}' > query.output
  curl -m 2 "$URL/traces*/_search" -H "Content-Type: application/json" -d "{\"query\": {\"bool\": {\"must\": [{\"range\": {\"@timestamp\": {\"gte\": \"now-1h\",\"lte\": \"now\"}}},{\"match\": {\"resource.attributes.service.name\": \"$SERVICE_NAME\"}}]}}}" > query.output
  DETECTED_SERVICE=$(jq '.hits.hits[0]._source.resource.attributes."service.name"' query.output | tr -d '"')
  if [ "x$DETECTED_SERVICE" = "x$SERVICE_NAME" ]
  then
    exit 0
  fi
  sleep 1
done

echo "error: the elasticsearch server failed to include a transaction with the service name $SERVICE_NAME wihin $MAX_WAIT_SECONDS seconds"
eval $KUBECTL_COMMAND
cat query.output | jq
exit 1
