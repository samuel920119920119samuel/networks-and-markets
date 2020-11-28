import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Global Variable
N = 100 # Grid length
RIDE_VALUE = 100

# Some helper functions for Part 5
# you may use these or define your own. Make sure it is clear where your solutions are

# compute the manhattan distance between two points a and b (represented as pairs)

# Part 5 - Q10
# Exchange Network Implementation
def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def generate_riders(n, num_of_riders) -> dict:
    # Rider is represented by "tuple(position): dist_to_destination"
    riders = {}
    for i in range(num_of_riders):
        pos = (np.random.randint(n), np.random.randint(n))
        dest = (np.random.randint(n), np.random.randint(n))
        regenerate_count = 0
        while dist(pos, dest) >= RIDE_VALUE or pos in riders:
            pos = (np.random.randint(n), np.random.randint(n))
            dest = (np.random.randint(n), np.random.randint(n))
        riders[pos] = dist(pos, dest)
        print('rider #', i, pos, dest, dist(pos, dest))
    return riders

def generate_drivers(n, num_of_drivers, riders) -> set:
    # Driver is represented by "tuple(position)"
    drivers = set()
    min_rider_cost = min(riders.values())
    for i in range(num_of_drivers):
        pos = (np.random.randint(n), np.random.randint(n))
        min_driver_cost = min([dist(r, pos) for r in riders])
        while pos in drivers or (min_rider_cost + min_driver_cost) >= RIDE_VALUE: # drop duplicates 
        # and drop drivers that will result in all negative utilities
            pos = (np.random.randint(n), np.random.randint(n))
        drivers.add(pos)
    print('drivers:', drivers)
    return drivers

def create_graph(riders, drivers):
    G = nx.Graph()
    for r in riders:
        for d in drivers:
            # weight on the edge is equal to the value of the ride minus 
            # rider's distance to destination and driver's distance to the rider
            w = RIDE_VALUE - riders[r] - dist(r, d)
            if w < 0:
                w = 0
            G.add_edge(r, d, weight=w)
    return G

# Give a representation for riders/ drivers somewhere which can be included in your graph used in stable_outcome

# Given a (bipartite) graph G with edge values specified by v, 
# output a stable outcome (M,a) consisting of a matching and allocations

def stable_outcome(G, small, big):
    # As the edge values are already stored in G, the parameter 'v' is removed here. 
    # G_0 is used for computing the eq 
    G_0 = G.copy()
    # a is a dict in which the key is the (rider, driver) pair and the value is the (discount, profit) they get respectively
    a = {}
    # Init allocation
    for r in small:
        for d in big:
            # Start with rider getting all the utility
            a[(r, d)] = [G.get_edge_data(r, d)['weight'], 0]

    matched_num = len(small)
    matched, constricted_set = determine_stable(G_0, small, big)
    while len(matched) < matched_num:
        a = price_modify(a, list(constricted_set))
        G_0 = G.copy()
        G_0 = update_weights(G_0, a)
        matched, constricted_set = determine_stable(G_0, small, big)
    # M is a graph showing the matches
    
    M = nx.Graph()
    for r in small:
        max_w = get_preferred(G_0, r)
        adjacent_nodes = list(G_0.neighbors(r))
        for d in adjacent_nodes:
            if G_0.get_edge_data(r, d)['weight'] != max_w:
                G_0.remove_edge(r, d)
    
    for r in small:
        adjacent_nodes = list(G_0.neighbors(r))
        if len(adjacent_nodes) == 1:
            M.add_edge(r, adjacent_nodes[0], weight =
                       G_0.get_edge_data(r, adjacent_nodes[0])['weight'])

    for edge in G_0.edges:
        if edge[0] in M.nodes or edge[1] in M.nodes:
            continue
        else:
            M.add_edge(*edge, weight=G_0.get_edge_data(*edge)['weight'])
    
    for pair in a:
        if M.has_edge(*pair) == False:
            a.pop(pair)
    nx.draw(M, with_labels=True)
    print('allocation:', a)
    print('match results:')
    for e in M.edges:
        print(e, M.get_edge_data(*e)['weight'])
    return (M,a)

