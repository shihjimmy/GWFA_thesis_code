import random
import argparse

def read_and_split_file(file_path, delimiter=" "):
    result = []
    
    with open(file_path, 'r') as file:
        for line in file:
            split_line = line.strip().split(delimiter)
            result.append(split_line)
    
    return result


def extract_gfa_data(gfa_lines, start, pos):
    nodes = []
    edges = []
    
    for line in gfa_lines:
        if line.startswith('S'):  
            parts = line.split()
            node_id = int(parts[1])
            
            if start <= node_id <= pos:
                nodes.append(parts)
                
        elif line.startswith('L'): 
            parts = line.split()
            node1 = int(parts[1])
            node2 = int(parts[3])

            if node1 >= start and node2 <= pos:
                edges.append(parts)

    return nodes, edges



def write_to_file(start_pos_data, gfa_lines, chrom):
    random.seed(120)
    sampled_indices = random.sample(range(len(start_pos_data)), min(10, len(start_pos_data)))

    with open(f"./out_sequence/chr{chrom}_pbsim3.fq", "r") as f:
        fq_lines = f.readlines()

    # Create a file to save sampled indices
    sampled_indices_file = f"./out_trim/chr{chrom}_sampled_indices.txt"
    
    # Write the sampled indices to the file
    with open(sampled_indices_file, 'w') as idx_file:
        for idx in sampled_indices:
            idx_file.write(f"{idx+1}\n")
    
    for idx in sampled_indices:
        start_pos = start_pos_data[idx] 
        name = start_pos[0]
        start = int(start_pos[1])
        pos = int(start_pos[3])

        nodes_in_range, edges_in_range = extract_gfa_data(gfa_lines, start, pos)

        file_name = f"./out_trim/chr{chrom}_{name}.gfa"
        sequence_file_name = f"./out_trim/chr{chrom}_{name}.fa" 
        
        with open(file_name, 'w') as f:
            for node in nodes_in_range:
                f.write("\t".join(str(x) for x in node) + "\n")
            
            for edge in edges_in_range:
                f.write("\t".join(str(x) for x in edge) + "\n")
        
        with open(sequence_file_name, 'w') as seq_file:
            sequence = fq_lines[4*idx + 1].strip()
            seq_file.write(f">{name}\n{sequence}\n")
            
        print(f"Data for start={name} written to {file_name} and sequence written to {sequence_file_name}")

    # Confirm that sampled indices have been saved
    print(f"Sampled indices saved to {sampled_indices_file}")




parser = argparse.ArgumentParser(description="gfa_trim")
parser.add_argument('chrom', type=str, help="chromosome")

args     = parser.parse_args()
chrom    = args.chrom

f = open(f"./out_graph/chr{chrom}.gfa", "r")
gfa_lines = f.readlines()
f.close()

start_pos_data = read_and_split_file(f"./pbsim3_trim/pbsim3_chr{chrom}_pos_on_graph.txt")
write_to_file(start_pos_data, gfa_lines, chrom)
print("gfa_trim is finished")
    
