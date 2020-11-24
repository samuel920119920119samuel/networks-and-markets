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
    return m_flow, res_g

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
	riders[:,n+m+1] = n
	biGraph = np.concatenate(([source],drivers, riders, [sink]), axis=0)
	return max_flow(biGraph, 0, m+n+1) # a matching

def calculateUtility(values, price):
    utility = []
    for person_v in values:
        person_u = []
        for i, item_v in enumerate(person_v):
            person_u.append(item_v - price[i])
        utility.append(person_u)
    return utility

def createGraph(utility):
    graph = [[0 for _ in range(len(utility[0]))] for _ in range(len(utility))]
    for person_i, person_u in enumerate(utility):
        for item_i, u in enumerate(person_u):
            if u == max(person_u):
                graph[person_i][item_i] = 1 
    return graph

def findConstrictedSet(original_graph, residual_graph):
    n = len(original_graph)
    m = len(original_graph[0])
    strictedSet = set()
    for i, res in enumerate(residual_graph[n+1: n+m+1]):
        if res[1:n+1].count(1) > 1:
            strictedSet.add(i)
    return strictedSet

def get_matching_result(original_graph, residual_graph):
    n = len(original_graph)
    m = len(original_graph[0])
    match = {}
    for i, res_row in enumerate(residual_graph[n+1: n+m+1]):
        for j, res_col in enumerate(res_row[1:n+1]):
            if res_col == 1:
                match[j] = i
                break
    return match

def allocate(v, p):
    while 1:
        utility = calculateUtility(v, p)
        g = createGraph(utility)
        _, res_g = max_matching(g)
        strictedSet = findConstrictedSet(g, res_g)
        if len(strictedSet) != 0:
            # price increase
            for i in strictedSet:
                p[i] += 1
            # price shift
            if p.count(0) != 0:
                for i in p: i -= 1
        else:
            M = get_matching_result(g, res_g)
            return M, p

# Q7, figure 8.3 test
if __name__ == "__main__":
    # 7(a)
    """
    v = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p = [0, 0, 0]
    utility = calculateUtility(v, p)
    g = createGraph(utility)
    _, res_g = max_matching(g)
    strictedSet = findConstrictedSet(g, res_g)
    if len(strictedSet) != 0:
        print("Stricted set:", strictedSet)
    else:
        print("Perfect matching!")
    """
    # 7(b)
    """
    v = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p = [0, 0, 0]
    M, p = allocate(v, p)
    print("Market equilibrium (M,p)")
    print("M:", M)
    print("p:", p)
    """
    # 7(c)
    