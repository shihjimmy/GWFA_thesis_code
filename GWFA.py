import argparse
import GWFA_512_boundary
import GWFA_golden
import time

NUM_NODES = 256
NUM_EDGES = 6
code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}


def generate_in_edges(edges, TOTAL_NODES, NUM_EDGES):
    golden_edges = [0 for _ in range(TOTAL_NODES)]  
    for i in range(0, TOTAL_NODES): 
        edge_bits = 0   

        for j in range(i-NUM_EDGES, i):
            if j >=0 :
                pos = i-j
                if edges[j] & (1 << (NUM_EDGES - pos)):
                    edge_bits |= (1 << (pos-1))

        golden_edges[i] = edge_bits

    return golden_edges



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
    print("-----------------------------")


    print("Start Golden caculation.")
    golden_edges = generate_in_edges(edges, len(nodes), NUM_EDGES)
    # -1 for minus the begginning " " in node and query
    start_time = time.time()
    gold_edit, gold_pos, gold_ans, _, _ = GWFA_golden.golden(golden_edges, query, nodes, len(nodes)-1, NUM_EDGES, len(query)-1)
    end_time = time.time()
    elapsed_time_gold = end_time - start_time

    batch_size = NUM_NODES 
    x, y = 0, 0 
    edit_distance = 0
    path = []

    left_x, left_y = len(query), len(nodes)
    trace_x, trace_y = 0, 0


    print("-----------------------------")
    print("Start GWFA calculation.")
    print("-----------------------------")
    print("Current position of x is                     :", x)
    print("Current position of y is                     :", y)
    print("Current edit distance is                     :", edit_distance)
    print("Golden  edit distance at your position is    :", gold_ans[x][y])
    print("Traceback result can reach                   :", (trace_x, trace_y))
    print("-----------------------------")

    start_time = time.time()
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
        print("Golden  edit distance at your position is    :", gold_ans[x][y])


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


    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Execution time                               : {elapsed_time} seconds")
    print(f"Final Edit Distance                          : {edit_distance}")
    print(f"Final Ending Position                        : {(x, y)}")
    print("-----------------------------")
    print(f"Execution time for Golden                    : {elapsed_time_gold} seconds")
    print(f"Final Edit Distance(golden)                  : {gold_edit}")
    print(f"Final Ending Position(golden)                : {gold_pos}")
    print("-----------------------------")

    
    gold_edit = int(gold_edit)
    edit_distance = int(edit_distance)
    precision = (1 - abs(gold_edit - edit_distance) / gold_edit) * 100
    print(f"Precision = abs(Golden-Yours) / Golden       : {precision:.4f} %")
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
    
    parser.add_argument('fa_file' , type=str, help="Path to the .fa file")
    parser.add_argument('truncated_gfa_file', type=str, help="Path to the truncated gfa file (.txt)")

    args     = parser.parse_args()
    gfa_file = args.truncated_gfa_file
    fa_file  = args.fa_file

    GWFA(fa_file, gfa_file)

