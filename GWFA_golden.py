import sys
sys.path.append("C:\\Users\\bl430\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages")
import numpy as np
from tqdm import tqdm


def generate_edges_from_golden(golden_edges, TOTAL_NODES, NUM_EDGES):
    edges = [0 for _ in range(TOTAL_NODES)]  
    for i in range(0, TOTAL_NODES): 
        edge_bits = 0   

        for j in range(i+1, i+1+NUM_EDGES):
            if j < TOTAL_NODES:
                pos = j-i
                if golden_edges[j] & (1 << (pos-1)):
                    edge_bits |= (1 << (NUM_EDGES-pos))

        edges[i] = edge_bits

    return edges

 
def golden_512(golden_edges, query, nodes, NUM_NODES, NUM_EDGES):
    ans  = np.zeros((NUM_NODES+1, NUM_NODES+1)).astype(np.uint32)
    
    # boundary condition
    for i in range(NUM_NODES + 1):
        ans[i][0] = i
    
    for i in range(1, NUM_NODES+1):
        edge_bits = golden_edges[i]
        source = []

        for k in range(NUM_EDGES):
            if edge_bits & (1 << (NUM_EDGES - k - 1)): 
                source.append(ans[0][i-NUM_EDGES+k]+1)
        
        ans[0][i] = min(source)
    
    # START
    cost = 0
    for i in range(1,NUM_NODES+1):
        for j in range(1,NUM_NODES+1):

            if(query[i]==nodes[j]):
                cost = 0
            else:
                cost = 1

            edges = golden_edges[j]
            source = []

            for k in range(NUM_EDGES):
                if edges & (1 << (NUM_EDGES - k - 1)):  
                        source.append(ans[i][j-NUM_EDGES+k]+1)
                        source.append(ans[i-1][j-NUM_EDGES+k]+cost)

            source.append(ans[i-1][j]+1)   
            ans[i][j] = min(source)


    # print("golden")
    # for i in range(NUM_NODES+1):
    #     print(" ".join(str(ans[i, j]) for j in range(NUM_NODES+1)))
    # print()

    return ans[NUM_NODES][NUM_NODES], ans



def golden(golden_edges, query, nodes, TOTAL_NODES, NUM_EDGES, NUM_QRY):
    print("-----------------------------")

    ans  = np.zeros((NUM_QRY+1, TOTAL_NODES+1)).astype(np.uint32)
    
    # boundary condition
    for i in range(NUM_QRY + 1):
        ans[i][0] = i
        
    
    for i in range(1, TOTAL_NODES+1):
        edge_bits = golden_edges[i]
        source = []

        for k in range(NUM_EDGES):
            if edge_bits & (1 << (NUM_EDGES - k - 1)): 
                source.append(ans[0][i-NUM_EDGES+k]+1)
        
        ans[0][i] = min(source)
    
    print("Finish Golden initialization.")
    print("-----------------------------")
    

    # START
    # Add tqdm to show progress for the second loop (over NUM_QRY and TOTAL_NODES)
    cost = 0
    
    for i in tqdm(range(1, NUM_QRY+1), desc="Processing"):
        for j in (range(1, TOTAL_NODES+1)):
            
            if(query[i] == nodes[j]):
                cost = 0
            else:
                cost = 1

            edges = golden_edges[j]
            source = []

            for k in range(NUM_EDGES):
                if edges & (1 << (NUM_EDGES - k - 1)):  
                    source.append(ans[i][j-NUM_EDGES+k]+1)
                    source.append(ans[i-1][j-NUM_EDGES+k]+cost)

            source.append(ans[i-1][j]+1)   
            ans[i][j] = min(source)


    print("Finish Golden calculation.")
    print("-----------------------------")


    rightmost_column = ans[0:NUM_QRY+1, TOTAL_NODES] 
    bottommost_row = ans[NUM_QRY, 0:TOTAL_NODES+1]    

    min_right = np.min(rightmost_column)
    min_bottom = np.min(bottommost_row)



    if min_right <= min_bottom:
        smallest = min_right
        pos = (int(np.argmin(rightmost_column)), TOTAL_NODES)
    else:
        smallest = min_bottom
        pos = (NUM_QRY, int(np.argmin(bottommost_row)))


    print("Return Golden semi-global result.")

    return smallest, pos, ans, rightmost_column, bottommost_row


