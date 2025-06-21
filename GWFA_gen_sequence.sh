# Run under ./GWFA folder

for dir in ./out_sequence_*; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        echo "Clearing contents of directory: $dir"
        rm -rf "$dir"/*  # Remove all files inside the directory but keep the directory
    fi
done


# 1024 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 1024 --prefix ./out_sequence_1k/chr1_pbsim3_1k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 1024 --prefix ./out_sequence_1k/chr22_pbsim3_1k

gzip -d ./out_sequence_1k/chr1_pbsim3_1k_0001.fq.gz
gzip -d ./out_sequence_1k/chr1_pbsim3_1k_0001.maf.gz

gzip -d ./out_sequence_1k/chr22_pbsim3_1k_0001.fq.gz
gzip -d ./out_sequence_1k/chr22_pbsim3_1k_0001.maf.gz

# 5000 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 5000 --prefix ./out_sequence_5k/chr1_pbsim3_5k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 5000 --prefix ./out_sequence_5k/chr22_pbsim3_5k

gzip -d ./out_sequence_5k/chr1_pbsim3_5k_0001.fq.gz
gzip -d ./out_sequence_5k/chr1_pbsim3_5k_0001.maf.gz

gzip -d ./out_sequence_5k/chr22_pbsim3_5k_0001.fq.gz
gzip -d ./out_sequence_5k/chr22_pbsim3_5k_0001.maf.gz


# 10240 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 10240 --prefix ./out_sequence_10k/chr1_pbsim3_10k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 10240 --prefix ./out_sequence_10k/chr22_pbsim3_10k

gzip -d ./out_sequence_10k/chr1_pbsim3_10k_0001.fq.gz
gzip -d ./out_sequence_10k/chr1_pbsim3_10k_0001.maf.gz

gzip -d ./out_sequence_10k/chr22_pbsim3_10k_0001.fq.gz
gzip -d ./out_sequence_10k/chr22_pbsim3_10k_0001.maf.gz


# 15000 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 15000 --prefix ./out_sequence_15k/chr1_pbsim3_15k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 15000 --prefix ./out_sequence_15k/chr22_pbsim3_15k

gzip -d ./out_sequence_15k/chr1_pbsim3_15k_0001.fq.gz
gzip -d ./out_sequence_15k/chr1_pbsim3_15k_0001.maf.gz

gzip -d ./out_sequence_15k/chr22_pbsim3_15k_0001.fq.gz
gzip -d ./out_sequence_15k/chr22_pbsim3_15k_0001.maf.gz


# 20480 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 20480 --prefix ./out_sequence_20k/chr1_pbsim3_20k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 20480 --prefix ./out_sequence_20k/chr22_pbsim3_20k

gzip -d ./out_sequence_20k/chr1_pbsim3_20k_0001.fq.gz
gzip -d ./out_sequence_20k/chr1_pbsim3_20k_0001.maf.gz

gzip -d ./out_sequence_20k/chr22_pbsim3_20k_0001.fq.gz
gzip -d ./out_sequence_20k/chr22_pbsim3_20k_0001.maf.gz

# 40480 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 40480 --prefix ./out_sequence_40k/chr1_pbsim3_40k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 40480 --prefix ./out_sequence_40k/chr22_pbsim3_40k

gzip -d ./out_sequence_40k/chr1_pbsim3_40k_0001.fq.gz
gzip -d ./out_sequence_40k/chr1_pbsim3_40k_0001.maf.gz

gzip -d ./out_sequence_40k/chr22_pbsim3_40k_0001.fq.gz
gzip -d ./out_sequence_40k/chr22_pbsim3_40k_0001.maf.gz


# 80480 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 80480 --prefix ./out_sequence_80k/chr1_pbsim3_80k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 80480 --prefix ./out_sequence_80k/chr22_pbsim3_80k

gzip -d ./out_sequence_80k/chr1_pbsim3_80k_0001.fq.gz
gzip -d ./out_sequence_80k/chr1_pbsim3_80k_0001.maf.gz

gzip -d ./out_sequence_80k/chr22_pbsim3_80k_0001.fq.gz
gzip -d ./out_sequence_80k/chr22_pbsim3_80k_0001.maf.gz


# 102400 and error rate = 15%
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr1.fasta   --accuracy-mean 0.85 --length-mean 100480 --prefix ./out_sequence_100k/chr1_pbsim3_100k
../pbsim3/src/pbsim --strategy wgs --method qshmm --qshmm ../pbsim3/data/QSHMM-RSII.model --depth 1 --genome ./Genome_data/GRCh38_chr22.fasta  --accuracy-mean 0.85 --length-mean 100480 --prefix ./out_sequence_100k/chr22_pbsim3_100k

gzip -d ./out_sequence_100k/chr1_pbsim3_100k_0001.fq.gz
gzip -d ./out_sequence_100k/chr1_pbsim3_100k_0001.maf.gz

gzip -d ./out_sequence_100k/chr22_pbsim3_100k_0001.fq.gz
gzip -d ./out_sequence_100k/chr22_pbsim3_100k_0001.maf.gz
