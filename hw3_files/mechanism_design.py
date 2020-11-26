import copy
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
        # externailiy with player present = sv - player value
        ext_with = sv - value[player][item]
        # externailiy without player present
        val = copy.deepcopy(value)
        pri = [0] * len(price)
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
    """
    v = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p = [0, 0, 0]
    M, vcg_p = vcg(v, p)
    print("VCG mechanism (M,p)")
    print("M:", M)
    print("p:", vcg_p)
    """
    # Q8(c), three self-generated test cases
    # test case 1
    """
    v = [[9, 7, 6, 2, 3, 4],
         [4, 2, 6, 7, 1, 1],
         [8, 7, 5, 5, 6, 4],
         [1, 4, 5, 1, 9, 7]]
    p = [0, 0, 0, 0, 0, 0]
    M, vcg_p = vcg(v, p)
    print("VCG mechanism (M,p)")
    print("M:", M)
    print("p:", vcg_p)
    """
    # test case 2
    """
    v = [[4, 4, 4, 6],
         [8, 3, 6, 9],
         [2, 7, 4, 1],
         [8, 4, 7, 4],
         [6, 7, 7, 7],
         [3, 4, 4, 4]]
    p = [0, 0, 0, 0]
    M, vcg_p = vcg(v, p)
    print("VCG mechanism (M,p)")
    print("M:", M)
    print("p:", vcg_p)
    """
    # test case 3
    """
    v = [[3, 6, 1, 8, 6, 3, 8, 6],
         [6, 6, 2, 1, 6, 6, 3, 3],
         [2, 2, 1, 3, 9, 6, 9, 8],
         [4, 1, 1, 6, 8, 9, 2, 4],
         [8, 9, 8, 7, 3, 4, 7, 2],
         [2, 8, 7, 8, 5, 7, 1, 7],
         [8, 3, 7, 1, 3, 4, 5, 3],
         [5, 1, 4, 7, 2, 1, 5, 4]]
    p = [0, 0, 0, 0, 0, 0, 0, 0]
    M, vcg_p = vcg(v, p)
    print("VCG mechanism (M,p)")
    print("M:", M)
    print("p:", vcg_p)
    """