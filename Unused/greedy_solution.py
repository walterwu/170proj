import networkx as nx
from utils import construct_cluster_graph
from utils import format_output_cycles
from utils import find_total_penalty
from utils import create_graph
from utils import add_solutions
import multiprocessing
import time
import sys

def greedy_algorithm(G):
	CG = construct_cluster_graph(G)
	CG_copy = CG.copy()
	print "done constructing"
	valid_nodes = CG.nodes()
	selected_clusters = []
	pre_penalty = 0
	while len(valid_nodes) != 0:
		# node_selected = find_max_penalty(valid_nodes, CG)
		node_selected = find_min_weighted_degree(valid_nodes, CG)
		pre_penalty += CG.node[node_selected]['penalty']
		selected_clusters.append(node_selected)
		list_edges = CG.edges(node_selected, False)
		nodes_to_remove = set()
		nodes_to_remove.add(node_selected)
		for edge in list_edges:
			nodes_to_remove.add(edge[0])
			nodes_to_remove.add(edge[1])
		for node in nodes_to_remove:
			valid_nodes.remove(node)
			CG.remove_node(node)
	list_cycles = []
	for cluster in selected_clusters:
		list_cycles.append(CG_copy.node[cluster]['nodes'])
	penalty = find_total_penalty(G) - pre_penalty
	output_string = format_output_cycles(list_cycles)
	print(find_total_penalty(G), pre_penalty)
	return [output_string, penalty]
	
def find_max_penalty(node_list, CG):
	max_penalty = 0
	max_node = None
	for node in node_list:
		penalty = CG.node[node]['penalty']
		if penalty > max_penalty:
			max_penalty = penalty
			max_node = node
	return max_node

def find_min_weighted_degree(node_list, CG):
	min_weighted_degree = sys.maxsize
	selected_node = None
	for node in node_list:
		penalty = CG.node[node]['penalty']
		neighbor_penalty = 0
		list_edges = CG.edges(node, False)
		neighbors = set()
		for edge in list_edges:
			if edge[0] is not node:
				neighbors.add(edge[0])
			if edge[1] is not node:
				neighbors.add(edge[1])
		for n in neighbors:
			neighbor_penalty += CG.node[n]['penalty']
		weighted_degree = neighbor_penalty/penalty
		if weighted_degree < min_weighted_degree:
			min_weighted_degree = weighted_degree
			selected_node = node
	return selected_node

def execute_greedy(index):
	filename = "instances/" + str(index) + ".in"
	G = create_graph(filename)
	solution = greedy_algorithm(G)
	formatted_solution = [index, "Greedy", solution[1], solution[0]]
	list_solutions = [formatted_solution]
	add_solutions(list_solutions)

def timed_execution():
	if __name__ == '__main__':
    	# Start foo as a process
		for index in range(1,493):
			print("Processing input " + str(index) + ".")
			p = multiprocessing.Process(target=execute_greedy, name="execute_greedy", args=(index,))	
			p.start()
 			# Wait 10 seconds for foo
			time.sleep(3)
			if p.is_alive():
				print("Process " + str(index) + " still running. Killing.")
				p.terminate()
				# Cleanup
				p.join()
			p.join()

timed_execution()







