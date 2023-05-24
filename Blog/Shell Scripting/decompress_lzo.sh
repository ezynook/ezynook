#!/bin/bash

# Set input and output directories
input_dir="/root"
output_dir="/home/lzo"

if []; then
    echo "Empty LZO File"
    exit 1
fi

# Loop over input files in the input directory
for input_file in "$input_dir"/*.lzo; do
    # Set the output file name based on the input file name
    #output_file="$output_dir/$(basename "${input_file%.lzo}.csv")"
    output_file="$output_dir/$(basename "${input_file%}.csv")"

    # Decompress the input file and save the output to a temporary file
    temp_file=$(mktemp)
    lzop -dc "$input_file" > "$temp_file"

    # Rename the temporary file to the desired output file name
    mv "$temp_file" "$output_file"

    # Remove the input file
    rm "$input_file"
done
