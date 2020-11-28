import numpy as np
from queue import Queue

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
	riders[:,n+m+1] = 1
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
    # find unpair left hand side nodes
    left_candidate = set()
    for i in range(n):
        back_flow = False
        for j in range(m):
            back_flow |= residual_graph[n+1+j][i+1]
        if not back_flow:
            left_candidate.add(i)
    # Add right hand side nodes to based strictedSet on candidates
    strictedSet = set()
    for i in left_candidate:
        for j in range(m):
            if residual_graph[i+1][n+1+j] == 1:
                strictedSet.add(j)
    return strictedSet

def get_matching_result(original_graph, residual_graph):
    n = len(original_graph)
    m = len(original_graph[0])
    match = [-1] * n
    for i, res_row in enumerate(residual_graph[n+1: n+m+1]):
        for j, res_col in enumerate(res_row[1:n+1]):
            if res_col == 1:
                match[j] = i
                break
    return match

def get_payment(M, p):
    payment = [0] * len(M)
    for person, item in enumerate(M):
        payment[person] = p[item]
    return payment

def market_eq(n, m, v):
    p = [0] * m
    while 1:
        utility = calculateUtility(v, p)
        g = createGraph(utility)
        flow, res_g = max_matching(g)
        # Check perfect matching
        if flow != min(n, m):
            strictedSet = findConstrictedSet(g, res_g)
            # price increase
            for i in strictedSet:
                p[i] += 1
            # price shift
            if p.count(0) == 0:
                for i in p: i -= 1
        else:
            M = get_matching_result(g, res_g)
            payment = get_payment(M, p)
            return payment, M

# Q7, figure 8.3 test
if __name__ == "__main__":
    # 7(b)
    """
    n = 3
    m = 3
    values = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p, M = market_eq(n, m, values)
    print("Market equilibrium (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # 7(c), three self-generated test cases
    # test case 1
    """
    n = 6
    m = 6
    values = [[1, 5, 2, 8, 7, 3],
              [1, 3, 8, 9, 5, 6],
              [1, 7, 6, 5, 4, 3],
              [1, 7, 4, 3, 7, 1],
              [7, 6, 3, 3, 2, 5],
              [1, 8, 7, 3, 1, 5]]
    p, M = market_eq(n, m, values)
    print("Market equilibrium (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # test case 2
    """
    n = 8
    m = 8
    values = [[2, 9, 4, 5, 9, 4, 6, 5],
              [9, 4, 1, 8, 6, 6, 3, 3],
              [4, 1, 8, 1, 4, 8, 9, 5],
              [3, 4, 5, 5, 7, 7, 6, 7],
              [4, 1, 2, 8, 3, 7, 5, 9],
              [3, 9, 5, 4, 5, 8, 3, 6],
              [4, 6, 8, 9, 6, 4, 8, 6],
              [8, 2, 7, 2, 3, 9, 7, 5]]
    p, M = market_eq(n, m, values)
    print("Market equilibrium (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # test case 3
    """
    n = 10
    m = 10
    values = [[9, 3, 5, 1, 5, 6, 3, 5, 1, 6],
         [5, 9, 7, 9, 5, 3, 3, 5, 8, 1],
         [3, 6, 6, 8, 6, 3, 7, 6, 1, 8],
         [3, 8, 7, 3, 8, 2, 2, 4, 6, 3],
         [1, 6, 9, 5, 9, 3, 6, 6, 3, 7],
         [9, 4, 8, 5, 4, 5, 2, 9, 6, 2],
         [1, 1, 4, 5, 2, 5, 2, 7, 3, 1],
         [8, 4, 7, 8, 1, 6, 4, 3, 1, 3],
         [2, 6, 6, 8, 8, 9, 8, 7, 2, 4],
         [8, 5, 1, 9, 5, 6, 8, 8, 1, 5]]
    p, M = market_eq(n, m, values)
    print("Market equilibrium (p,M)")
    print("p:", p)
    print("M:", M)
    """