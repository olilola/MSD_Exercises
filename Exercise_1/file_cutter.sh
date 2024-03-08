#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file output_file"
    exit 1
fi

input_file="$1"
output_file="$2"

# Count the total number of lines in the input file
total_lines=$(wc -l < "$input_file")

# Calculate 5% of the total number of lines
percentage=$((total_lines / 20))

# Use shuf command to randomly select lines from the input file
# and save them to the output file
shuf -n "$percentage" "$input_file" > "$output_file"

echo "Selected $percentage lines randomly from $input_file and saved to $output_file"
