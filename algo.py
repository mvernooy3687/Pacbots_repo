# You can modify this file to implement your own algorithm

from constants import *

"""
You can use the following values from constants.py to check for the type of cell in the grid:
I = 1 -> Wall 
o = 2 -> Pellet (Small Dot)
e = 3 -> Empty
"""

def get_next_coordinate(grid, location):

    """
    Calculate the next coordinate for 6ix-pac to move to.
    Check if the next coordinate is a valid move.

    Parameters:
    - grid (list of lists): A 2D array representing the game board.
    - location (list): The current location of the 6ix-pac in the form (x, y).

    Returns:
    - list or tuple: 
        - If the next coordinate is valid, return the next coordinate in the form (x, y) or [x,y].
        - If the next coordinate is invalid, return None.
    """
    

    #A* attempt:

    import heapq

    def a_star_call(start,goal):

        class Node:
            def __init__(self, position, parent=None, cost=0):
                self.position = position
                self.parent = parent
                self.cost = cost

            def __lt__(node1, node2):
                return node1.cost < node2.cost

        def heuristic(node, goal):
            y1, x1 = node.position
            y2, x2 = goal.position
            return abs(x1 - x2) + abs(y1 - y2)

        def get_neighbors(node,grid):
            y, x = node.position
            neighbors = []

            # Add adjacent nodes (up, down, left, right)
            for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_y, new_x = y + dy, x + dx
                
                if new_x < 0 or new_x > 30 or new_y < 0 or new_y > 27:
                    continue
                elif grid[new_y][new_x] == 1 or grid[new_y][new_x] == 6:
                    continue
                
                neighbors.append(Node((new_y, new_x), parent=node, cost=node.cost + 1))

            return neighbors


        def astar(start, goal):
            open_list = []
            closed_list = set()

            heapq.heappush(open_list, (start.cost, start))
            
            while open_list:
                current_cost, current_node = heapq.heappop(open_list)

                if current_node.position == goal.position:
                    # Goal reached, construct and return the path
                    path = []
                    while current_node:
                        path.append(current_node.position)
                        current_node = current_node.parent
                    return path[::-1]

                closed_list.add(current_node)

                for neighbor in get_neighbors(current_node,grid):
                    if neighbor in closed_list:
                        continue

                    new_cost = current_node.cost + 1
                    if neighbor not in open_list:
                        heapq.heappush(open_list, (new_cost + heuristic(neighbor, goal), neighbor))
                    elif new_cost < neighbor.cost:
                        neighbor.cost = new_cost
                        neighbor.parent = current_node

        start = Node(start)
        goal = Node(goal)
        
        path = astar(start, goal)
        return path[1]
    
    def get_closest_dot(grid, location):
        import copy
        dist_grid = copy.deepcopy(grid)
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                dist_grid[y][x] = 1000 if dist_grid[y][x]!=2 else abs(y-location[0])+abs(x-location[1])
        
        mins = [row.index(min(row)) for row in dist_grid] #index of smallest dist in each row
        smallest_dists = [dist_grid[x][mins[x]] for x in range(len(dist_grid))] #gets list of smallest dists per row
        smallest_row = smallest_dists.index(min(smallest_dists))
        smallest_col = dist_grid[smallest_row].index(min(dist_grid[smallest_row]))
        return(smallest_row,smallest_col)
    
    closest_dot = get_closest_dot(grid, location)
    coords = a_star_call(location,closest_dot)
    return coords

""" grid copied here for convenience
grid = [[I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I], # 0
        [I,o,o,o,o,I,I,o,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I], # 5
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I], # 10
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I],
        [I,o,I,I,I,I,I,e,I,I,I,I,I,e,I,n,n,n,n,e,I,I,I,I,I,o,I,I,I,I,I],
        [I,o,o,o,o,I,I,o,o,o,o,I,I,e,I,n,n,n,I,e,e,e,o,I,I,o,o,o,o,o,I], # 15
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,n,n,n,I,e,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,I,e,I,I,I,I,I,e,I,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,e,e,e,e,e,e,e,e,e,I,I,o,o,o,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,e,I,o,I],
        [I,o,I,I,I,I,I,o,I,I,o,I,I,I,I,I,e,I,I,I,I,I,I,I,I,o,I,I,I,o,I], # 20
        [I,o,I,I,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,I,I,I,I,I,I,I,I,I,I,o,I,I,o,I,I,I,o,I],
        [I,o,I,I,o,I,I,I,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,o,o,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,e,I,o,I],
        [I,o,I,I,o,I,I,o,I,I,o,I,e,e,e,e,e,e,e,e,e,I,o,I,I,o,I,I,I,o,I], # 25
        [I,o,o,o,o,I,I,o,o,o,o,I,e,e,e,e,e,e,e,e,e,I,o,o,o,o,o,o,o,o,I],
        [I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I]]
#        |         |         |         |         |         |         |   
#        0         5        10        15       20         25       30
"""

""" for debugging, and v2 WIP
import copy
import statistics
import pandas as pd
"""

def get_closest_dot(grid, location):
    import copy
    dist_grid = copy.deepcopy(grid)
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            dist_grid[y][x] = 1000 if dist_grid[y][x]!=2 else abs(y-location[0])+abs(x-location[1])

    """ for debugging
    print(dist_grid)
    with pd.option_context('display.max_rows', None,'display.max_columns',None):
        print(pd.DataFrame(dist_grid))
    """
    
    mins = [row.index(min(row)) for row in dist_grid] #index of smallest dist in each row
    smallest_dists = [dist_grid[x][mins[x]] for x in range(len(dist_grid))] #gets list of smallest dists per row
    smallest_row = smallest_dists.index(min(smallest_dists))
    smallest_col = dist_grid[smallest_row].index(min(dist_grid[smallest_row]))
    return(smallest_row,smallest_col)

""" work in progress on additional heuristic, for initial algo challenge pls ignore
If curious, idea is to try to apply a bias towards pacman not going past a cluster of dots;
when multiple dots are equally close, old version just chose one arbitrarily, but this can 
lead to pacman going past a group of dots and having to backtrack later

def get_closest_dot_v2(grid, location):
    dist_grid = copy.deepcopy(grid)
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            dist_grid[y][x] = 1000 if dist_grid[y][x]!=2 else abs(y-location[0])+abs(x-location[1])

    print(dist_grid)
    with pd.option_context('display.max_rows', None,'display.max_columns',None):
        print(pd.DataFrame(dist_grid))
    
    mins = [row.index(min(row)) for row in dist_grid] #index of smallest dist in each row
    smallest_dists = [dist_grid[x][mins[x]] for x in range(len(dist_grid))] #gets list of smallest dists per row

    if len(smallest_dists)!=len(set(smallest_dists)): #if multiple dots equally close
        clusters = [(9,15),(18,15)] #tweak me
        update_cycles = 3 #tweak me
        for cluster in clusters:
            for cycle in update_cycles:
                x_vectors = []
                y_vectors = []
                for row in grid:
                    for point in row:
                        y_vectors.append(point[0] - cluster[0])
                        x_vectors.append(point[1] - cluster[1])
                ave_vector = (statistics.mean(y_vectors),statistics.mean(x_vectors))
                cluster = (cluster[0]+ave_vector[0], cluster[1]+ave_vector[1])

        #choose dot closest to nearest cluster
    
    smallest_row = smallest_dists.index(min(smallest_dists))
    smallest_col = dist_grid[smallest_row].index(min(dist_grid[smallest_row]))
    return(smallest_row,smallest_col)

pacman_location = (25,15)

closest_dot = get_closest_dot(grid, pacman_location)
print(closest_dot)
"""