def determine_stable(G, small, big):
    matched = set()
    constricted_set = set()
    for node in small:
        max_w = get_preferred(G, node)
        for d in G.neighbors(node):
            if G.get_edge_data(node, d)['weight']==max_w:
                if d in matched:
                    constricted_set.add(d)
                matched.add(d)
    return matched, constricted_set

def price_modify(a, constricted_set):
    # Price Increase
    for d in constricted_set:
        for pair in a:
            if d in pair:
                a[pair][0] -= 1
                a[pair][1] += 1
    # Price Shift
    prices = [a[x][1] for x in a]
    if min(prices) > 0:
        for pair in a:
            a[pair][0] += 1
            a[pair][1] -= 1
    return a

def get_preferred(G, node):
    adjacent_nodes = G.neighbors(node)
    weights = []
    for d in adjacent_nodes:
        weights.append(G.get_edge_data(node, d)['weight'])
    return max(weights)

def update_weights(G, a):
    for pair in a:
        G.get_edge_data(*pair)['weight'] = a[pair][0]
    return G


# Part 5 - Q11 (a)
riders = generate_riders(N, 6)
drivers = generate_drivers(N, 6, riders)
G = create_graph(riders, drivers)
utilities = {}
for e in G.edges:
    utilities[str(e)] = G.get_edge_data(*e)['weight']
print('Graph:')
print(json.dumps(utilities, default=str, indent=4))

M, a = stable_outcome(G, riders, drivers)

'''
Example 1:
rider # 0 (1, 7) (21, 33) 46
rider # 1 (36, 43) (23, 15) 41
rider # 2 (86, 91) (84, 74) 19
rider # 3 (28, 42) (65, 68) 63
rider # 4 (37, 83) (20, 38) 62
drivers: {(1, 22), (38, 74), (2, 43), (69, 57), (30, 74)}
Graph:
{
    "((1, 7), (1, 22))": 39,
    "((1, 7), (38, 74))": 0,
    "((1, 7), (2, 43))": 17,
    "((1, 7), (69, 57))": 0,
    "((1, 7), (30, 74))": 0,
    "((1, 22), (36, 43))": 3,
    "((1, 22), (86, 91))": 0,
    "((1, 22), (28, 42))": 0,
    "((1, 22), (37, 83))": 0,
    "((38, 74), (36, 43))": 26,
    "((38, 74), (86, 91))": 16,
    "((38, 74), (28, 42))": 0,
    "((38, 74), (37, 83))": 28,
    "((2, 43), (36, 43))": 25,
    "((2, 43), (86, 91))": 0,
    "((2, 43), (28, 42))": 10,
    "((2, 43), (37, 83))": 0,
    "((69, 57), (36, 43))": 12,
    "((69, 57), (86, 91))": 30,
    "((69, 57), (28, 42))": 0,
    "((69, 57), (37, 83))": 0,
    "((30, 74), (36, 43))": 22,
    "((30, 74), (86, 91))": 8,
    "((30, 74), (28, 42))": 3,
    "((30, 74), (37, 83))": 22
}
allocation: {((1, 7), (1, 22)): [39, 0], ((36, 43), (30, 74)): [22, 0], ((86, 91), (69, 57)): [30, 0], 
((28, 42), (2, 43)): [7, 3], ((37, 83), (38, 74)): [24, 4]}
match results:
((1, 7), (1, 22)) 39
((86, 91), (69, 57)) 30
((28, 42), (2, 43)) 7
((37, 83), (38, 74)) 24
((30, 74), (36, 43)) 22

'''

