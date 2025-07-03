#!/bin/bash

# Function to update frontmatter in a file
update_frontmatter() {
  local file=$1
  
  # Check if the file has applies_to section
  if grep -q "applies_to:" "$file"; then
    # Use sed to add the product section under applies_to
    sed -i '' '/applies_to:/,/[a-z]/ {
      /serverless:/,/[a-z]/ {
        /observability:/a\
  product:\
    edot_collector: ga
      }
    }' "$file"
    echo "Updated: $file"
  else
    echo "Skipping (no applies_to section): $file"
  fi
}

# Process all markdown files in the specified directories
find /Users/fabri/repos/opentelemetry/docs/reference/edot-collector \
     /Users/fabri/repos/opentelemetry/docs/reference/quickstart \
     /Users/fabri/repos/opentelemetry/docs/reference/use-cases \
     -name "*.md" -type f | while read -r file; do
  update_frontmatter "$file"
done
