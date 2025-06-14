import random
import numpy as np
from collections import deque
from GWFA_golden import golden_512, generate_edges_from_golden


NUM_NODES = 512
NUM_EDGES = 6
code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}


def extend_position(traceback, offset, position, i, current_idx, query, nodes, edges):
    edge_bits = edges[current_idx]

    if edge_bits==0 :
        position.append((i, current_idx))
        return

    for k in range(NUM_EDGES):
        if edge_bits & (1 << k): 
            next_idx = current_idx + (NUM_EDGES-k)

            if next_idx < NUM_NODES+1 and i+1 < NUM_NODES+1 and offset[i + 1][next_idx] == 0:

                if query[i + 1] == nodes[next_idx]:
                    offset[i + 1][next_idx] = 1  

                    for move in traceback[i][current_idx]:
                        traceback[i+1][next_idx].append(move)
                    
                    traceback[i+1][next_idx].append( str(NUM_EDGES-k) + 'M' )

                    extend_position(traceback, offset, position, i + 1, next_idx, query, nodes, edges)  

                elif query[i + 1] != nodes[next_idx]:
                    # extension stop point
                    position.append((i, current_idx))
            
            else: 
                # boundary
                position.append((i, current_idx))



def GWFA_512_x_512(nodes, edges, query):
    offset      = np.zeros((NUM_NODES+1, NUM_NODES+1)).astype(np.uint32)
    traceback   = [[[] for _ in range(NUM_NODES+1)] for _ in range(NUM_NODES+1)]
    position = []
    queue = deque([(0, 0)])

    offset[0][0] = 1
    current_idx = 0
    edit_distance = 0
    
    while (not offset[NUM_NODES, NUM_NODES]):

        # print("offset:")
        # for i in range(NUM_NODES+1):
        #     print(" ".join(str(offset[i, j]) for j in range(NUM_NODES+1)))
        # print()

        
        while(queue):
            i, current_idx = queue.popleft()
            extend_position(traceback, offset, position, i, current_idx, query, nodes, edges)

            if offset[NUM_NODES, NUM_NODES]:
                return edit_distance, traceback[NUM_NODES][NUM_NODES], offset

        edit_distance += 1

        # expansion
        for pos in position:
            x, y = pos  
            pos_edge_bits = edges[y]

            if x+1 < NUM_NODES+1 and offset[x + 1][y]==0:
                offset[x + 1][y] = 1
                queue.append((x + 1, y))

                for move in traceback[x][y]:
                    traceback[x+1][y].append(move)

                traceback[x+1][y].append(str(0) + 'I')

            for t in range(NUM_EDGES):
                if pos_edge_bits & (1 << t): 
                    next_y = y + (NUM_EDGES-t)

                    if next_y < NUM_NODES+1 and offset[x][next_y]==0:
                        offset[x][next_y] = 1
                        queue.append((x, next_y))

                        for move in traceback[x][y]:
                            traceback[x][next_y].append(move)

                        traceback[x][next_y].append(str(NUM_EDGES-t) + 'D')

                    if x+1 < NUM_NODES+1 and next_y < NUM_NODES+1 and offset[x + 1][next_y]==0:
                        offset[x + 1][next_y] = 1
                        queue.append((x + 1, next_y)) 

                        for move in traceback[x][y]:
                            traceback[x+1][next_y].append(move)

                        traceback[x+1][next_y].append(str(NUM_EDGES-t) + 'U')

        position = []

    # print("offset:")
    # for i in range(NUM_NODES+1):
    #     print(" ".join(str(offset[i, j]) for j in range(NUM_NODES+1)))
    # print()
    
    return edit_distance, traceback[NUM_NODES][NUM_NODES], offset
        
    

def test_512_x_512():

    # for boundary conditions
    nodes        = []
    golden_edges = []
    query        = []
    nodes.append(4)
    query.append(4)
    golden_edges.append(0)
    golden_edges.append(1)
    
    #random.seed(421)

    for i in range(0, NUM_NODES):
        base_code = random.getrandbits(2)              
        nodes.append(base_code)
        qry = random.getrandbits(2)
        query.append(qry)

    # print("Nodes:")
    # print([code_to_base[node] for node in nodes]) 

    # print("Query:")
    # print([code_to_base[q] for q in query])  
    # print()

    # setting for in-edges
    for i in range(1, NUM_NODES):       
        if i <= NUM_EDGES:     
            edge_bits = random.randint(1, 2**i-1)
        else:
            edge_bits = random.randint(1, 2**NUM_EDGES-1)
        
        golden_edges.append(edge_bits)

    #print(golden_edges)


    res, ans = golden_512(golden_edges, query, nodes, NUM_NODES, NUM_EDGES)
    print("total edit distance (golden) is: ", res)


    # setting for out-edges
    edges = generate_edges_from_golden(golden_edges, NUM_NODES+1, NUM_EDGES)
    #print(edges)


    # GWFA 512x512
    score, path, offset = GWFA_512_x_512(nodes, edges, query)
    print("total edit distance is: ", score)
    #print("traceback path is: ", path)
    print()


    # print("golden * offset = GWFA path")
    # for i in range(NUM_NODES+1):
    #     print(" ".join(str(ans[i, j]*offset[i][j]) for j in range(NUM_NODES+1)))
    # print()


    # check
    check = 0
    for move in path:
        if move[1] == 'U' or move[1] == 'I' or move[1] == 'D':
            check += 1
    

    if check == score and score == res:
        print("Your edit distance is identical to golden!")
        print("Your Traceback result matches with your edit distance!")
    else:
        print("There are some errors.")


 
    i = NUM_NODES
    j = NUM_NODES
    cur = len(path) - 1
    check = 0

    while not (i==0 and j==0):

        before = int(path[cur][0])
        dir    = path[cur][1]
        golden_edge_bits = golden_edges[j]


        if(query[i]==nodes[j]):
            cost = 0
        else:
            cost = 1


        source = []
        for k in range(NUM_EDGES):
            if golden_edge_bits & (1 << (NUM_EDGES - k - 1)):  
                source.append(ans[i][j-NUM_EDGES+k]+1)
                source.append(ans[i-1][j-NUM_EDGES+k]+cost)
                

        source.append(ans[i-1][j]+1)   
        result = min(source)

        if dir == 'M':
            if result != ans[i-1][j-before]:
                check += 1
        elif dir == 'D':
            if result != ans[i][j-before]+1:
                check += 1
        else:
            if result != ans[i-1][j-before]+1:
                check += 1

  
        if dir != 'D':
            i -= 1

        j   -= before
        cur -= 1

    
    if check==0:
        print("Your result shares same path as the golden")
    else:
        print(f"There are {check} different parts in the path")


if __name__ == "__main__":
    test_512_x_512()

