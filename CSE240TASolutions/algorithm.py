# class Node:
#     """
#     This class describes a single node contained within a graph. 
#     It has the following instannce level attributes:
    
#     ID: An integer id for the node i.e. 1
#     """    
#     def __init__(self, ID):
#         self.ID = ID
#         self.connected_nodes = []
        
#     def __repr__(self):
#         ID = self.ID
#         if len(self.connected_nodes)==0:
#             nodes = 'None'
#         else:
#             nodes = ','.join(str(cn[1].ID) for cn in self.connected_nodes)
#         return '\nNode:{}\nConnected Nodes:{}'.format(ID, nodes)
        
#     def set_connected_nodes(self,connected_nodes):
#         """
#         Adds edges that lead from this node to other nodes:
        
#         Parameters:
#         - connected_nodes: A list of tuples consisting of (cost, Node), 
#                            where 'cost' is a floating point value 
#                            indicating the cost to get from this node 
#                            to 'Node' and 'Node' is a Node object
#         """
#         self.connected_nodes = connected_nodes
    
# def build_graph():
#     """
#     Builds the graph to be parsed by the search algorithms.
#     Returns: All nodes with connectivity in the graph
#     """
#     ids = range(13)
#     coords = [(0,0), (1,1), (1,0), (1,1), (5,2), (3,1), (3,0), 
#               (3,-1), (5,1), (4,1), (4,0), (4,-2), (7,0)]
    
#     #https://en.wikipedia.org/wiki/Euclidean_distance
#     euclidean_distance = lambda x1y1, x2y2: ((x1y1[0]-x2y2[0])**2 +  (x1y1[1]-x2y2[1])**2)**(0.5)
    
#     def build_connected_node_list(from_id, to_ids):
#         starting_coords = coords[from_id]
        
#         connected_nodes = []
#         for to_id in to_ids:
#             connected_nodes.append((euclidean_distance(starting_coords, coords[to_id]), all_nodes[to_id]))
            
#         return connected_nodes
    
#     goal_coords = (7,0)
#     all_nodes = [Node(_id) for _id in ids]
    
#     all_nodes[8].set_connected_nodes(build_connected_node_list(8, [12]))
#     all_nodes[10].set_connected_nodes(build_connected_node_list(10,[12]))
#     all_nodes[5].set_connected_nodes(build_connected_node_list(5, [8]))
#     all_nodes[6].set_connected_nodes(build_connected_node_list(6, [9, 10]))
#     all_nodes[7].set_connected_nodes(build_connected_node_list(7, [11]))
#     all_nodes[1].set_connected_nodes(build_connected_node_list(1, [4,5]))
#     all_nodes[2].set_connected_nodes(build_connected_node_list(2, [5,6]))
#     all_nodes[3].set_connected_nodes(build_connected_node_list(3, [7]))
#     all_nodes[0].set_connected_nodes(build_connected_node_list(0, [1,2,3]))
    
#     return all_nodes


# # The starting node. You can use this cell to familiarize
# # yourself with the node/graph structure
# build_graph()


# def BFS(starting_node, goal_node):
#     """
#     This function implements the breath first search algorithm
    
#     Parameters:
#     - starting_node: The entry node into the graph
#     - goal_node: The integer ID of the goal node.
    
#     Returns:
#     A list containing the visited nodes in order they were visited with starting node
#     always being the first node and the goal node always being the last
#     """
#     visited_nodes_in_order = []
    
#     # YOUR CODE HERE
#     fringe = [starting_node]
#     exploredSet = set()
#     all_nodes = build_graph()
#     visited_nodes_in_order.append(starting_node)
    
#     # if starting node is goal
#     if(starting_node.ID == goal_node):
#         visited_nodes_in_order.append(all_nodes[str(goal_node)])
#         return visited_nodes_in_order


#     while(len(fringe) != 0):
#         poppedNode = fringe.pop(0)
#         exploredSet.add(poppedNode.ID)
        
#         successors = sorted(poppedNode.connected_nodes, key= lambda nodeTup: nodeTup[1].ID)
        
#         for cost, successor in successors:
#             if successor.ID not in exploredSet and successor not in fringe:
#                 if(successor.ID == goal_node):
#                     visited_nodes_in_order.append(successor)
#                     fringe.clear()
#                     return visited_nodes_in_order
#                 fringe.append(successor)
#                 visited_nodes_in_order.append(successor)


    
#     # if goal node isn't found, add goal node, as specified in assignment
#     if len(visited_nodes_in_order) > 0 and visited_nodes_in_order[-1] != goal_node:
#         visited_nodes_in_order.append(goal_node)



#     return visited_nodes_in_order

# def DFS(starting_node, goal_node):
#     """
#     This function implements the depth first search algorithm
    
#     Parameters:
#     - starting_node: The entry node into the graph
#     - goal_node: The integer ID of the goal node.
    
#     Returns:
#     A list containing the visited nodes in order they were visited with starting node
#     always being the first node and the goal node always being the last
#     """
#     visited_nodes_in_order = []
    
#     # YOUR CODE HERE
#     fringe = [starting_node]
#     exploredSet = set()
#     all_nodes = build_graph()
#     visited_nodes_in_order.append(starting_node)
    
#     # if starting node is goal
#     if(starting_node.ID == goal_node):
#         visited_nodes_in_order.append(all_nodes[str(goal_node)])
#         return visited_nodes_in_order

#     while(len(fringe) != 0):
#         poppedNode = fringe.pop(0)
#         exploredSet.add(poppedNode.ID)


#         if(poppedNode.ID == goal_node):
#             fringe.clear()
#             return visited_nodes_in_order
        
#         successors = sorted(poppedNode.connected_nodes, key= lambda nodeTup: nodeTup[1].ID)
#         siblingList = []
#         for cost, successor in successors:
#             if successor.ID not in exploredSet and successor not in fringe:
#                 siblingList.append(successor)
#                 visited_nodes_in_order.append(successor)
#         fringe = siblingList + fringe

#     # if goal node isn't found, add goal node, as specified in assignment
#     if len(visited_nodes_in_order) > 0 and visited_nodes_in_order[-1] != goal_node:
#         visited_nodes_in_order.append(goal_node)



    
#     return visited_nodes_in_order

# goal_node = 12

# print(BFS(build_graph()[0], goal_node))

# print(DFS(build_graph()[0], goal_node))

# Python program to print DFS traversal for complete graph
from collections import defaultdict

# This class represents a directed graph using adjacency
# list representation
class Graph:

	# Constructor
	def __init__(self):

		# default dictionary to store graph
		self.graph = defaultdict(list)

	# function to add an edge to graph
	def addEdge(self,u,v):
		self.graph[u].append(v)

	# A function used by DFS
	def DFSUtil(self, v, visited):

		# Mark the current node as visited and print it
		visited[v]= True
		print (v)

		# Recur for all the vertices adjacent to
		# this vertex
		for i in self.graph[v]:
			if visited[i] == False:
				self.DFSUtil(i, visited)


	# The function to do DFS traversal. It uses
	# recursive DFSUtil()
	def DFS(self):
		V = len(self.graph) #total vertices

		# Mark all the vertices as not visited
		visited =[False]*(V)

		# Call the recursive helper function to print
		# DFS traversal starting from all vertices one
		# by one
		for i in range(V):
			if visited[i] == False:
				self.DFSUtil(i, visited)


# Driver code
# Create a graph given in the above diagram
g = Graph()
g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 2)
g.addEdge(2, 0)
g.addEdge(2, 3)
g.addEdge(3, 3)

print ("Following is Depth First Traversal")
g.DFS()

# This code is contributed by Neelam Yadav
