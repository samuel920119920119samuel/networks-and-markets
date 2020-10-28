# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# 9 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.
import random
import numpy as np
from queue import Queue
from matplotlib import pyplot as plt

def print_g(g):
    for i in g: print(i)

def bfs(res_g, s, t, p):
    # create q and a map for checking whether a node has visited or not
    q = Queue()
    visited = [0] * len(res_g)
    # init
    q.put(s)
    visited[s] = 1
    # bfs loop
    while not q.empty():
        u = q.get()
        for v, val in enumerate(res_g[u]):
            if not visited[v] and val > 0:
                q.put(v)
                visited[v] = 1
                p[v] = u
    return visited[t] == True

def max_flow(g, s, t):
    # create a residiual graph
    res_g = [[g[u][v] for v in range(len(g[0]))] for u in range(len(g))]
    # record of path
    p = [-1] * len(g)
    m_flow = 0
    # Augumenting path
    while bfs(res_g, s, t, p):
        res_cap = float('Inf')
        # find min flow from available path
        cur_t = t
        while cur_t != s:
            res_cap = min(res_cap, res_g[p[cur_t]][cur_t])
            cur_t = p[cur_t]
        # update residuel graph
        cur_t = t
        while cur_t != s:
            cur_p = p[cur_t]
            res_g[cur_p][cur_t] -= res_cap
            res_g[cur_t][cur_p] += res_cap
            cur_t = p[cur_t]
        # add flow to overall flow
        m_flow += res_cap
    # print_g(res_g)
    
    return m_flow

# test case from figure 6.1
g_6_1 = [
    [0, 1, 3, 0],
    [0, 0, 2, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]
# print(max_flow(g_6_1, 0, 3))

# test case from figure 6.3
# s, x1, x2, x3, x4, x5, y1, y2, y3, y4, y5, t
g_6_3 = [
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# print(max_flow(g_6_3, 0, 11))

# takes a 2d array of driver matches, n x m for drivers by riders
def max_matching(G):
	n = len(G)
	m = len(G[0])
	source = np.ones(n, dtype=np.int)
	source = np.pad(source, [(1,m+1)], mode='constant')
	sink = np.zeros(n+m+2, dtype=np.int)
	drivers = np.array(G)
	drivers = np.pad(drivers, [(0,0), (n + 1, 1)], mode='constant')
	riders = np.zeros((m, n+m+2), dtype = np.int)
	riders[:,n+m+1] = 1
	biGraph = np.concatenate(([source],drivers, riders, [sink]), axis=0)

	return max_flow(biGraph, 0, m+n+1) # a matching

def createDriverGraph(n,m, p):
	driverGraph = [[0 for x in range(m)] for y in range(n)]
	for x in range(n):
		for y in range(m):
			if random.uniform(0, 1) < p:
				driverGraph[x][y] = 1
	return driverGraph

match_test1 = [
    [0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 1, 0]
]

match_test2 = [
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0]
]

# print(max_matching(match_test1))
# print(max_matching(match_test2))

"""
test_time = 10
n = 100
for p in range(101):
    p = p / 100
    fullMatches = 0
    for rep in range(test_time):
        driverGraph = createDriverGraph(n, n, p)
        matches = max_matching(driverGraph)
        if matches == 100:
            fullMatches += 1
    print(p, ",", fullMatches / test_time)
"""