'''
Example 2:
rider # 0 (49, 3) (30, 33) 49
rider # 1 (10, 17) (45, 9) 43
rider # 2 (65, 92) (93, 42) 78
rider # 3 (90, 56) (73, 42) 31
rider # 4 (83, 48) (73, 49) 11
drivers: {(8, 23), (25, 56), (72, 63), (22, 6), (91, 86)}
Graph:
{
    "((49, 3), (8, 23))": -10,
    "((49, 3), (25, 56))": -26,
    "((49, 3), (72, 63))": -32,
    "((49, 3), (22, 6))": 21,
    "((49, 3), (91, 86))": -74,
    "((8, 23), (10, 17))": 49,
    "((8, 23), (65, 92))": -104,
    "((8, 23), (90, 56))": -46,
    "((8, 23), (83, 48))": -11,
    "((25, 56), (10, 17))": 3,
    "((25, 56), (65, 92))": -54,
    "((25, 56), (90, 56))": 4,
    "((25, 56), (83, 48))": 23,
    "((72, 63), (10, 17))": -51,
    "((72, 63), (65, 92))": -14,
    "((72, 63), (90, 56))": 44,
    "((72, 63), (83, 48))": 63,
    "((22, 6), (10, 17))": 34,
    "((22, 6), (65, 92))": -107,
    "((22, 6), (90, 56))": -49,
    "((22, 6), (83, 48))": -14,
    "((91, 86), (10, 17))": -93,
    "((91, 86), (65, 92))": -10,
    "((91, 86), (90, 56))": 38,
    "((91, 86), (83, 48))": 43
}
allocation: {((49, 3), (22, 6)): [21, 0], ((10, 17), (8, 23)): [49, 0], ((65, 92), (91, 86)): [-44, 34], ((90, 56), (25, 56)): [4, 0], ((83, 48), (72, 63)): [23, 40]}
match results:
((49, 3), (22, 6)) 21
((10, 17), (8, 23)) 49
((65, 92), (91, 86)) -44
((25, 56), (90, 56)) 4
((72, 63), (83, 48)) 23
'''

# Part 5 - Q11(b)

def get_prices_and_profits(M, a, riders_less = True):
    if riders_less:
        prices = np.array([a[x][0] for x in a])
        profits = np.array([a[x][1] for x in a])
    else:
        prices = np.array([a[x][1] for x in a])
        profits = np.array([a[x][0] for x in a])
    return np.mean(prices[prices>=0]), np.mean(profits[profits>=0])

# Case 1: r = d
avg_prices = []
avg_profits = []
for i in range(50):
    riders = generate_riders(N, 10)
    drivers = generate_drivers(N, 10, riders)
    G = create_graph(riders, drivers)
    M, a = stable_outcome(G, riders, drivers)
    avg_price, avg_profit = get_prices_and_profits(M, a)
    avg_prices.append(avg_price)
    avg_profits.append(avg_profit)
print('avg_prices:', avg_prices)
print('avg_profits:', avg_profits)

'''
avg_prices: [2.0, 40.2, 16.333333333333332, 39.75, 19.8, 5.0, 18.25, 25.75, 21.0, 16.0, 17.4, 24.333333333333332, 
    12.666666666666666, 33.166666666666664, 43.25, 19.25, 23.2, 14.833333333333334, 24.666666666666668, 
    31, 25.0, 28.714285714285715, 17.666666666666668, 7.666666666666667, 32.5, 
    18.0, 33.5, 30.0, 38.5, 11.0, 25.0, 10.0, 35.25, 35.0, 19.0, 17.333333333333332, 
    16.5, 28.2, 7.666666666666667, 15.4, 16.0, 21.0, 33.8, 47.857142857142854, 25.0, 
    15.0, 25.833333333333332, 17.0, 11.142857142857142, 13.833333333333334]
avg_profits: [28.857142857142858, 12.4, 24.75, 25.11111111111111, 20.0, 42.75, 25.4, 20.2, 
    35.0, 32.0, 17.4, 31.6, 13.9, 19.5, 5.222222222222222, 2.1, 18.88888888888889, 8.88888888888889, 
    23.3, 53.75, 33.333333333333336, 4.9, 18.4, 23.555555555555557, 19.0, 35.44444444444444, 21.666666666666668, 
    28.0, 35.5, 32.375, 8.88888888888889, 12.444444444444445, 15.555555555555555, 23.9, 14.11111111111111, 23.7, 
    30.88888888888889, 15.8, 55.888888888888886, 18.22222222222222, 28.0, 34.55555555555556, 15.333333333333334, 
    3.5555555555555554, 29.9, 43.25, 14.0, 43.333333333333336, 14.444444444444445, 25.9]
'''

