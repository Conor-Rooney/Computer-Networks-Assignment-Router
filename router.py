#Assignment 2 , computer networks 2
#Conor Rooney 17384796
#The following code is all my own work unless stated otherwise in the comments.

from collections import defaultdict
from pandas import DataFrame
from copy import deepcopy
import math

class Router():
	#The router class all share the same instance of graph, any changes to the graph will affect all routers.

	def __init__(self, name, graph):
		self.name = name
		self.graph = graph

	def __str__(self):
		return self.name

	#A helper function that simply returns the values rather than print them.
	def get_path_no_print(self, router2):
		copy = deepcopy(self)
		start, end, path, cost = dijkstra(copy.graph.routers, copy.name, router2)
		return start, end, path, cost

	#A function which takes two routers, self and another, and prints the path between them.
	#Uses djikstras function.
	#Creates a deep copy of the router and graph for the purposes of iteration in djikstras function.
	def get_path(self, router2):
		copy = deepcopy(self)
		start, end, path, cost = dijkstra(copy.graph.routers, copy.name, router2)
		print("Start: " + start)
		print("End: " + end)
		print("Path: " + path)
		print("Cost: " + cost)

	def get_routing_table(self):
		#creates a list of all other routers in the graph
		lst_routers = []
		for key, value in self.graph.routers.items():
			if key not in lst_routers and key != self.name:
				lst_routers.append(key)
			for subkey, subvalue in self.graph.routers[key].items():
				if subkey not in lst_routers and subkey != self.name:
					lst_routers.append(subkey)
		#stores all paths to other rooters from the current router in a list
		#Uses dataframe from the pandas module to print a table
		storage = []
		for router in lst_routers:
			copy = deepcopy(self)
			storage.append(copy.get_path_no_print(router))
		x = DataFrame(data=storage, columns=["From", "To", "Path", "Cost"])
		print(x)



class Graph():

	def __init__(self):
		self.routers = defaultdict()
	
	def add_edge(self, node_1, node_2, cost):
		#Using defaultdict, add the node to the tree if it is not a main entry
		#else add the associated path and cost to its' entry
		if node_1 not in self.routers:
			self.routers[node_1] = {}
		self.routers[node_1][node_2] = cost
		if node_2 not in self.routers:
			self.routers[node_2] = {}
		return self
#https://www.pythonpool.com/dijkstras-algorithm-python/
#The following implementation of Dijkstra's Algorithm was taken from the link above. All credit to the author(s).
#I implemented a small number of tweaks to this function to get it to work for the purposes of this assignment.
def dijkstra(graph,source,target):
	start = source
	end = target
	if source not in graph:
		raise TypeError ("Not in graph")
	# These are all the nodes which have not been visited yet
	unvisited_nodes=graph
	# It will store the shortest distance from one node to another
	shortest_distance={}
	# This will store the Shortest path between source and target node 
	route=[] 
	# It will store the predecessors of the nodes
	predecessor={}
	# Iterating through all the unvisited nodes
	for nodes in unvisited_nodes:
		# Setting the shortest_distance of all the nodes as infinty
		shortest_distance[nodes]=math.inf
	# The distance of a point to itself is 0.
	shortest_distance[source]=0
	# Running the loop while all the nodes have been visited
	while(unvisited_nodes):
		# setting the value of min_node as None
		min_Node=None
		# iterating through all the unvisited node
		for current_node in unvisited_nodes: 
			# For the very first time that loop runs this will be called
			if min_Node is None:
				# Setting the value of min_Node as the current node
				min_Node=current_node
			elif shortest_distance[min_Node] > shortest_distance[current_node]:
				# I the value of min_Node is less than that of current_node, set 
				#min_Node as current_node
				min_Node=current_node
		# Iterating through the connected nodes of current_node (for 
		# example, a is connected with b and c having values 10 and 3 
		# respectively) and the weight of the edges
		for child_node,value in unvisited_nodes[min_Node].items():
			# checking if the value of the current_node + value of the edge 
			# that connects this neighbor node with current_node
			# is lesser than the value that distance between current nodes 
			# and its connections
			if value + shortest_distance[min_Node] < shortest_distance[child_node]:  
				# If true  set the new value as the minimum distance of that connection
				shortest_distance[child_node] = value + shortest_distance[min_Node]
				# Adding the current node as the predecessor of the child node
				predecessor[child_node] = min_Node
		# After the node has been visited (also known as relaxed) remove it from unvisited node
		unvisited_nodes.pop(min_Node)
		
	# Till now the shortest distance between the source node and target node 
	# has been found. Set the current node as the target node 
	node = target
	
	# Starting from the goal node, we will go back to the source node and 
	# see what path we followed to get the smallest distance
	while node != source:
		
		# As it is not necessary that the target node can be reached from # the source node, we must enclose it in a try block
		try:
			route.insert(0,node)
			node = predecessor[node]
		except Exception:
			return(str(start), str(end), "0", "")
			break
	# Including the ssource in the path
	route.insert(0,source)
	
	# If the node has been visited,
	if shortest_distance[target] != math.inf:
		return (str(start), str(end), "->".join(route), str(shortest_distance[target]))

def remove_router(router):
	#get the universal graph for all routers
	graph = router.graph.routers
	#backup is the first router in the graph
	for key, value in sorted(graph.items()):
		first = key
		break
	backup = Router(first, router.graph)
	#remove all traces of the router from the graph
	new_graph = {key:value for key, value in backup.graph.routers.items() if key != router.name}
	for key, value in new_graph.items():
		x = {subkey : subvalue for subkey, subvalue in new_graph[key].items() if subkey != router.name}
		new_graph[key] = x
	backup.graph.routers = new_graph
	#print new routing table
	backup.get_routing_table()


def main():
	#example operations
	graph = Graph()
	routera = Router("a", graph)
	routerb = Router("b", graph)
	routerc = Router("c", graph)
	graph.add_edge("a", "b", 7)
	graph.add_edge("a", "c", 9)
	graph.add_edge("a", "f", 14)
	graph.add_edge("b", "c", 10)
	graph.add_edge("b", "d", 15)
	graph.add_edge("c", "d", 11)
	graph.add_edge("c", "f", 2)
	graph.add_edge("d", "e", 6)
	graph.add_edge("e", "f", 9)
	routera.get_path("f")
	print("----------")
	routerb.get_routing_table()
	print("----------")
	routera.get_routing_table()
	print("----------")
	remove_router(routerc)
	print("----------")
	routerb.get_routing_table()



if __name__ == '__main__':
	main()