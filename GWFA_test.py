import numpy as np
import random
from collections import deque
import GWFA_512_boundary
import GWFA_512_retreat
import GWFA_512_preload
import GWFA_golden


NUM_NODES = 50
NUM_EDGES = 6
TOTAL_NODES = 510
NUM_QRY = 250
code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}

RETREAT_STEP = 3




def GWFA_test():

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
        
        
        
    gold_edit, gold_pos, gold_ans, col, row = GWFA_golden.golden(golden_edges, query, nodes, TOTAL_NODES, NUM_EDGES, NUM_QRY)
    
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
    
    
    #preload_pos = deque()

    print("-----------------------------")
    print("Current position of x is                     :", x)
    print("Current position of y is                     :", y)
    print("Current edit distance is                     :", edit_distance)
    print("Golden  edit distance at your position is    :", gold_ans[x][y])
    print("-----------------------------")

    
    while x < len(query)-1 and y < len(nodes)-1:
        
        batch_query = query[x:x + batch_size]
        batch_nodes = nodes[y:y + batch_size]
        batch_edges = edges[y:y + batch_size]
        
        beginning = x==0 and y==0
        last = batch_size >= (left_x) or batch_size >= (left_y)
        
        score, traceback, (end_x, end_y) = GWFA_512_boundary.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, beginning, last, NUM_NODES, NUM_EDGES)
        #score, traceback, (end_x, end_y) = GWFA_512_retreat.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, beginning, NUM_NODES, NUM_EDGES)
        
        
        # score, traceback, (end_x, end_y), preload_pos, min_x, min_y = GWFA_512_preload.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, beginning, last, NUM_NODES, NUM_EDGES, RETREAT_STEP, preload_pos)
        
        # x += min_x 
        # y += min_y
        # left_x -= (min_x+1)
        # left_y -= (min_y+1)
        
        
        # # Print the golden values for x range: x to x + end_x and y range: y to y + end_y
        # print(f"Golden values for x range: {x} to {x + end_x}")
        # print(f"Golden values for y range: {y} to {y + end_y}")

        # # Print the 2D matrix in a square format
        # for i in range(x, x + end_x+1):
        #     row_values = []
        #     for j in range(y, y + end_y+1):
        #         row_values.append(str(gold_ans[i][j]))  # Collect each element as a string
        #     print(" ".join(row_values))  # Print the row with tab separation
        
        # print(traceback)
        
        x += end_x 
        y += end_y
        left_x -= (end_x+1)
        left_y -= (end_y+1)
        
        edit_distance += (score)
        path.append(traceback)
        
        
        breakpoints.append((x, y))
        
        print("Current position of x is                     :", x)
        print("Current position of y is                     :", y)
        print("Current edit distance is                     :", edit_distance)
        print("Golden  edit distance at your position is    :", gold_ans[x][y])
        
        
        # if  (x < len(query)-1 and y < len(nodes)-1):
        #     # need to minus 1
        #     # due to the 1 overlapping genome
        #     # we start next batch from x, y
        #     # But previous batch just stops at x, y
        #     edit_distance -= 1
        
        
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
    
    for seg in path:
        for move in seg:
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
    
    return gold_ans, gold_pos, path, (x, y), breakpoints





if __name__ == "__main__":
    gold_ans, gold_pos, path, final_ending_pos, breakpoints = GWFA_test()
    
    # output_file = "GWFA_gold_ans.txt"
    
    # with open(output_file, 'w') as f:
    #     for row in gold_ans:
    #         f.write("\t".join(str(cell) for cell in row) + "\n")
        
    # print(f"gold_ans has been written to {output_file}")


