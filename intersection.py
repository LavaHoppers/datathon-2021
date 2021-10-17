

def sub(a, b):
    return [a[0] - b[0], a[1] - b[1]]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def contains(x, y, nodes, edges):
    '''
    https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    '''
    total = 0
    p = [x, y]
    r = [3.14648, 800.7436]  # arbitrary
    for edge in edges:
        q = nodes[edge[0]] 
        s = sub(nodes[edge[1]], q)

        t = cross(sub(q, p), s) / cross(r, s)
        u = cross(sub(p, q), r) / cross(s, r)

        if 0 <= t and t <= 1 and 0 <= u and u <= 1:
            total = total + 1
        
    return total % 2 == 1
