#!/bin/bash

TEST_CASE_FOLDER="./out_trim"  
OUTPUT_FILE="GWFA_golden.txt"  

# If the results file already exists, remove it
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
fi

# Iterate over all files in the test case folder
for fa_file in "$TEST_CASE_FOLDER"/*.fa; do
    # Extract the base name of the file (e.g., "1" from "1.fq")
    base_name=$(basename "$fa_file" .fa)
    
    # Find the corresponding .gfa file
    gfa_file="$TEST_CASE_FOLDER/$base_name.gfa"
    
    # Check if the corresponding .gfa file exists
    if [ -f "$gfa_file" ]; then
        echo "Running test case pair: $fa_file and $gfa_file" 
        echo "Running test case pair: $fa_file and $gfa_file" >> "$OUTPUT_FILE"
        
        # Capture the result and execution time
        time ./gwfa-master/gwf-test "$gfa_file" "$fa_file" >> "$OUTPUT_FILE"
        echo "------------------------------------" >> "$OUTPUT_FILE"
    else
        echo "Warning: No matching .gfa file found for $fa_file"
    fi
done

echo "All test cases have been processed. Results saved to $OUTPUT_FILE."
