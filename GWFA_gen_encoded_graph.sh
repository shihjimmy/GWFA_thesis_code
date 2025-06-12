#!/bin/bash
python3 GWFA_fq_trim.py 1
python3 GWFA_fq_pos_on_graph.py 1
python3 GWFA_fq_trim.py 22
python3 GWFA_fq_pos_on_graph.py 22
python3 GWFA_gfa_trim.py 1
python3 GWFA_gfa_trim.py 22

for gene in 1 22; do
    sampled_indices_file="./out_trim/chr${gene}_sampled_indices.txt"
    
    if [ -f "$sampled_indices_file" ]; then
        # Iterate over the sampled indices
        while IFS= read -r index; do
            echo "Processing gene $gene and num $index"
            python3 ./GWFA_gfa_encode.py $index $gene
            
        done < "$sampled_indices_file"
    fi
done


