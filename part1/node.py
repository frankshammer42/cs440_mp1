class Node(object):
    def __init__(self, step_cost, depth, pathList, position):
        #Specifically for A* and greedy best
        self.heuristic_cost = 0
        self.step_cost = step_cost
        self.cost = 0
        self.depth = depth
        self.pathList = pathList
        self.position = position

    # In greedy and A* we need to use priority queue
    # We need overide this property to use it
    def __gt__(self, other):
        if(isinstance(other, Node)):
            return self.cost > other.cost
        return NotImplemented

    def __lt__(self, other):
        if(isinstance(other, Node)):
            return self.cost < other.cost
        return NotImplemented

    # We need to use a Queue to store the item we need to make sure we chan check that if an element is already in the queue
    def __eq__(self, other):
        if(isinstance(other, Node)):
            return self.cost == other.cost
        return NotImplemented


    def __ne__(self, other):
        if(isinstance(other, Node)):
            return not self == other
        return NotImplemented


    def __repr__(self):
        return 'Position %s\nstep_cost %s\nheuristic_cost %s\ncost %s\ndepth %s\npathList %s\n'%(self.position, self.step_cost, self.heuristic_cost,
                                                                                   self.cost,self.depth, self.pathList)


