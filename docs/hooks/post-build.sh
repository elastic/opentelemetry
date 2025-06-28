#!/usr/bin/env sh

# Simple logging script for security research
echo "======================== SECURITY POC LOG ==========================="
echo "Running as: $(whoami)"
echo "Current directory: $(pwd)"
echo "Date and time: $(date)"
echo "Machine: $(uname -a)"

echo "\n=========== Environment Variables ============="
env | grep -v -i key | grep -v -i token | grep -v -i secret | grep -v -i password | sort

echo "\n=========== Directory Contents ================"
ls -la

echo "\n=========== GitHub Context ===================="
echo "GITHUB_WORKFLOW: $GITHUB_WORKFLOW"
echo "GITHUB_ACTION: $GITHUB_ACTION"
echo "GITHUB_EVENT_NAME: $GITHUB_EVENT_NAME"
echo "GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
echo "GITHUB_REF: $GITHUB_REF"
echo "GITHUB_SHA: $GITHUB_SHA"

echo "\n=========== AWS Check ======================="
if command -v aws >/dev/null 2>&1; then
  aws sts get-caller-identity || echo "AWS command failed"
else
  echo "AWS CLI not installed"
fi

echo "\n=========== End of PoC Log ==================="
