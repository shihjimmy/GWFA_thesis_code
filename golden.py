import numpy as np

NUM_NODES = 512
NUM_EDGES = 6
TOTAL_NODES = 4000
NUM_QRY = 2000

def golden(golden_edges, query, nodes, TOTAL_NODES, NUM_EDGES, NUM_QRY):
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
                source.append(ans[0][i-NUM_EDGES+k]+1)
        
        ans[0][i] = min(source)
    
    # START
    cost = 0
    for i in range(1,NUM_QRY+1): 
        for j in range(1,TOTAL_NODES+1):

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

    rightmost_column = ans[1:NUM_QRY+1, TOTAL_NODES] 
    bottommost_row = ans[NUM_QRY, 1:TOTAL_NODES+1]    

    min_right = np.min(rightmost_column)
    min_bottom = np.min(bottommost_row)

    if min_right <= min_bottom:
        smallest = min_right
        pos = (int(np.argmin(rightmost_column)), TOTAL_NODES-1)
    else:
        smallest = min_bottom
        pos = (NUM_QRY-1, int(np.argmin(bottommost_row)))

    return smallest, pos, ans, rightmost_column, bottommost_row
