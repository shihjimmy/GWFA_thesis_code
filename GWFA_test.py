import numpy as np
import random
import GWFA_512_boundary
import GWFA_golden

NUM_NODES = 512
NUM_EDGES = 6
TOTAL_NODES = 2550
NUM_QRY = 512
code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}


def GWFA_test():

    # for boundary conditions
    nodes        = []
    golden_edges = []
    query        = []
    nodes.append(4)
    query.append(4)
    golden_edges.append(0)
    golden_edges.append(1)
    
    random.seed(421)

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


    # setting for out-edges
    edges = GWFA_golden.generate_edges_from_golden(golden_edges, TOTAL_NODES+1, NUM_EDGES)
    

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
        
        score, traceback, (end_x, end_y), _ = GWFA_512_boundary.GWFA_512_x_512_boundary(batch_nodes, batch_edges, batch_query, x==0 and y==0, NUM_NODES, NUM_EDGES)
        x += end_x 
        y += end_y
            
        print("Current position of x is :", x)
        print("Current position of y is :", y)
        print("-----------------------------")

        edit_distance += score
        path.append(traceback)

    
    
    print(f"Final Edit Distance: {edit_distance}")
    print(f"Final Ending Position: {(x, y)}")
    
    final_trace_result = ""
    for segment in path:
        for step in segment:
            final_trace_result+=step
            
    print("Your traceback result: ")
    print(final_trace_result)
    print("-----------------------------")
    
    
    
    gold_edit, gold_pos, gold_ans, _, _ = GWFA_golden.golden(golden_edges, query, nodes, TOTAL_NODES, NUM_EDGES, NUM_QRY)
    print(f"Final Edit Distance(golden): {gold_edit}")
    print(f"Final Ending Position(golden): {gold_pos}")
    print("-----------------------------")
    
    gold_edit = int(gold_edit)
    edit_distance = int(edit_distance)
    precision = (1 - abs(gold_edit - edit_distance) / gold_edit) * 100
    print(f"Precision = abs(Golden-Yours) / Golden = {precision:.4f} %")
    print("-----------------------------")
    
    
    return gold_ans, final_trace_result




if __name__ == "__main__":
    gold_ans, final_trace_result = GWFA_test()

