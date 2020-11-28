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
    n = 4
    m = 6
    values = [[9, 7, 6, 2, 3, 4],
              [4, 2, 6, 7, 1, 1],
              [8, 7, 5, 5, 6, 4],
              [1, 4, 5, 1, 9, 7]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # test case 2
    """
    n = 6
    m = 4
    values = [[4, 4, 4, 6],
              [8, 3, 6, 9],
              [2, 7, 4, 1],
              [8, 4, 7, 4],
              [6, 7, 7, 7],
              [3, 4, 4, 4]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """
    # test case 3
    """
    n = 8
    m = 8
    values = [[3, 6, 1, 8, 6, 3, 8, 6],
              [6, 6, 2, 1, 6, 6, 3, 3],
              [2, 2, 1, 3, 9, 6, 9, 8],
              [4, 1, 1, 6, 8, 9, 2, 4],
              [8, 9, 8, 7, 3, 4, 7, 2],
              [2, 8, 7, 8, 5, 7, 1, 7],
              [8, 3, 7, 1, 3, 4, 5, 3],
              [5, 1, 4, 7, 2, 1, 5, 4]]
    p, M = vcg(n, m, values)
    print("VCG mechanism (p,M)")
    print("p:", p)
    print("M:", M)
    """