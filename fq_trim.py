import argparse


parser = argparse.ArgumentParser(description="fq_trim")
parser.add_argument('chrom', type=str, help="chromosome")

args     = parser.parse_args()
chrom    = args.chrom


f = open(f"./out_sequence/chr{chrom}_pbsim3.fq", "r")
f2 = open(f"./out_sequence/chr{chrom}_pbsim3.maf", "r")
lines = f.readlines()
lines_maf = f2.readlines()
f.close()
f2.close()

f = open(f"./pbsim3_trim/pbsim3_chr{chrom}_trim.txt", "w", newline='\n') #　Need to change to .fastq by hand
f2 = open(f"./pbsim3_trim/pbsim3_chr{chrom}_start_pos.txt", "w", newline='\n')

num_reads = len(lines)//4
after_trim = 1

lengths = [0 for i in range(10)]

for i in range(num_reads):
    lengths[ min(len(lines[4*i+1])//1024, 9) ] += 1

    if "N" not in lines[4*i+1]:
        # remove character beyond "ATCG"
        lines[4*i+1] = "".join([c for c in lines[4*i+1] if c in "ATCG\n"])
        lines[(4*i)+3] = lines[(4*i)+3][:len(lines[(4*i)+1])-1] + "\n"
        f.writelines([f"@S1_{after_trim}\n", lines[(4*i)+1], f"+S1_{after_trim}\n", lines[(4*i)+3]])

        # write the start position on reference of this read
        lines_maf[(4*i)+1] = [i for i in lines_maf[(4*i)+1].split(" ") if i != '']
        lines_maf[(4*i)+2] = [i for i in lines_maf[(4*i)+2].split(" ") if i != '']

        #print(lines_maf[4*i+1])
        f2.write(f"S1_{after_trim} {lines_maf[(4*i)+1][2]} {lines_maf[(4*i)+1][3]} {lines_maf[(4*i)+2][4]}\n")
        after_trim += 1

f.close()
f2.close()
print("fq_trim is finished")
#print(num_reads, after_trim)
