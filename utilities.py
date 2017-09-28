#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
 #File Name : utilities.py
 #Creation Date : 26-09-2017
 #Created By : Rui An  
#_._._._._._._._._._._._._._._._._._._._._.
import numpy as np

def file_to_array(maze_file):
    ret_matrix = []
    start_position = (0,0)
    goal_position_list = [] 
    with open(maze_file, "r+") as f:
        line_count = 0
        for line in f:
            chars = list(line.rstrip())
            temp_array = []
            char_count = 0
            for i in chars: 
                if(i=='%'): 
                    temp_array.append(0)
                elif(i==' '):
                    temp_array.append(1)
                elif(i=='P'):
                    temp_array.append(1)
                    start_position = (line_count, char_count)
                elif(i=='.'):
                    temp_array.append(1)
                    goal_position_list.append((line_count, char_count))
                char_count += 1
            line_count += 1
            ret_matrix.append(temp_array)
    ret_matrix = np.array(ret_matrix)
    return (ret_matrix,start_position,goal_position_list)


def print_route(maze_file, path_list):
    map = []
    with open(maze_file, "r+") as f:
        for line in f:
            chars = list(line.rstrip())
            map.append(chars)

    for i in path_list:
        map[i[0]][i[1]] = 'O'
    for i in range(len(map)):
        for j in range(len(map[0])):
            print map[i][j],
        print '\n'
