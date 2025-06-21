import vg_pb2

def generate_gam_format(seq_name, start_node):
    # Create a Position message
    alignment_position = vg_pb2.Position(
        node_id=start_node,
        offset=0,
        is_reverse=False,
    )

    # Create a Mapping message using the Position
    alignment_mapping = vg_pb2.Mapping(
        position=alignment_position
    )

    # Wrap the alignment_mapping in a list as the Path expects an iterable (list)
    alignment_path = vg_pb2.Path(
        mapping=[alignment_mapping]  # Pass the mapping as a list
    )

    # Create the Alignment message
    alignment = vg_pb2.Alignment(
        path=alignment_path, 
        name=seq_name,
        query_position=0,
    )

    return alignment


def write_gam_to_file(sampled_indices_file, start_pos_graph_file, output_folder, chrom):

    with open(sampled_indices_file, 'r') as sampled_file:
        sampled_indices = [line.strip() for line in sampled_file.readlines()]

    with open(start_pos_graph_file, 'r') as graph_file:
        graph_lines = graph_file.readlines()

    # Iterate over each sampled index
    for index in sampled_indices:
        # Create a new file for each index
        output_file = f"{output_folder}/chr{chrom}_S1_{index}_gam_file.gam"
        
        # Open the corresponding file in write-binary mode
        with open(output_file, 'wb') as f_out:
            for line in graph_lines:
                # Format start_index to match the line in the graph file
                start_index = "S1_" + str(int(index))

                if line.startswith(start_index):
                    parts = line.strip().split()

                    seq_name = parts[0]
                    start_node = int(parts[1])

                    # Generate the GAM format for the specific index
                    alignment = generate_gam_format(seq_name, start_node)
                    print(f"Serialized Alignment: {alignment}")

                    # Write the serialized GAM data to the corresponding file
                    f_out.write(alignment.SerializeToString())

                    print(f"Generated GAM for {seq_name} with start node {start_node}, saved to {output_file}")

chrom = 1
start_pos_graph_file = f"./pbsim3_trim_1k/pbsim3_chr{chrom}_pos_on_graph.txt"
sampled_indices_file = f"./out_trim_1k/chr{chrom}_sampled_indices.txt"
output_folder = "./out_trim_1k"  # Specify your output folder here

# Call the function to write the GAM files
write_gam_to_file(sampled_indices_file, start_pos_graph_file, output_folder, chrom)

