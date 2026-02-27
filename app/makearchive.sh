#!/bin/bash

for dir in data/out/*/; do
    # Remove trailing slash from directory name
    dirname="${dir%/}"
    
    # Skip if not a directory
    [ -d "$dirname" ] || continue
    
    # Extract just the base directory name (e.g., "edrdev" from "data/out/edrdev")
    basename=$(basename "$dirname")
    
    # Create zip file for the directory (only .md files)
    echo "Creating ${basename}.zip..."
    zip -r "data/result/${basename}.zip" "$dirname" -i '*.md'
done

echo "Done! Created zip files for all subdirectories."
