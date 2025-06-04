import argparse
import numpy as np
import GWFA_512_boundary

NUM_NODES = 512
NUM_EDGES = 6
code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}


def GWFA(query_path, gfa_path):
    nodes = [code_to_base[4]]
    query = [code_to_base[4]]
    edges = [1<<(NUM_EDGES-1)]


    with open(gfa_path, 'r') as f:
        for line in f:
            binary_data = line.strip() 
            nodes.append(code_to_base[ int(binary_data[:2], 2) ])
            edges.append(int(binary_data[2:], 2))

    
    with open(query_path, 'r') as f:
        lines = f.readlines()
        sequence = lines[1].strip()
        
        for base in sequence:
            query.append(base)

    print(f"There are {len(nodes)} genome in the graph")
    print(f"There are {len(query)} genome in the sequence")
    print()
    
    
    batch_size = NUM_NODES 
    x, y = 0, 0 

    print("Current position of x is :", x)
    print("Current position of y is :", y)
    print("-----------------------------")

    edit_distance = 0
    path = []

    while x < len(query)-1 and y < len(nodes)-1:
        
        batch_query = query[x:x + batch_size]
        batch_nodes = nodes[y:y + batch_size]
        batch_edges = edges[y:y + batch_size]
        
        score, traceback, (end_x, end_y), _ = GWFA_512_boundary.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, (x == 0 and y == 0))
        x += end_x
        y += end_y

        print("Current position of x is :", x)
        print("Current position of y is :", y)
        print("-----------------------------")


        edit_distance += score
        path.append(traceback)

    print(f"Final Edit Distance: {edit_distance}")
    #print(f"Path: {path}")
    
        
        
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="GWFA")
    parser.add_argument('truncated_gfa_file', type=str, help="Path to the truncated gfa file (.txt)")
    parser.add_argument('fa_file' , type=str, help="Path to the .fa file")

    args     = parser.parse_args()
    gfa_file = args.truncated_gfa_file
    fa_file  = args.fa_file

    GWFA(fa_file, gfa_file)

