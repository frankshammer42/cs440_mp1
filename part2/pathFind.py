import numpy as np
import node
import nodept2
import utilities
import copy
import Queue


def contain_goal(frontier, dot_number):
    #Here the node in frontier belongs to nodept2
    goal_condition = dot_number * [1]
    for node in frontier:
        # print node.dot_condition
        # print "------------------------------------------------------"
        if node.dot_condition.values() == goal_condition:
            return True
    return False


def calculate_maze_contain_goal(frontier, goal_position):
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


#we use the same inform expand calculate maze distance
#Expand node and add the expended node to the frontier
#Since the frontier has a different data structures this time we can't simply copy paste
#which_method: 0 for greedy -1 for A*
def calculate_maze_expand(to_expand_node, map, frontier, explored_positions, goal_position):
    available_position=[]
    to_expend_x, to_expend_y = to_expand_node.position
    available_position.append((to_expend_x-1, to_expend_y))
    available_position.append((to_expend_x+1, to_expend_y))
    available_position.append((to_expend_x, to_expend_y-1))
    available_position.append((to_expend_x, to_expend_y+1))
    legal_positions = legal_position(available_position, map)
    # if(to_expand_node.position == (2,16)):
        # print "yeah"
    
    
    for position in legal_positions:
        #Part 1 of repeated states detection
        #Since our heurstic is consistent we can still use repeated states detection
        if position not in explored_positions:

            same_position_node_exists = 0
            toadd_pathList = copy.deepcopy(to_expand_node.pathList)
            toadd_pathList.append(position)
            node_to_add = node.Node(to_expand_node.step_cost + 1, to_expand_node.depth + 1, toadd_pathList, position)

            #we use the A* search here using manhatan distance as heuristic
            node_to_add.heuristic_cost = manhattan_distance(goal_position, node_to_add.position)
            node_to_add.cost = node_to_add.step_cost + node_to_add.heuristic_cost
            # if(to_expand_node.position == (2,16)):
                # print frontier.queue
                # print "--------------"

            #Check if we have a node that has the same position and has a smaller cost
            #if true, then remove the old node and attach the new node
            counter = 0
            for frontier_node in frontier.queue:
                if position == frontier_node.position:
                    same_position_node_exists = 1
                    if node_to_add.cost < frontier_node.cost:
                        del frontier.queue[counter]
                        frontier.put(node_to_add)
                counter += 1

            #we don't have the same position node
            if not same_position_node_exists:
                frontier.put(node_to_add)



    return



def calculate_maze_distance(start_position, goal_position, map):
    """
    Helper function to calculate maze distance
    """
    start_node = node.Node(0,0,[start_position],start_position)
    start_node.heuristic_cost = manhattan_distance(goal_position, start_position)
    start_node.cost = start_node.heuristic_cost + 0
    frontier = Queue.PriorityQueue()
    frontier.put(start_node)
    explored_positions = set() 
    debug_it = 0
    
    while(not calculate_maze_contain_goal(frontier.queue, goal_position)):
        to_expand_node = frontier.get()
        explored_positions.add(to_expand_node.position)
        calculate_maze_expand(to_expand_node, map, frontier, explored_positions, goal_position)

    for frontier_node in frontier.queue:
        if(frontier_node.position == goal_position):
            return frontier_node.cost


def initialize_dot_condition(goal_position_list):
    dot_condition = {}
    for goal_position in goal_position_list:
        dot_condition[goal_position] = 0
    return dot_condition



def search_expand(to_expand_node, map, frontier, explored_states, goal_position_list, precomputed_distance):
    available_position=[]
    to_expend_x, to_expend_y = to_expand_node.position
    available_position.append((to_expend_x-1, to_expend_y))
    available_position.append((to_expend_x+1, to_expend_y))
    available_position.append((to_expend_x, to_expend_y-1))
    available_position.append((to_expend_x, to_expend_y+1))
    legal_positions = legal_position(available_position, map)

    dot_condition = to_expand_node.dot_condition


    #A suffix to append to each legal position for repeated states
    explored_identifier_suffix = dot_condition.values()


    for position in legal_positions:
        #Part 1 of repeated states detection
        #Since our heurstic is consistent we can still use repeated states detection
        if tuple(list(position)+explored_identifier_suffix) not in explored_states:

            same_position_node_exists = 0

            toadd_pathList = copy.deepcopy(to_expand_node.pathList)
            toadd_pathList.append(position)
            node_to_add = nodept2.Node_pt2(to_expand_node.step_cost + 1, to_expand_node.depth + 1, toadd_pathList, position)
            toadd_dot_condition = copy.deepcopy(to_expand_node.dot_condition)
            #We need to check whether we are actually at a goal if yes we have to update the dot_condition and identifier
            if position in goal_position_list:
                toadd_dot_condition[position] = 1
            toadd_explored_identifier = list(position) + toadd_dot_condition.values()
            node_to_add.dot_condition = toadd_dot_condition
            node_to_add.explored_identifier = toadd_explored_identifier


            node_to_add.heuristic_cost = computeHeuristic(node_to_add, map, goal_position_list, precomputed_distance)
            node_to_add.cost = node_to_add.step_cost + node_to_add.heuristic_cost


            #Check if we have a node that has the same position and has a smaller cost
            #if true, then remove the old node and attach the new node
            counter = 0
            for frontier_node in frontier.queue:
                if node_to_add.explored_identifier == frontier_node.explored_identifier:
                    same_position_node_exists = 1
                    if node_to_add.step_cost < frontier_node.step_cost:
                        frontier.queue.remove(frontier_node)
                        frontier.put(node_to_add)
                counter += 1

            #we don't have the same position node
            if not same_position_node_exists:
                frontier.put(node_to_add)


