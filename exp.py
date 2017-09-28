import Queue as queue
import node

first_node = node.Node(0,0,[(0,0)],(0,0))
first_node.heuristic_cost = 6
first_node.cost = first_node.heuristic_cost + first_node.step_cost

second_node = node.Node(3,3,[(1,3)],(1,3))
second_node.heuristic_cost = 1
second_node.cost = second_node.heuristic_cost + second_node.step_cost


third_node = node.Node(4,4,[(2,3)],(2,3))
third_node.heuristic_cost = 5
third_node.cost = third_node.heuristic_cost + third_node.step_cost


forth_node = node.Node(3,3,[(1,3)],(1,3))
forth_node.heuristic_cost = 2
forth_node.cost = forth_node.heuristic_cost + second_node.step_cost


pqueue = queue.PriorityQueue()
pqueue.put(second_node)
pqueue.put(third_node)
pqueue.put(first_node)

for node in pqueue.queue:
    if node.position == (0,0):
        pqueue.queue.remove(node)


pqueue.put(forth_node)

#so pqueue sort in get
print pqueue.get()
print pqueue.get()
print pqueue.get()