# Case 2: r < d
avg_prices = []
avg_profits = []
for i in range(50):
    riders = generate_riders(N, 5)
    drivers = generate_drivers(N, 20, riders)
    G = create_graph(riders, drivers)
    M, a = stable_outcome(G, riders, drivers)
    avg_price, avg_profit = get_prices_and_profits(M, a)
    avg_prices.append(avg_price)
    avg_profits.append(avg_profit)
print('avg_prices:', avg_prices)
print('avg_profits:', avg_profits)

'''
avg_prices: [50.0, 28.5, 27.6, 24.5, 45.666666666666664, 38.333333333333336, 25.0, 16.0, 31.0, 
    27.0, 42.666666666666664, 34.2, 14.666666666666666, 21.5, 49.5, 34.25, 37.4, 31.8, 
    48.666666666666664, 34.666666666666664, 29.25, 28.333333333333332, 79.0, 45.75, 
    18.0, 32.333333333333336, 20.0, 31.5, 31.75, 20.666666666666668, 28.666666666666668, 49.0, 
    60.0, 16.25, 36.6, 42.25, 37.5, 29.25, 32.5, 44.6, 25.2, 32.666666666666664, 46.333333333333336, 
    28.0, 42.333333333333336, 21.0, 30.4, 49.666666666666664, 27.8, 26.25]
avg_profits: [2.8, 0.0, 0.8, 0.0, 1.4, 0.8, 0.2, 1.4, 0.0, 4.0, 6.6, 0.0, 
    0.6, 0.0, 0.0, 6.0, 0.6, 0.0, 3.6, 0.0, 1.8, 0.0, 0.0, 0.0, 1.2, 0.0, 0.0, 
    4.8, 0.4, 5.5, 1.8, 0.0, 1.2, 0.0, 0.0, 0.0, 0.0, 1.4, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.6, 0.0, 0.0]
'''

# Case 3: r > d
avg_prices = []
avg_profits = []
for i in range(50):
    riders = generate_riders(N, 20)
    drivers = generate_drivers(N, 5, riders)
    G = create_graph(riders, drivers)
    M, a = stable_outcome(G, drivers, riders)
    avg_price, avg_profit = get_prices_and_profits(M, a, riders_less=False)
    avg_prices.append(avg_price)
    avg_profits.append(avg_profit)
print('avg_prices:', avg_prices)
print('avg_profits:', avg_profits)

'''
avg_prices: [6.8, 7.8, 6.2, 5.6, 6.75, 2.4, 23.0, 6.8, 4.8, 0.0, 6.0, 
    17.0, 8.0, 6.0, 2.4, 2.6, 4.6, 0.0, 4.0, 7.6, 4.8, 0.0, 2.6, 3.4, 6.8, 
    0.6, 1.0, 2.0, 2.8, 13.6, 0.0, 7.2, 5.6, 4.0, 10.6, 5.0, 3.5, 2.4, 5.4, 1.8, 
    3.2, 13.0, 3.8, 2.2, 10.8, 16.2, 15.4, 3.4, 5.2, 0.0]
avg_profits: [46.4, 29.0, 26.8, 32.5, 28.666666666666668, 57.6, 23.5, 33.0, 27.25, 54.6, 
    33.4, 17.4, 26.0, 32.75, 48.0, 42.6, 40.4, 31.6, 26.2, 35.2, 25.6, 27.6, 51.6, 44.4, 
    30.8, 32.0, 28.5, 47.0, 43.2, 27.5, 63.4, 41.2, 48.8, 31.0, 32.6, 43.8, 37.5, 43.8, 
    40.8, 62.0, 38.6, 30.666666666666668, 56.0, 47.8, 23.8, 13.25, 17.0, 42.6, 20.2, 26.8]
'''