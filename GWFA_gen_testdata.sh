#!/bin/bash
rm -rf ./out_trim/*
python3 GWFA_gen_testdata.py 1
python3 GWFA_gen_testdata.py 22


#!/bin/bash

# Clear out the out_trim folder
rm -rf ./out_trim/*

# Iterate through all subdirectories starting with "out_sequence_"
for dir in ./out_sequence_*; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        # Extract the chromosome number from the directory name
        chrom=$(basename "$dir" | sed 's/out_sequence_//')

        echo "Processing directory: $dir for chromosome: $chrom"

        # Run your Python scripts for each directory
        python3 GWFA_gen_testdata.py $chrom
        python3 GWFA_gen_testdata.py $chrom  # Run it again or adjust as needed

    fi
done

echo "All test cases have been processed."
