class Node:
    """
    This class describes a single node contained within a graph. 
    It has the following instannce level attributes:
    
    ID: An integer id for the node i.e. 1
    """    
    def __init__(self, ID):
        self.ID = ID
        self.connected_nodes = []
        
    def __repr__(self):
        ID = self.ID
        if len(self.connected_nodes)==0:
            nodes = 'None'
        else:
            nodes = ','.join(str(cn[1].ID) for cn in self.connected_nodes)
        return '\nNode:{}\nConnected Nodes:{}'.format(ID, nodes)
        
    def set_connected_nodes(self,connected_nodes):
        """
        Adds edges that lead from this node to other nodes:
        
        Parameters:
        - connected_nodes: A list of tuples consisting of (cost, Node), 
                           where 'cost' is a floating point value 
                           indicating the cost to get from this node 
                           to 'Node' and 'Node' is a Node object
        """
        self.connected_nodes = connected_nodes
    
def build_graph():
    """
    Builds the graph to be parsed by the search algorithms.
    Returns: All nodes with connectivity in the graph
    """
    ids = range(13)
    coords = [(0,0), (1,1), (1,0), (1,1), (5,2), (3,1), (3,0), 
              (3,-1), (5,1), (4,1), (4,0), (4,-2), (7,0)]
    
    #https://en.wikipedia.org/wiki/Euclidean_distance
    euclidean_distance = lambda x1y1, x2y2: ((x1y1[0]-x2y2[0])**2 +  (x1y1[1]-x2y2[1])**2)**(0.5)
    
    def build_connected_node_list(from_id, to_ids):
        starting_coords = coords[from_id]
        
        connected_nodes = []
        for to_id in to_ids:
            connected_nodes.append((euclidean_distance(starting_coords, coords[to_id]), all_nodes[to_id]))
            
        return connected_nodes
    
    goal_coords = (7,0)
    all_nodes = [Node(_id) for _id in ids]
    
    all_nodes[8].set_connected_nodes(build_connected_node_list(8, [12]))
    all_nodes[10].set_connected_nodes(build_connected_node_list(10,[12]))
    all_nodes[5].set_connected_nodes(build_connected_node_list(5, [8]))
    all_nodes[6].set_connected_nodes(build_connected_node_list(6, [9, 10]))
    all_nodes[7].set_connected_nodes(build_connected_node_list(7, [11]))
    all_nodes[1].set_connected_nodes(build_connected_node_list(1, [4,5]))
    all_nodes[2].set_connected_nodes(build_connected_node_list(2, [5,6]))
    all_nodes[3].set_connected_nodes(build_connected_node_list(3, [7]))
    all_nodes[0].set_connected_nodes(build_connected_node_list(0, [1,2,3]))
    
    return all_nodes


build_graph()


def BFS(starting_node, goal_node):
    """
    This function implements the breath first search algorithm
    
    Parameters:
    - starting_node: The entry node into the graph
    - goal_node: The integer ID of the goal node.
    
    Returns:
    A list containing the visited nodes in order they were visited with starting node
    always being the first node and the goal node always being the last
    """
    visited_nodes_in_order = []
    
    # YOUR CODE HERE
    # raise NotImplementedError()
    explored_list = []
    frontier = []
    frontier.append(starting_node)
    expanded_list = []
    visited_node = frontier.pop(0)
    while visited_node.ID != goal_node :
        visited_nodes_in_order.append(visited_node)
        explored_list.append(visited_node)
        expanded_list = visited_node.connected_nodes
        for i in expanded_list :
          if i not in explored_list :
            frontier.append(i)
        distance,visited_node = frontier.pop(0)
    
    return visited_nodes_in_order

def DFS(starting_node, goal_node):
    """
    This function implements the depth first search algorithm
    
    Parameters:
    - starting_node: The entry node into the graph
    - goal_node: The integer ID of the goal node.
    
    Returns:
    A list containing the visited nodes in order they were visited with starting node
    always being the first node and the goal node always being the last
    """
    visited_nodes_in_order = []
    
    # YOUR CODE HERE
    raise NotImplementedError()
    
    return visited_nodes_in_order


goal_node = 12

print(BFS(build_graph()[0], goal_node))

print(DFS(build_graph()[0], goal_node))