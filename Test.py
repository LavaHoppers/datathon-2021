'''
Created on Oct 16, 2021

@author: Jeremy Parker Yang
'''

from FitBoundaries import *

percentPartyA = 50.0

peopleDots = [(0.3, 0.3, 1, 1), (0.3, 0.5, 1, 1), (0.5, 0.5, 1, 1), (4.9, 4.9, 0, 4), (4.9, 0.3, 0, 3), (1.05, 1.05, 10, 10), (1.05, 1.1, 1, 1), (1.1, 1.1, 1, 1)]

boundaryPoints = [[0.0, 0.0], [0.0, 5.0], [5.0, 5.0], [5.0, 0.0], [1.0, 1.0]]
boundaryEdges = [[(0, 1), (1, 4), (4, 3), (3, 0)], [(1, 2), (2, 3), (3, 4), (4, 1)]]

partySwitchScore = 2
maxEpochs = 10
temperature = 65
moveDist = 0.5

print("run fit_boundaries")
fit_boundaries(percentPartyA, peopleDots, boundaryPoints, boundaryEdges, partySwitchScore, maxEpochs, temperature, moveDist)
