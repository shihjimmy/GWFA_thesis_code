import random
import numpy as np
from collections import deque
from GWFA_golden import golden_512, generate_edges_from_golden


code_to_base = {0: 'A', 1: 'T', 2: 'C', 3: 'G', 4: ' '}


def extend_position_boundary(traceback, offset, position, i, current_idx, query, nodes, edges, NUM_EDGES):
    
    if i==len(query)-1 or current_idx==len(nodes)-1:
        return False, i , current_idx

    edge_bits = edges[current_idx]

    # if edge_bits==0 :
    #     position.append((i, current_idx))
    #     return True, i , current_idx

    for k in range(NUM_EDGES):
        if edge_bits & (1 << k): 
            next_idx = current_idx + (NUM_EDGES-k)

            if next_idx < len(nodes) and offset[i + 1][next_idx] == 0: 

                if query[i + 1] == nodes[next_idx]:
                    offset[i + 1][next_idx] = 1  

                    for move in traceback[i][current_idx]:
                        traceback[i+1][next_idx].append(move)
                    
                    traceback[i+1][next_idx].append( str(NUM_EDGES-k) + 'M' )

                    return_values, x, y = extend_position_boundary(traceback, offset, position, i + 1, next_idx, query, nodes, edges, NUM_EDGES)

                    if return_values == False: 
                        return False, x, y
                    

                elif query[i + 1] != nodes[next_idx]:
                    # extension stop point
                    position.append((i, current_idx))
                    
            
            elif next_idx >= len(nodes): 
                # over next segment
                return False, i , current_idx

    return True, i , current_idx



def GWFA_512_x_512_boundary(nodes, edges, query, beginning, last, NUM_NODES, NUM_EDGES):

    if beginning:
        offset      = np.zeros((NUM_NODES+1, NUM_NODES+1)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES+1)] for _ in range(NUM_NODES+1)]
    else:
        offset      = np.zeros((NUM_NODES, NUM_NODES)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]


    offset[0][0] = 1
    position    = []
    queue       = deque([(0, 0)])
    check = True
    edit_distance = 0
    

    while (check):
               
        """
            farthest wavefront should be processed first!!!
        """
        
        sorted_queue = sorted(queue, key=lambda x: (x[1], x[0]), reverse=True)
        idx = 0
        
        while(idx != len(sorted_queue)):
            i, current_idx = sorted_queue[idx]
            idx += 1

            check, x , y = extend_position_boundary(traceback, offset, position, i, current_idx, query, nodes, edges, NUM_EDGES)
            
            if not check:
                
                if not last:
                    # When check is False, backtrack using the last move
                    last_move_pos = traceback[x][y][-1][0]  # Get the position of the last move
                    last_move_dir = traceback[x][y][-1][1]  # Get the direction of the last move

                    # If I / D / U
                    if last_move_dir == 'I':  # Insert
                        x -= 1
                        edit_distance -= 1
                        
                    elif last_move_dir == 'D':  # Delete
                        y -= int(last_move_pos)
                        edit_distance -= 1
                        
                    elif last_move_dir == 'U':  # Mismatch
                        x -= 1
                        y -= int(last_move_pos)
                        edit_distance -= 1
                    
                
                return edit_distance, traceback[x][y], (x, y)

        
        edit_distance += 1
        
    
        """
            farthest wavefront should be processed first!!!
        """
        sorted_pos = sorted(position, key=lambda x: (x[1], x[0]), reverse=True)


        # expansion
        for pos in sorted_pos:
            x, y = pos  
            pos_edge_bits = edges[y]


            if  offset[x + 1][y]==0:
                offset[x + 1][y] = 1
                queue.append((x + 1, y))

                for move in traceback[x][y]:
                    traceback[x+1][y].append(move)

                traceback[x+1][y].append(str(0) + 'I')


            for t in range(NUM_EDGES):

                if pos_edge_bits & (1 << t): 
                    next_y = y + (NUM_EDGES-t)

                    
                    if next_y > len(nodes):
                        edit_distance -= 1
                        return edit_distance, traceback[i][current_idx], (i, current_idx)
                    
                    
                    if  offset[x][next_y]==0:
                        offset[x][next_y] = 1
                        queue.append((x, next_y))

                        for move in traceback[x][y]:
                            traceback[x][next_y].append(move)

                        traceback[x][next_y].append(str(NUM_EDGES-t) + 'D')


                    if  offset[x + 1][next_y]==0:
                        offset[x + 1][next_y] = 1
                        queue.append((x + 1, next_y)) 

                        for move in traceback[x][y]:
                            traceback[x+1][next_y].append(move)

                        traceback[x+1][next_y].append(str(NUM_EDGES-t) + 'U')
        position = []
    
    return edit_distance, traceback[-1][-1], (len(query)-1, len(nodes)-1)





def test_512_x_512_boundary(NUM_NODES, NUM_EDGES):

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

    # setting for in-edges
    for i in range(1, NUM_NODES):       
        if i <= NUM_EDGES:     
            edge_bits = random.randint(1, 2**i-1)
        else:
            edge_bits = random.randint(1, 2**NUM_EDGES-1)
        
        golden_edges.append(edge_bits)

    #print(golden_edges)


    res, ans = golden_512(golden_edges, query, nodes, NUM_NODES, NUM_EDGES)
    #print("total edit distance (golden) is: ", res)


    # setting for out-edges
    edges = generate_edges_from_golden(golden_edges, NUM_NODES+1, NUM_EDGES)
    #print(edges)


    # GWFA 512x512
    score, path, (end_x, end_y) = GWFA_512_x_512_boundary(nodes, edges, query, True, NUM_NODES, NUM_EDGES)
    print("edit distance (boundary) is: ", score)
    print("traceback path is: ", path)
    print("ends at position x: ", end_x)
    print("ends at position y: ", end_y)
    print()

    res = ans[end_x][end_y]

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


 
    i = end_x
    j = end_y
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
    NUM_NODES = 512
    NUM_EDGES = 6
    test_512_x_512_boundary(NUM_NODES, NUM_EDGES)
    