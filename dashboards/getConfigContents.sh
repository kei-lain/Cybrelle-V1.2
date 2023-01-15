#!/bin/bash

declare -A files

# Find all files with the .conf extension
for file in $(find /path/to/dir -name '*.conf'); do
    # Read the contents of each file
    contents=$(cat "$file")
    # store the file name as key and contents as value in the dictionary
    files["$file"]="$contents"
done

# Iterate over the dictionary and print the contents of each file
for key in "${!files[@]}"; do
    echo "file: $key"
    echo "contents: ${files[$key]}"
done
