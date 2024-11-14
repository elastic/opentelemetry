#!/bin/bash

set -euxo pipefail

EXECUTION_LINE=$1
FILE_GUIDE="./docs/kubernetes/operator/README.md"
MATCHES=$(sed -n '/```/,/```/p' $FILE_GUIDE | perl -pe 's/^\s*//; s/\s*\\\s*\n/ /mg' | grep "$EXECUTION_LINE" | wc -l)
if [ $MATCHES -eq 1 ]
then
  echo "Executing '$EXECUTION_LINE'"
  eval "$EXECUTION_LINE"
else
  echo "Couldn't find '$EXECUTION_LINE' in '$FILE_GUIDE' so aborting"
  exit 1
fi
