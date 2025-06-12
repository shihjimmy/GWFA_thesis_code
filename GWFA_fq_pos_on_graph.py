import argparse
from tqdm import tqdm

def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left+1 < right:
        mid = (left + right) // 2
        # print(left, right, mid)
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid
        else:
            right = mid

    return left



parser = argparse.ArgumentParser(description="fq_pos")
parser.add_argument('chrom', type=str, help="chromosome")

args     = parser.parse_args()
chrom    = args.chrom


# read graphs
f = open(f"./out_graph/chr{chrom}.gfa", "r")
lines = f.readlines()
f.close()

nodes = dict()

for i in tqdm(lines[1::], desc="Processing Lines"):
    line = i[0:-1].split()

    if line[0] == "S":
        nodes[int(line[1])] = line[2]
        
    # path of main sequence
    elif line[0] == "P":
        path = line[2].split("+,")
        path[-1] = path[-1][:-1]



# position of node on reference
path_accu_len = [0 for i in range(len(path))]
temp = 0

for i in range(len(path)):
    path_accu_len[i] = temp
    temp += len(nodes[int(path[i])])
        




f = open(f"./pbsim3_trim/pbsim3_chr{chrom}_start_pos.txt", "r")
lines = f.readlines()
f.close()

f = open(f"./pbsim3_trim/pbsim3_chr{chrom}_pos_on_graph.txt", "w")

for i in tqdm(lines, desc="Processing"):
    i = i.split(" ")

    start_node = binary_search(path_accu_len, int(i[1]))
    start_offset = int(i[1]) - path_accu_len[start_node]

    end_node = binary_search(path_accu_len, int(i[1])+int(i[2]))
    end_offset = int(i[1])+int(i[2]) - path_accu_len[end_node]
    
    f.write(f"{i[0]} {path[start_node]} {start_offset} {path[end_node]} {end_offset} {i[3]}")


f.close()
print("fq_pos is finished")
