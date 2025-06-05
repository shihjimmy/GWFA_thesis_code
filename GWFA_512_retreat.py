import random
import numpy as np
from collections import deque

def extend_position_boundary(traceback, offset, position, i, current_idx, query, nodes, edges, NUM_EDGES):
    
    if i==len(query)-1 or current_idx==len(nodes)-1:
        return False, i, current_idx

    edge_bits = edges[current_idx]

    # if edge_bits==0 :
    #     position.append((i, current_idx))
    #     return True

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
                return False, i, current_idx
            
    return True, i, current_idx




def GWFA_512_x_512_boundary(nodes, edges, query, beginning, NUM_NODES, NUM_EDGES):

    if beginning:
        offset      = np.zeros((NUM_NODES+1, NUM_NODES+1)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES+1)] for _ in range(NUM_NODES+1)]
    else:
        offset      = np.zeros((NUM_NODES, NUM_NODES)).astype(np.uint32)
        traceback   = [[[] for _ in range(NUM_NODES)] for _ in range(NUM_NODES)]
        

    offset[0][0] = 1
    position    = []
    queue       = deque([(0, 0)])
    edit_distance = 0
    check = True
    

    while (check):
    
        while(queue):
            i, current_idx = queue.popleft()
            check, x, y = extend_position_boundary(traceback, offset, position, i, current_idx, query, nodes, edges, NUM_EDGES)

            if not check:
                
                if x==len(query)-1 or y==len(nodes)-1:
                    return edit_distance, traceback[x][y], (x, y)
                
                
                # When check is False, backtrack using the last move
                last_move_pos = traceback[i][current_idx][-1][0]  # Get the position of the last move
                last_move_dir = traceback[i][current_idx][-1][1]  # Get the direction of the last move

                # Backtrack to the previous position based on the direction of the move
                # Must be I / D / U
                if last_move_dir == 'I':  # Insert
                    i -= 1
                elif last_move_dir == 'D':  # Delete
                    current_idx -= int(last_move_pos)
                elif last_move_dir == 'U':  # Mismatch
                    i -= 1
                    current_idx -= int(last_move_pos)
                
                # Find the previous extension point
                if len(traceback[i][current_idx]) >= 2:
                    old_i = i
                    old_idx = current_idx
                
                    for j in range(len(traceback[old_i][old_idx])-2, -1, -1):

                        last_move_pos = traceback[old_i][old_idx][j][0]
                        last_move_dir = traceback[old_i][old_idx][j][1]

                        if last_move_dir != "M":
                            break
                        else:
                            i -= 1
                            current_idx -= int(last_move_pos)

                
                edit_distance -= 1
                return edit_distance, traceback[i][current_idx], (i, current_idx)


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

                    if next_y > len(nodes):
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

