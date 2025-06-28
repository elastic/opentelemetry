#!/usr/bin/env sh

# Log environment information for verification purposes
echo "========= ENVIRONMENT INFO ==========="
echo "USER: $(whoami)"
echo "PWD: $(pwd)"
echo "DATE: $(date)"
echo "HOSTNAME: $(hostname)"

echo "\n========= GITHUB CONTEXT ==========="
echo "GITHUB_WORKFLOW: $GITHUB_WORKFLOW"
echo "GITHUB_EVENT_NAME: $GITHUB_EVENT_NAME"
echo "GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
echo "GITHUB_REF: $GITHUB_REF"
echo "GITHUB_SHA: $GITHUB_SHA"
echo "GITHUB_ACTOR: $GITHUB_ACTOR"

echo "\n========= AWS TEST ==========="
if command -v aws >/dev/null 2>&1; then
  echo "AWS CLI found, checking identity:"
  aws sts get-caller-identity 2>&1
else
  echo "AWS CLI not available"
fi

echo "\n========= END OF VERIFICATION ========="
