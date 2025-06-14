import random
import GWFA_512_boundary
import GWFA_golden
import time
from GWFA_plot import flatten_path, create_resizable_matrix_gui

code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}

""" 
    Can try different combination
"""
NUM_EDGES = 6       #   edges in graph
TOTAL_NODES = 500   #   graph
NUM_QRY = 500       #   query


""" 
    NUM_NODES, which is a batch size for GWFA PE
    affect the precision significantly
"""

NUM_NODES = 256
ANS_NODES = max(NUM_QRY, TOTAL_NODES)



def GWFA_test(check_golden_GWFA = False):

    # for boundary conditions
    nodes        = []
    golden_edges = []
    query        = []
    nodes.append(4)
    query.append(4)
    golden_edges.append(0)
    golden_edges.append(1)
    
    random.seed(420)

    for i in range(0, TOTAL_NODES):
        base_code = random.getrandbits(2)              
        nodes.append(base_code)

    for i in range(0, NUM_QRY):
        qry = random.getrandbits(2)
        query.append(qry)


    # setting for in-edges
    for i in range(1, TOTAL_NODES):       
        if i <= NUM_EDGES:     
            edge_bits = random.randint(1, 2**i-1)
        else:
            edge_bits = random.randint(1, 2**NUM_EDGES-1)
        
        golden_edges.append(edge_bits)
    

    start_time = time.time()
    gold_edit, gold_pos, gold_ans, _, _ = GWFA_golden.golden(golden_edges, query, nodes, TOTAL_NODES, NUM_EDGES, NUM_QRY)
    end_time = time.time()
    elapsed_time_gold = end_time - start_time
    
    
    # setting for out-edges
    edges = GWFA_golden.generate_edges_from_golden(golden_edges, TOTAL_NODES+1, NUM_EDGES)
    

    batch_size = NUM_NODES 
    x, y = 0, 0 
    left_x, left_y = len(query), len(nodes)
    edit_distance = 0

    path = []
    trace_x, trace_y = 0, 0
    
    breakpoints = []
    breakpoints.append((x,y))


    print("-----------------------------")
    print("Start GWFA caculation.")
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
        
        
        breakpoints.append((x, y))
        
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
    

    gwfa_score = 0
    gwfa_traceback = []
    gwfa_end_x = 0
    gwfa_end_y = 0


    if check_golden_GWFA:
        print("Start Golden GWFA calculation.")
        print("-----------------------------")
    
        gwfa_score, gwfa_traceback, (gwfa_end_x, gwfa_end_y) = GWFA_512_boundary.GWFA_512_x_512_boundary(nodes, edges, query, True, True, ANS_NODES, NUM_EDGES)


        print("Finish Golden GWFA calculation.")
        print("-----------------------------")
    

    return gold_ans, gold_pos, path, (x, y), breakpoints, gwfa_score, gwfa_traceback, (gwfa_end_x, gwfa_end_y)


if __name__ == "__main__":
    """ 
        Want to generate golden path in perfect GWFA mode or not
    """
    
    check_golden_GWFA = False 

    gold_ans, gold_pos, path, final_ending_pos, breakpoints, gwfa_score, gwfa_traceback, (gwfa_end_x, gwfa_end_y) = GWFA_test(check_golden_GWFA)


    """ 
        Generate a GUI surface for the calculation result (debug)
    """
    debug = False
    
    if debug:
        rows = gold_ans.shape[0]
        cols = gold_ans.shape[1]

        # Flatten the path to convert directions into coordinates
        pos_path = flatten_path(path)
        gwfa_path = flatten_path(gwfa_traceback)

        # Call the function with the flattened path, gold_ans, breakpoints, and both final and gold positions
        create_resizable_matrix_gui(rows, cols, gold_ans, gold_pos, pos_path, final_ending_pos, breakpoints, gwfa_path)
