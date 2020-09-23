import queue
import random
import networkx as nx

# given number of nodes n and probability p, output a random graph 
# as specified in homework
def create_graph(n, p):
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                G.add_edge(i, j)
    return G

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G, i, j):
    q = queue.Queue()
    q.put((i, 0))
    visited = [0 for _ in range(G.number_of_nodes())]
    visited[i] = 1
    while not q.empty():
        n, leng = q.get()
        for neighbor in G.neighbors(n):
            if visited[neighbor] == 0:
                if neighbor == j: return leng + 1
                visited[neighbor] = 1
                q.put((neighbor, leng+1))
    return "infinity"

def avg_shortest_path(G, verbal):
    rep = 1000
    shortest_path_sum = 0
    while rep != 0:
        i, j = random.sample(range(G.number_of_nodes()), 2)
        if i == j: continue
        s = shortest_path(G, i, j)
        if s == "infinity": continue
        shortest_path_sum += s
        rep -= 1
        if verbal == 1: yield i, j, s
    if verbal == 0:
        yield shortest_path_sum / 1000

# 8.c
G = create_graph(1000, 0.1)
f = open(r"./avg_shortest_path.txt", "w")
for i, j, s in avg_shortest_path(G, 1):
    f.writelines("({}, {}, {})\r".format(i, j, s))
for l in avg_shortest_path(G, 0):
    print("avg shortest path with 1000 nodes and p=0.1: ", l)
f.close()

# 8.d
f = open(r"./varying_p.txt", "w") 
f.writelines("p, avg_shortest_path\r")
for p in range(4, 0, -1):
    p = p * 0.01
    G = create_graph(1000, p)
    for l in avg_shortest_path(G, 0):
        f.writelines("{}, {}\r".format(p, l))
for p in range(5, 55, 5):
    p = p * 0.01
    G = create_graph(1000, p)
    l = avg_shortest_path(G, 0)
    for l in avg_shortest_path(G, 0):
        f.writelines("{}, {}\r".format(p, l))
f.close()

# 9.a
f = open(r"./facebook_combined.txt", "r")
G = create_graph(4039, 0)
for l in f:
    n1, n2 = l.split()
    G.add_edge(int(n1), int(n2))
f.close()
f = open(r"./fb_shortest_path.txt", "w")
for i, j, s in avg_shortest_path(G, 1):
    f.writelines("({}, {}, {})\r".format(i, j, s))
f.close()

# 9.c
for l in avg_shortest_path(G, 0):
    print("Fb avg shortest path: ", l)
# Estimation with p = 0.0108
G2 = create_graph(4039, 0.0108)
for l in avg_shortest_path(G2, 0):
    print("Estimated avg shortest path: ", l)