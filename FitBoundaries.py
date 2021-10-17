# import module to get population data at a location
# import module to draw updated boundaries to screen
from intersection import contains
import numpy as np
import random


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
    print("want ", numDistrictsForA, " A districts and ", len(boundaryEdges) - numDistrictsForA, " B districts")
    print()
   
    ################ calculate party percentage within each boundary ################
    # get oldAByDistrict
    oldAByDistrict = list()  # percent of population in a boundary voting for A
    districtAssignment = dict()
    flippableSet = set()
    districtAssignment, flippableSet = initialize()
    
    # for each 
    for key in districtAssignment:  # for each district
        votesPartyA = 0.0
        totalVotes = 0.0
        for i in len(districtAssignment[key]):  # for each zip code in district
            votesPartyA += zip_dict[districtAssignment[key][i]][2]
            totalVotes += zip_dict[districtAssignment[key][i]][3]
        oldAByDistrict.append(votesPartyA / totalVotes)
    oldAByDistrict.sort(reverse=True)  # put counties w/ highest percent A at top
    
    print("initial sorted districts by A", oldAByDistrict)
    print()
    
    ############################## simulated annealing ##############################
    for epoch in range(maxEpochs):
        
        print("epoch: ", epoch)
   
        ########## pick boundary point and move ##########
        while True:
            flippedZip = random.sample(list(flippableSet))
            # cant flip a zipcode that is the only zipcode of a region
            if len(zips_in_districts[zip_dict[flippedZip[0]][REGION]]) == 1:
                flippableSet.remove(flippedZip)
            # this point is flippable
            else:
                break
            
        update(flippedZip)  # updates district assignment and flippable set
        
        ########## re calculate boundary percentages ##########
        newAByDistrict.sort()
        for key in districtAssignment:  # for each district
            votesPartyA = 0.0
            totalVotes = 0.0
            for i in len(districtAssignment[key]):  # for each zip code in district
                votesPartyA += zip_dict[districtAssignment[key][i]][2]
                totalVotes += zip_dict[districtAssignment[key][i]][3]
                newAByDistrict.append(votesPartyA / totalVotes)
        newAByDistrict.sort(reverse=True)  # put counties w/ highest percent A at top
        
        print("\t new district percentages: ", newAByDistrict)

        ########## calculate change in representation ##########
        totalChange = 0  # total change in representation
        districtChange = 0  # change in representation in one district
        # loop thru each district, sum scores
        for i in range(len(boundaryEdges)):
            
            # reset district change
            districtChange = 0
            
            # if parties switched
            if (oldAByDistrict[i] <= 0.5 and newAByDistrict[i] >= 0.5) or (newAByDistrict[i] <= 0.5 and oldAByDistrict[i] >= 0.5):
                districtChange = partySwitchScore * (newAByDistrict[i] - oldAByDistrict[i])
            # parties did not switch and if party is incorrect
            elif newAByDistrict[i] < 0.5:
                    districtChange = newAByDistrict[i] - oldAByDistrict[i]
                    
            # if party B was supposed to win    
            if i < numDistrictsForA:
                districtChange *= -1.0
                    
            # add county change to total change
            totalChange += districtChange
         
        # done finding change in representation   
        print("\t change in fairness: ", totalChange)
        print("\t old: ", oldAByDistrict)
        print("\t new: ", newAByDistrict)
  
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

