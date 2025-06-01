import numpy as np
import argparse

code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}
NUM_EDGES = 6


parser = argparse.ArgumentParser(description="gfa_encode")
parser.add_argument('num', type=str, help="chromosome")
parser.add_argument('gene', type=str, help="genome")

args   = parser.parse_args()
num    = args.num
gene   = args.gene

file_path = f"./out_trim/chr{gene}_S1_{num}.gfa"

if ".gfa" in file_path:
    prefix = file_path.split(".gfa")[0]
out_path = prefix + f"_truncate_to_{NUM_EDGES}.txt"

f = open(file_path, "r")
lines = f.readlines()
f.close()

nodes = dict()
edges = dict()

for i in lines:
    line = i[0:-1].split('\t')

    if line[0] == "S":
        nodes[int(line[1])] = line[2]

    elif line[0] == "L":
        start = int(line[1])
        end   = int(line[3])

        # after vg's generation, it should be a DAG
        if (end < start):
            print("reverse edge", line)
            break
        try:
            edges[start].append(end)
        except:
            edges[start] = [end]


nodes = dict(sorted(nodes.items()))
#print(nodes)
#print(edges)

node_edge_bits = []

for i, node_id in enumerate(nodes):
    edge_bits = 0

    for i in range(len(nodes[node_id])-1):
        if nodes[node_id][i] == 'A':
            edge_bits = 0 | (1 << NUM_EDGES-1)
        elif nodes[node_id][i] == 'T':
            edge_bits = (1 << NUM_EDGES) | (1 << NUM_EDGES-1)
        elif nodes[node_id][i] == 'C':
            edge_bits = (2 << NUM_EDGES) | (1 << NUM_EDGES-1)
        else:
            edge_bits = (3 << NUM_EDGES) | (1 << NUM_EDGES-1)

        node_edge_bits.append(edge_bits)


    if nodes[node_id][-1] == 'A':
        edge_bits = 0 
    elif nodes[node_id][-1] == 'T':
        edge_bits = (1 << NUM_EDGES) 
    elif nodes[node_id][-1] == 'C':
        edge_bits = (2 << NUM_EDGES) 
    else:
        edge_bits = (3 << NUM_EDGES) 


    if node_id in edges:
        count = 0
        accum = 0
        num_neighbors = len(edges[node_id])  

        for idx, neighbor in enumerate(edges[node_id]):  

            edge_bits |= (1 << (NUM_EDGES - count - 1))
            length = len(nodes[neighbor])
            accum += length

            if accum > NUM_EDGES:
                break
    
            count += 1

        node_edge_bits.append(edge_bits)
    
    

with open(out_path, 'w') as out_file:
    for bits in node_edge_bits:
        binary_edge_bits = bin(bits)[2:].zfill(NUM_EDGES+2)
        out_file.write(f"{binary_edge_bits}\n")


print(f"Edge bits have been written to {out_path}")

