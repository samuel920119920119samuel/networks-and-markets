import copy
from matching_market import market_eq, get_payment

def vcg(n, m, value):
    _, M = market_eq(n, m, value)
    vcg_price = [0] * m
    # sv
    sv = 0
    for player, item in enumerate(M):
        if item == -1: continue
        sv += value[player][item]
    # ignore each player
    for player, item in enumerate(M):
        if item == -1: continue
        # externailiy with player present = sv - player value
        ext_with = sv - value[player][item]
        # externailiy without player present
        val = copy.deepcopy(value)
        val.pop(player)
        ext_without = 0
        _, matching = market_eq(n-1, m, val)
        for p, i in enumerate(matching):
            ext_without += val[p][i]
        # item price = player externailiy = ext_without - ext_with
        vcg_price[item] = ext_without - ext_with
    payment = get_payment(M, vcg_price)
    return payment, M

if __name__ == "__main__":
    # Q8(c), figure 8.3 test
    """
    n = 3
    m = 3
    values = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # Q8(c), three self-generated test cases
    # test case 1
    """
    n = 5
    m = 5
    values = [[1, 6, 5, 9, 2],
              [5, 8, 7, 6, 3],
              [9, 4, 3, 7, 8],
              [9, 4, 6, 8, 7],
              [3, 9, 6, 1, 2]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # test case 2
    """
    n = 8
    m = 8
    values = [[4, 6, 14, 8, 12, 9, 10, 11],
              [7, 13, 14, 8, 11, 9, 10, 4],
              [10, 5, 2, 1, 7, 6, 9, 4],
              [8, 11, 5, 9, 12, 1, 10, 3],
              [1, 13, 6, 11, 12, 7, 14, 5],
              [1, 10, 13, 11, 4, 9, 6, 8],
              [4, 6, 10, 12, 11, 1, 9, 13],
              [8, 13, 2, 14, 6, 12, 1, 5]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
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
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """