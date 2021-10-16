
def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def contains(point, nodes, edges):
    '''
    https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    '''
    total = 0
    p = point
    r = [3.14648, 800.7436] # arbitrary
    for edge in edges:
        q = nodes[edge[0]] 
        s = sub(nodes[edge[1]], q)

        t = cross(sub(q, p), s) / cross(r, s)
        u = cross(sub(p, q), r) / cross(s, r)

        if 0 <= t and t <= 1 and 0 <= u and u <= 1:
            total = total + 1
        
    return total % 2 == 1

# import random
# def main():
#     test_nodes = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
#     test_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
#     for _ in range(100):
#         if (contains([random.random(), random.random()], test_nodes, test_edges)):
#             pass
#         else:
#             print("Test Failed")
# main()