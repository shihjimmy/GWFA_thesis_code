#!/bin/bash

# Iterate over all subdirectories starting with "out_trim_"
for dir in ./out_trim_*; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        echo "Processing data in directory: $dir"
        len=$(basename "$dir" | sed 's/out_trim_//')
        
        # Set the directory for test cases
        TEST_CASE_FOLDER="$dir"
        OUTPUT_FILE="GWFA_${len}.txt"  

        # If the results file already exists, remove it
        if [ -f "$OUTPUT_FILE" ]; then
            rm "$OUTPUT_FILE"
        fi

        # Iterate over all files in the test case folder
        for fa_file in "$TEST_CASE_FOLDER"/*.fa; do
            # Extract the base name of the file (e.g., "1" from "1.fq")
            base_name=$(basename "$fa_file" .fa)

            # Find the corresponding .gfa file
            gfa_file="$TEST_CASE_FOLDER/${base_name}_truncate_to_6.txt"

            # Check if the corresponding .gfa file exists
            if [ -f "$gfa_file" ]; then
                echo "Running test case pair: $fa_file and $gfa_file"
                echo "Running test case pair: $fa_file and $gfa_file" >> "$OUTPUT_FILE"

                python3 GWFA.py "$fa_file" "$gfa_file" >> "$OUTPUT_FILE" 2>&1

                echo "-----------------------------" >> "$OUTPUT_FILE"
                echo "                             " >> "$OUTPUT_FILE"
                echo "                             " >> "$OUTPUT_FILE"
                echo "                             " >> "$OUTPUT_FILE"
                echo "                             " >> "$OUTPUT_FILE"
                echo "                             " >> "$OUTPUT_FILE"
                echo "-----------------------------" >> "$OUTPUT_FILE"
            else
                echo "Warning: No matching .gfa file found for $fa_file"
            fi
        done

        echo "All test cases for $dir have been processed. Results saved to $OUTPUT_FILE."

        # Run the GWFA_extract_ans.py script after processing the files in the current folder
        python3 GWFA_extract_ans.py $len
    fi
done

echo "All test cases have been processed. Results saved to respective directories."
