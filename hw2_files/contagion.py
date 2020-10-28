# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 8 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.
import numpy as np
import random

def facebook_graph(n):
	graph = [[0 for x in range(n)] for y in range(n)]
	fb_data = open("facebook_combined.txt")
	Lines = fb_data.readlines()
	for line in Lines:
		item = line.split();
		graph[int(item[0])][int(item[1])] = 1;
		graph[int(item[1])][int(item[0])] = 1;
	return graph

fbGraph = facebook_graph(4039)

# Contagion BRD returns the number of nodes infected
def contagion_brd(G, S, q):
	changes = 1;
	while changes != 0:
		changes = 0
		for index, node in enumerate(G):
			if(not index in S):
				neighbors = np.sum(np.array(node))
				infectedNodes = np.sum(np.take(np.array(node), S))
				if infectedNodes/neighbors > q:
					S.append(index)
					changes +=1
	return len(S)


# Part A Verification Code
# Figure 4.1 graph a
graph4_1_a = [[0,1,0,0], [1,0,1,0], [0,1,0,1], [0,0,1,0]]
S_4_1_a = [0,1]
# Without Complete Cascade
# print(contagion_brd(graph4_1_a, S_4_1_a, 0.5))
# With Complete Cascade achieve by lowering q to 0.4
# print(contagion_brd(graph4_1_a, S_4_1_a, 0.4))

# Figure 4.1 graph b
graph4_1_b = [[0,1,0,0,0,0,0],
		      [1,0,1,1,0,0,0],
		      [0,1,0,0,0,0,0], 
		      [0,1,0,0,1,1,0], 
		      [0,0,0,1,0,0,0], 
		      [0,0,0,0,1,0,1], 
		      [0,0,0,0,0,1,0]]
S_4_1_b = [0,1,2]
# Without Complete Cascade
# print(contagion_brd(graph4_1_b, S_4_1_b, 1/3))
# With Complete Cascade achieve by lowering q to 1/4
# print(contagion_brd(graph4_1_b, S_4_1_b, 1/4))


"""
# 8(b)
totalInfected = 0
totalContagions = 0
for i in range(0, 100):
 	print(i)
 	startS = random.sample(range(0, len(fbGraph)), 10)
 	infected = contagion_brd(fbGraph, startS, 0.1 )
 	totalInfected += infected
 	print("Count Infected: %s" % (infected,))
 	if infected ==len(fbGraph):
 		totalContagions += 1
 		print("CONTAGION")

print("Average Infected: %d" % (totalInfected/100,))
"""


data = open("fb_contagion_rates.txt", "a")
data.truncate(0)
data.write("q, k, average, numCascades(out of 10)")
"""
# 8(c)
for q in range(0, 55, 5):
 	print(q/100)
 	for k in range(0, 260, 10):
 		print(k)
 		totalInfected=0
 		totalContagions=0
 		for i in range(0, 10):
 			startS = random.sample(range(0, len(fbGraph)), k)
 			infected = contagion_brd(fbGraph, startS, q/100 )
 			totalInfected += infected
 			# print("Count Infected: %s", (infected,))
 			if infected ==len(fbGraph):
 				totalContagions += 1
 				# print("CONTAGION")
 		if totalContagions == 10:
 			break
 		print("(%s, %s, %s,%d)\n" % (q/100,k,totalInfected/10, totalContagions))
 		data.write("(%s, %s, %s,%d)\n" % (q/100,k,totalInfected/10, totalContagions)) 
		

print("Average Infected: %d", (totalInfected/100,))
"""
"""
# Filling out the data points
q = 20
for k in range(130, 260, 10):
	print(k)
	totalInfected=0
	totalContagions=0
	for i in range(0, 10):
		startS = random.sample(range(0, len(fbGraph)), k)
		infected = contagion_brd(fbGraph, startS, q/100 )
		totalInfected += infected
		# print("Count Infected: %s", (infected,))
		if infected ==len(fbGraph):
			totalContagions += 1
				# print("CONTAGION")
	print("(%s, %s, %s,%d)\n" % (q/100,k,totalInfected/10, totalContagions))
	data.write("(%s, %s, %s,%d)\n" % (q/100,k,totalInfected/10, totalContagions))
"""
