import random
import numpy as np
import copy
from collections import deque


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



def GWFA_512_x_512_boundary(nodes, edges, query, beginning, last, NUM_NODES, NUM_EDGES, RETREAT_STEP, preload_pos):

    if beginning:
        offset      = np.zeros((NUM_NODES+1, NUM_NODES+1)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES+1)] for _ in range(NUM_NODES+1)]
        queue       = deque([(0, 0)])
        offset[0][0] = 1
        
    else:
        offset      = np.zeros((NUM_NODES, NUM_NODES)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
        queue       = preload_pos
        
        for (x,y) in preload_pos:
            offset[x][y] = 1
        
        
    position    = []
    check = True
    edit_distance = 0
    

    while (check):
        backup = copy.deepcopy(queue)
        

        while(queue):    
            i, current_idx = queue.popleft()
            check, p, q = extend_position_boundary(traceback, offset, position, i, current_idx, query, nodes, edges, NUM_EDGES)
            
            if not check and last:
                return edit_distance, traceback[p][q], (p, q), None, -1, -1
            
            
            if (not check) and (not last):
                    
                preload_pos = deque()
                candidate = []
                
                print(backup)

                for (x,y) in backup:
                    if (i-x <= RETREAT_STEP and i-x >= 0) and (current_idx-y <= RETREAT_STEP and current_idx-y >= 0):
                        candidate.append((x,y))

                print(i,current_idx)
                min_x = min(candidate, key=lambda x: x[0])[0]
                min_y = min(candidate, key=lambda x: x[1])[1]


                for (i,j) in candidate:
                    preload_pos.append( (i-min_x, j-min_y) )
                    
                return edit_distance, traceback[i][current_idx], (i, current_idx), preload_pos, min_x, min_y
            

        
        edit_distance += 1

        # expansion
        for pos in position:
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

                    
                    # if next_y > len(nodes):
                    #     edit_distance -= 1
                    #     return edit_distance, traceback[x][y], (x, y), preload_pos, min_x, min_y, traceback
                    
                    
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
    
    return edit_distance, traceback[-1][-1], (len(query)-1, len(nodes)-1),  None, -1, -1

    