#!/bin/bash

# Function to update frontmatter in a file
update_frontmatter() {
  local file=$1
  
  # Check if the file has applies_to section and doesn't already have product: edot_collector
  if grep -q "applies_to:" "$file" && ! grep -q "edot_collector: ga" "$file"; then
    # Create a temporary file
    temp_file=$(mktemp)
    
    # Process the file
    awk '
    BEGIN { in_frontmatter = 0; in_applies_to = 0; added = 0; }
    /^---/ && in_frontmatter == 0 { in_frontmatter = 1; print; next; }
    /^---/ && in_frontmatter == 1 { in_frontmatter = 0; print; next; }
    /^applies_to:/ && in_frontmatter == 1 { in_applies_to = 1; print; next; }
    /^[a-zA-Z]/ && in_applies_to == 1 && in_frontmatter == 1 && added == 0 { 
      in_applies_to = 0; 
      print "  product:";
      print "    edot_collector: ga";
      added = 1;
      print;
      next;
    }
    { print; }
    ' "$file" > "$temp_file"
    
    # Replace the original file with the modified content
    mv "$temp_file" "$file"
    echo "Updated: $file"
  else
    if grep -q "edot_collector: ga" "$file"; then
      echo "Already updated: $file"
    else
      echo "Skipping (no applies_to section): $file"
    fi
  fi
}

# Process all markdown files in the specified directories
find /Users/fabri/repos/opentelemetry/docs/reference/edot-collector \
     /Users/fabri/repos/opentelemetry/docs/reference/quickstart \
     /Users/fabri/repos/opentelemetry/docs/reference/use-cases \
     -name "*.md" -type f | while read -r file; do
  update_frontmatter "$file"
done