def distance_between_goal_pair(map, goal_position_list):
    ret_list = {}
    position_list_len = len(goal_position_list)
    for i in range(position_list_len):
        for j in range(i+1,position_list_len):
            dis = calculate_maze_distance(goal_position_list[i], goal_position_list[j], map)
            if goal_position_list[i][0]+goal_position_list[i][1]<goal_position_list[j][0]+goal_position_list[j][1]: ret_list[(goal_position_list[i],goal_position_list[j])] = dis
            elif(goal_position_list[i][0]+goal_position_list[i][1]>goal_position_list[j][0]+goal_position_list[j][1]):
                ret_list[(goal_position_list[j],goal_position_list[i])] = dis
            else: #the x+y of these two coordinates are the same
                if goal_position_list[i][0]<goal_position_list[j][0]:
                    ret_list[(goal_position_list[i],goal_position_list[j])] = dis
                else:
                    ret_list[(goal_position_list[j],goal_position_list[i])] = dis
    return ret_list


def computeHeuristicHelper(node, goal_list, goal_distance_dictionary):
    not_eaten_keys = []
    for pos in goal_list:
        if node.dot_condition[pos] == 0:
            not_eaten_keys.append(pos)

    selected_dictionary = {}
    for i in range(len(not_eaten_keys)):
        x1, y1 = not_eaten_keys[i]
        for j in range(i+1, len(not_eaten_keys)):
            x2,y2 = not_eaten_keys[j]
            if (x1+y1 < x2+y2):
                val = goal_distance_dictionary[((x1,y1),(x2,y2))]
                #selected_dictionary.update({((x1,y1),(x2,y2)), val})
                selected_dictionary[((x1,y1),(x2,y2))] = val
            elif (x1+y1 == x2+y2):
                if x1 <= x2:
                    val = goal_distance_dictionary[((x1, y1), (x2, y2))]
                    selected_dictionary[((x1, y1), (x2, y2))] = val
                else:
                    val = goal_distance_dictionary[((x2, y2), (x1, y1))]
                    selected_dictionary[((x2, y2), (x1, y1))] = val
            else:
                val = goal_distance_dictionary[((x2, y2), (x1, y1))]
                selected_dictionary[((x2, y2), (x1, y1))] = val
    return selected_dictionary



def findBiggestKeyPair(dictionary):
    keyArr = []
    valArr = []
    for key, value in dictionary.iteritems():
        keyArr.append(key)
        valArr.append(value)
    max_idx = valArr.index(max(valArr))
    pos1, pos2 = keyArr[max_idx]
    goal_dist = valArr[max_idx]
    return (pos1, pos2, goal_dist)


def computeHeuristic(node, maze_map, goal_list, goal_distance_dictionary): #return a heuristic for
    #find two goals which preserve the largest distance:
    #We need to reward the progress

    goal_number = len(goal_list)
    sum_of_conditions = sum(node.dot_condition.values())
    if(sum_of_conditions == goal_number-1):
        for key in node.dot_condition:
            if node.dot_condition[key] == 0:
                return calculate_maze_distance(node.position, key, maze_map)

    if(sum_of_conditions == goal_number):
        return 0


    to_pass_in_dict = computeHeuristicHelper(node, goal_list, goal_distance_dictionary)


    pos1, pos2, goal_dist = findBiggestKeyPair(to_pass_in_dict)
    #find heuristic for node1 & node2:
    h1 = calculate_maze_distance(node.position, pos1, maze_map)
    h2 = calculate_maze_distance(node.position, pos2, maze_map)
    # if sum_of_conditions == 0: 
        # h1_result = (h1+goal_dist)/0.5
        # h2_result = (h2+goal_dist)/0.5
    # else:
    h1_result = (h1+goal_dist)
    h2_result = (h2+goal_dist)
    # h1_result = (h1+goal_dist)
    # h2_result = (h2+goal_dist)
    return min(h1_result, h2_result)




def search(maze_name):
    #In here the node we are using should come from nodept2
    map, start_position, goal_position_list = utilities.file_to_array(maze_name)
    dot_condition = initialize_dot_condition(goal_position_list)
    start_node = nodept2.Node_pt2(0,0,[start_position],start_position)
    dot_number = len(goal_position_list)
    start_node.dot_condition = dot_condition

    precomputed_distance = distance_between_goal_pair(map, goal_position_list)

    start_node.heuristic_cost = computeHeuristic(start_node, map, goal_position_list, precomputed_distance)

    start_node.cost = start_node.heuristic_cost + 0
    explored_identifier = list(start_node.position) + list(dot_condition.values())
    start_node.dot_condition = dot_condition
    start_node.explored_identifier = explored_identifier
    frontier = Queue.PriorityQueue()
    frontier.put(start_node)

    explored_states = set()
    counter = 0
    while(not contain_goal(frontier.queue, dot_number)):
        counter += 1
        to_expand_node = frontier.get()
        if(to_expand_node.position == (5,2)):
            print to_expand_node.dot_condition
        tuple_id = tuple(to_expand_node.explored_identifier)
        explored_states.add(tuple_id)
        search_expand(to_expand_node, map, frontier, explored_states, goal_position_list, precomputed_distance)

    goal_condition = dot_number * [1]
    for frontier_node in frontier.queue:
        if(frontier_node.dot_condition.values() == goal_condition):
            print frontier_node
            utilities.print_route(maze_name, frontier_node.pathList)
            return

search("./small.txt")
