# import module to get population data at a location
# import module to draw updated boundaries to screen
from intersection import contains
import numpy as np
import random

import matplotlib.pyplot as plt


# updates county boundaries to maximize fairness
def fit_boundaries(percentPartyA, peopleDots, boundaryPoints, boundaryEdges, partySwitchScore, maxEpochs, temperature, moveDist):
    
    ''' use simulated annealing to increase fairness in boundary drawings
    
    Args:
        percentPartyA (float): percent of people in party A
        peopleDots (list of tupples): data to represent people at a location
        boundaryPoints (list of lists): points to define boundary location: each has x,y
        boundaryEdges (list of list of tupples): define edges that define boundaries
        
        partySwitchScore (float): multiplier for party switching
        maxEpochs (int): max number of epochs
        temperature (float): starting temperature for annealing process
        moveDist (float): move distance for moving boundary points
    
    Returns:
        boundaryPoints (updated from original)
           
    '''

    ############### find num districts that should vote for each party ##############
    numDistrictsForA = 0  # optimal # counties for party A
    if percentPartyA > 1:
        percentPartyA /= 100
    if percentPartyA > 0.5:
        numDistrictsForA = np.floor(len(boundaryEdges) * percentPartyA)
    else:
        numDistrictsForA = np.ceil(len(boundaryEdges) * percentPartyA)
    
    print("percent A: ", percentPartyA)
    print("num districts A: ", numDistrictsForA, "num districts B: ", len(boundaryEdges) - numDistrictsForA)
   
    ################ calculate party percentage within each boundary ################
    # calculate party percentage in each boundary
    oldAByDistrict = list()  # percent of population in a boundary voting for A
    for i in range(len(boundaryEdges)):  # for each boundary
        votesPartyA = 0.0
        totalVotes = 0.0
        for j in range(len(peopleDots)):  # count total votes, votes for party A
            if contains(peopleDots[j][0], peopleDots[j][1], boundaryPoints, boundaryEdges[i]):
                totalVotes += peopleDots[j][3]
                votesPartyA += peopleDots[j][2]
        oldAByDistrict.append(votesPartyA / totalVotes)
    oldAByDistrict.sort(reverse=True)  # put counties w/ highest percent A at top
    
    print("initial sorted districts by A", oldAByDistrict)
    print()
    
    ############################## simulated annealing ##############################
    for epoch in range(maxEpochs):
        
        print("epoch: ", epoch)
   
        ########## pick boundary point and move ##########
        # pick boundary point
        movedPoint = np.random.randint(0, len(boundaryPoints))
        originalPoint = boundaryPoints[movedPoint].copy()
        
        # move point slightly
        moveVec = np.random.multivariate_normal([0, 0], [[moveDist, 0], [0, moveDist]])
        newPoint = [originalPoint[0] + moveVec[0], originalPoint[1] + moveVec[1]]
        
        print("\t moved point #", movedPoint, " = ", originalPoint, " to: ", newPoint[0], ", ", newPoint[1])
         
        # check if move is valid
        # TODO
        # move point
        boundaryPoints[movedPoint] = newPoint.copy()
        
        ########## re calculate boundary percentages ##########
        newAByDistrict = list()
        # TODO: update % of a party within each boundary (but faster)
        for i in range(len(boundaryEdges)):  # for each boundary
            votesPartyA = 0.0
            totalVotes = 0.0
            for j in range(len(peopleDots)):  # count total votes, votes for party A
                if contains(peopleDots[j][0], peopleDots[j][1], boundaryPoints, boundaryEdges[i]):
                    totalVotes += peopleDots[j][3]
                    votesPartyA += peopleDots[j][2]
            newAByDistrict.append(votesPartyA / totalVotes)
        # END TODO:
        newAByDistrict.sort(reverse=True)
        
        print("\t new district percentages: ", newAByDistrict)

        ########## calculate change in representation ##########
        totalChange = 0  # total change in representation
        districtChange = 0  # change in representation in one district
        # loop thru each district, sum scores
        for i in range(len(boundaryEdges)):
            
            # reset district change
            districtChange = 0
            
            # if district i should vote for party A
            if i < numDistrictsForA:
                # if parties switched
                if (oldAByDistrict[i] <= 0.5 and newAByDistrict[i] >= 0.5) or (newAByDistrict[i] <= 0.5 and oldAByDistrict[i] >= 0.5):
                    districtChange = partySwitchScore * (newAByDistrict[i] - oldAByDistrict[i])
                # parties did not switch
                else:
                    # if party is incorrect
                    if newAByDistrict[i] < 0.5:
                        districtChange = newAByDistrict[i] - oldAByDistrict[i]
                
            # county should not vote for party A
            else:
                # if parties switched
                if (oldAByDistrict[i] <= 0.5 and newAByDistrict[i] >= 0.5) or (newAByDistrict[i] <= 0.5 and oldAByDistrict[i] >= 0.5):
                    districtChange = partySwitchScore * (oldAByDistrict[i] - newAByDistrict[i])
                # parties did not switch
                else:
                    # if party is incorrect
                    if newAByDistrict[i] >= 0.5:
                        districtChange = oldAByDistrict[i] - newAByDistrict[i];
                    
            # add county change to total change
            totalChange += districtChange
            
        print("\t change in fairness: ", totalChange)
        print("old: ", oldAByDistrict)
        print("new: ", newAByDistrict)
  
        ########## choose to accept or reject move ##########
        # if overall change was beneficial, accept
        accept = False;
        if totalChange >= 0:
            accept = True
        elif random.random() < np.exp(totalChange / (temperature / np.sqrt(1.0 + epoch))):
            accept = True
            
        totalChange = 0
            
        ########## accept or reject move ##########
        if accept == True:
            print("\t accept!!!")
            oldAByDistrict = newAByDistrict.copy()
        else:
            print("\t reject")
            boundaryPoints[movedPoint] = originalPoint.copy()

    # function done
    return 0

