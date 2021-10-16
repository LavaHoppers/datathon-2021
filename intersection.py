def contains(point, nodes, edges):
    rx, ry = point
    # ray eqation = 
    for edge in edges:
        

def main():

    test_pt = (0, 0)
    test_nodes = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    test_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

    if (contains(test_pt, test_nodes, test_edges)):
        print("Test Passed")
    else:
        print("Test Failed")



main()