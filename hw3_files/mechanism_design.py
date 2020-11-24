import random
import numpy as np
import copy
from queue import Queue
from matplotlib import pyplot as plt
from matching_market import allocate

def vcg(value, price):
    M, _ = allocate(value, price)
    vcg_price = [0] * len(price)
    # sv
    sv = 0
    for player, item in M.items():
        sv += value[player][item]
    # ignore each player
    for player, item in M.items():
        # externailiy with plyer present = sv - player value
        ext_with = sv - value[player][item]
        # externailiy without plyer present
        val = copy.deepcopy(value)
        pri = [0] * len(price)
        #####v[player] = [-1] * len(value[player])
        val.pop(player)
        ext_without = 0
        m, _ = allocate(val, pri)
        for p, i in m.items():
            ext_without += val[p][i]
        # item price = player externailiy = ext_without - ext_with
        vcg_price[item] = ext_without - ext_with
    return M, vcg_price

if __name__ == "__main__":
    # Q8(c), figure 8.3 test
    v = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p = [0, 0, 0]
    M, vcg_p = vcg(v, p)
    print("VCG mechanism (M,p)")
    print("M:", M)
    print("p:", vcg_p)
    # Q8(c), three self-generated test cases
