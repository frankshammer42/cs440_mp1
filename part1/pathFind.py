import numpy as np
import node
import utilities
import copy
import Queue


def contain_goal(frontier, goal_position):
    for frontier_node in frontier:
        if(frontier_node.position == goal_position):
            return True
    return False


def legal_position(position_list, map):
    row_size, col_size = map.shape
    result = []
    for position in position_list:
        position_x = position[0]
        position_y = position[1]
        if (position_x<row_size) and (position_y<col_size) and (position_x>=0) and (position_y>=0) and map[position_x][position_y]:
            result.append((position_x, position_y))
    return result


def manhattan_distance(point_1, point_2):
    point_1_x, point_1_y = point_1
    point_2_x, point_2_y = point_2
    return abs(point_1_x-point_2_x) + abs(point_1_y-point_2_y)


#Expand node and add the expended node to the frontier
#Since the frontier has a different data structures this time we can't simply copy paste
#which_method: 0 for greedy -1 for A*
def informed_expand(to_expand_node, map, frontier, explored_positions, goal_position ,which_method):
    available_position=[]
    to_expend_x, to_expend_y = to_expand_node.position
    available_position.append((to_expend_x-1, to_expend_y))
    available_position.append((to_expend_x+1, to_expend_y))
    available_position.append((to_expend_x, to_expend_y-1))
    available_position.append((to_expend_x, to_expend_y+1))
    legal_positions = legal_position(available_position, map)
    for position in legal_positions:
        #Part 1 of repeated states detection
        #Since our heurstic is consistent we can still use repeated states detection
        if position not in explored_positions:
            same_position_node_exists = 0
            toadd_pathList = copy.deepcopy(to_expand_node.pathList)
            toadd_pathList.append(position)
            node_to_add = node.Node(to_expand_node.step_cost + 1, to_expand_node.depth + 1, toadd_pathList, position)
            #Here is the difference we need to update the cost accordingly based on informed search strategy
            if(which_method == 0):
                #greedy
                node_to_add.heuristic_cost = manhattan_distance(goal_position, node_to_add.position)
                node_to_add.cost = node_to_add.heuristic_cost
            else:
                #A*
                node_to_add.heuristic_cost = manhattan_distance(goal_position, node_to_add.position)
                node_to_add.cost = node_to_add.step_cost + node_to_add.heuristic_cost


            #Check if we have a node that has the same position and has a smaller cost
            #if true, then remove the old node and attach the new node
            for frontier_node in frontier.queue:
                if position == frontier_node.position:
                    same_position_node_exists = 1
                    if node_to_add.cost < frontier_node.cost:
                        frontier.queue.remove(frontier_node)
                        frontier.put(node_to_add)

            #we don't have the same position node
            if not same_position_node_exists:
                frontier.put(node_to_add)





#Expand node and add the expended node to the frontier
def uninformed_expand(to_expand_node, map, frontier, explored_positions):
    available_position=[]
    to_expend_x, to_expend_y = to_expand_node.position
    available_position.append((to_expend_x-1, to_expend_y))
    available_position.append((to_expend_x+1, to_expend_y))
    available_position.append((to_expend_x, to_expend_y-1))
    available_position.append((to_expend_x, to_expend_y+1))
    legal_positions = legal_position(available_position, map)
    for position in legal_positions:
        #Part 1 of repeated states detection
        if position not in explored_positions:
            same_position_node_exists = 0
            toadd_pathList = copy.deepcopy(to_expand_node.pathList)
            toadd_pathList.append(position)
            node_to_add = node.Node(to_expand_node.step_cost + 1, to_expand_node.depth + 1, toadd_pathList, position)
            #Check if we have a node that has the same position and has a smaller cost
            #if true, then remove the old node and attach the new node


            for frontier_node in frontier:
                if position == frontier_node.position:
                    same_position_node_exists = 1
                    if to_expand_node.step_cost+1 < frontier_node.step_cost:
                        frontier.remove(frontier_node)
                        frontier.append(node_to_add)

            #we don't have the same position node
            if not same_position_node_exists:
                frontier.append(node_to_add)




#This fucking bug about reference just hurts my fucking ass fucking much
#WTF is wrong with the fucking del and remove fuck
def uninformed_search(maze_name, which_method):
    """
    This function will do both bfs and dfs 
    param maze_name: the filename of the file contains maze
    param which_method: -1 for dfs 0 for bfs 
    """
    map, start_position, goal_position_list = utilities.file_to_array(maze_name)
    goal_position = goal_position_list[0]
    start_node = node.Node(0,0,[start_position],start_position)
    frontier = [start_node]
    explored_positions = []
    while(not contain_goal(frontier, goal_position)):
        to_expand_node = frontier[which_method]
        if(which_method == 0):
            del frontier[0]
        else:
            del frontier[len(frontier)-1]

        explored_positions.append(to_expand_node.position)
        uninformed_expand(to_expand_node, map, frontier, explored_positions)
    for frontier_node in frontier:
        if(frontier_node.position == goal_position):
            print frontier_node
            utilities.print_route(maze_name, frontier_node.pathList)
            return


def informed_search(maze_name, which_method):
    """
    This function will do both greedy and A* 
    param maze_name: the filename of the file contains maze
    param which_method: 0 for greedy -1 for A* 
    """
    map, start_position, goal_position_list = utilities.file_to_array(maze_name)
    goal_position = goal_position_list[0]
    start_node = node.Node(0,0,[start_position],start_position)
    start_node.heuristic_cost = manhattan_distance(goal_position, start_position)
    start_node.cost = start_node.heuristic_cost + 0
    frontier = Queue.PriorityQueue()
    frontier.put(start_node)
    explored_positions = []
    counter = 0
    while(not contain_goal(frontier.queue, goal_position)):
        to_expand_node = frontier.get()
        explored_positions.append(to_expand_node.position)
        informed_expand(to_expand_node, map, frontier, explored_positions, goal_position, which_method)
        counter += 1


    print counter
    for frontier_node in frontier.queue:
        if(frontier_node.position == goal_position):
            print frontier_node
            utilities.print_route(maze_name, frontier_node.pathList)
            return




informed_search("./big_maze.txt", -1)
# uninformed_search("./big_maze.txt",-1)


