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
