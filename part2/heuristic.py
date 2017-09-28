import numpy as np
def findBiggestKeyPair(dictionary):
    keyArr = np.array([])
    valArr = np.array([])
    for key, value in dictionary.iteritems():
        keyArr = np.append(keyArr, key)
        valArr = np.append(valArr, value)
    max_idx = np.argmax(valArr)
    pos1, pos2 = keyArr[max_idx]
    goal_dist = valArr[max_idx]
    return (pos1, pos2, goal_dist)

def computeHeuristic(node, maze_map, goal_list): #return a heuristic for
    #find the least-distance goal pair:
    dictionary = distance_between_goal_pair(maze_map, goal_list)
    #find two goals which preserve the largest distance:
    pos1, pos2, goal_dist = findBiggestKeyPair(dictionary)
    #find heuristic for node1 & node2:
    h1 = calculate_maze_distance(node.position, pos1, maze_map)
    h2 = calculate_maze_distance(node.position, pos2, maze_map)
    return max(h1+goal_dist, h2+goal_dist)
