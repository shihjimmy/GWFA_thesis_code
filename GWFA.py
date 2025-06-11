import argparse
import GWFA_512_boundary

NUM_NODES = 256
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


    print("-----------------------------")
    print(f"There are {len(nodes)} genome in the graph")
    print(f"There are {len(query)} genome in the sequence")
    
    
    batch_size = NUM_NODES 
    x, y = 0, 0 
    edit_distance = 0
    path = []

    left_x, left_y = len(query), len(nodes)
    trace_x, trace_y = 0, 0


    print("-----------------------------")
    print("Start GWFA caculation.")
    print("-----------------------------")
    print("Current position of x is                     :", x)
    print("Current position of y is                     :", y)
    print("Current edit distance is                     :", edit_distance)
    print("-----------------------------")

 
    
    
    while x < len(query)-1 and y < len(nodes)-1:
        
        batch_query = query[x:x + batch_size]
        batch_nodes = nodes[y:y + batch_size]
        batch_edges = edges[y:y + batch_size]
        
        beginning = x==0 and y==0
        last = batch_size >= (left_x) or batch_size >= (left_y)
        
        score, traceback, (end_x, end_y) = GWFA_512_boundary.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, beginning, last, NUM_NODES, NUM_EDGES)
        
        x += end_x 
        y += end_y
        left_x -= (end_x+1)
        left_y -= (end_y+1)
        
        edit_distance += (score)
        

        for move in traceback:
            path.append(move)


        print("Current position of x is                     :", x)
        print("Current position of y is                     :", y)
        print("Current edit distance is                     :", edit_distance)
        print("-----------------------------")


        """ Check traceback """
        for move in traceback:
            num = int(move[0])
            direction = move[1]
            
            if direction == 'M' or direction == 'U':
                trace_x += 1
                trace_y += num
            
            elif direction == 'I':
                trace_x += 1
            
            else:
                trace_y += num
        
        print("Traceback result can reach                   :", (trace_x, trace_y))
        print("-----------------------------")



    print(f"Final Edit Distance                          : {edit_distance}")
    print(f"Final Ending Position                        : {(x, y)}")
    print("-----------------------------")



    check = 0
    final_trace_result = ""
    
    for move in path:
        final_trace_result += move
        
        if move[1] == 'U' or move[1] == 'I' or move[1] == 'D':
            check += 1
            
    print(f"Your MIS/INS/DEL times                       : {check}")
    
    
    if check == edit_distance:
        print("Your Traceback result matches with your edit distance!")
    else:
        print("There are some errors in Traceback.")
    
    
    print("Your traceback result                        : ")
    print(final_trace_result)
    print("-----------------------------")
    
        
        
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="GWFA")
    parser.add_argument('truncated_gfa_file', type=str, help="Path to the truncated gfa file (.txt)")
    parser.add_argument('fa_file' , type=str, help="Path to the .fa file")

    args     = parser.parse_args()
    gfa_file = args.truncated_gfa_file
    fa_file  = args.fa_file

    GWFA(fa_file, gfa_file)

