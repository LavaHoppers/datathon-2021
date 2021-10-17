# import module to get population data at a location
# import module to draw updated boundaries to screen
from intersection import contains
import numpy as np
import random
import pygame
import pandas
import math
import random
from pygame.locals import * 

Colors=["#D79922","EFE2BA","F13C20","4056A1","C5CBE3"]
BG_COLOR = (234,236,238)
DRK_WHT = (248,249,249)
RED = '#48C9B0'#(231,	76,	60)
BLUE = (52,	152, 219)
GREY = (66,	73, 73)

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCALE_H = 120 * .6
SCALE_V = 160 * .6

LON_OFFSET = 92.8022 # Do not change
LAT_OFFSET = -42.5

DRAW_OFFSET_X = 100
DRAW_OFFSET_Y = -200
TEXT_X_ALIGN = SCREEN_WIDTH * .6

# Defines the regions we want to look at
# congressional dist
# state senate dist
# state house dist
REGION = 'congressional dist'

pygame.init()

pygame.font.init()
consolas = pygame.font.SysFont('Calibri', 30)


DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gerrymandering Evaluator")
DISPLAY.fill(BG_COLOR)

def display_str(text, x, y):
    text_img = consolas.render(text, True, GREY, BG_COLOR)
    DISPLAY.blit(text_img, (x, y))

def display_districts(x, y, w, h, total_districts, red_districts):
    gap = 4
    indiv_w = (w - gap * (total_districts - 1)) / total_districts
    for i in range(total_districts):
        if i < red_districts:
            pygame.draw.rect(DISPLAY, RED, pygame.Rect(x + i * (indiv_w + gap), y, indiv_w, h), border_radius=7)
        else:
            pygame.draw.rect(DISPLAY, BLUE, pygame.Rect(x + i * (indiv_w + gap), y, indiv_w, h), border_radius=7)



df = pandas.read_csv("data/votes.csv")
flipables = set()

districts = list(set(df[REGION]))

NUM_DISTRICTS = len(districts)

zip_dict = dict()
zips_in_districts = dict()

for _, row in df.iterrows():
    zip_dict[row['zip']] = row
    if row[REGION] not in zips_in_districts:
        zips_in_districts[row[REGION]] = list()
    zips_in_districts[row[REGION]].append(row)

dis_color = dict()
for distric in districts:
    
    dis_color[distric] = (Colors[random.randint(0,len(Colors))])

pygame.draw.rect(DISPLAY, DRK_WHT, pygame.Rect(SCREEN_WIDTH / 20, SCREEN_HEIGHT / 20, SCREEN_WIDTH * .5, SCREEN_HEIGHT * .9), border_radius=18)


for _, row in df.iterrows():
    lon = (row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X
    lat = SCREEN_HEIGHT - (row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y
    size = 3 if math.log(row['population']) < 3 else math.log(row['population'])

    # dis_color[row[REGION]]
    # (row['rep'] / row['votes_count'] * 255, 0, row['dem'] / row['votes_count'] * 255)
    pygame.draw.circle(DISPLAY, dis_color[row[REGION]], (lon, lat), size)

ACCEL_MAX_DIST = 25   
accel_struct = list()
for _ in range(0, SCREEN_WIDTH, ACCEL_MAX_DIST):
    accel_struct.append(list())

for item in accel_struct:
    for _ in range(0, SCREEN_HEIGHT, ACCEL_MAX_DIST):
        item.append(list())

for _, row in df.iterrows():
    x = (row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X 
    y = SCREEN_HEIGHT - (row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y  
    x = int(x) // ACCEL_MAX_DIST
    y = int(y) // ACCEL_MAX_DIST
    accel_struct[x][y].append(row)

def count_rep_districts():
    r_value = 0
    for district in zips_in_districts.keys():
        total_voters = 0
        total_rep_votes = 0
        for zip_code in zips_in_districts[district]:
            total_voters += zip_code['votes_count']
            total_rep_votes += zip_code['rep']
        r_value += 1 if total_rep_votes / total_voters > .5 else 0
    return r_value

display_districts(SCREEN_WIDTH * .07, SCREEN_HEIGHT * .80, SCREEN_WIDTH * .46, 90, len(zips_in_districts.keys()), count_rep_districts())

def get_overall_rep():
    total_voters = 0
    total_rep_votes = 0
    for district in zips_in_districts.keys():
        for zip_code in zips_in_districts[district]:
            total_voters += zip_code['votes_count']
            total_rep_votes += zip_code['rep']
    return total_rep_votes / total_voters


display_str('Gerrymander score: {}%'.format(get_overall_rep()), TEXT_X_ALIGN, 40)

for y in range(0, SCREEN_HEIGHT):
    for x in range(0, SCREEN_WIDTH):

        #### INSERTED PYGAME CODE ###
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        possible_closest = list()
        X = int(x) // ACCEL_MAX_DIST
        Y = int(y) // ACCEL_MAX_DIST
        possible_closest = possible_closest + accel_struct[X][Y]
        if not X - 1 < 0:
            possible_closest = possible_closest + accel_struct[X-1][Y]
            if not Y - 1 < 0:
                possible_closest = possible_closest + accel_struct[X][Y - 1]
                possible_closest = possible_closest + accel_struct[X - 1][Y - 1]
                if not len(possible_closest) <= X + 1:
                    possible_closest = possible_closest + accel_struct[X + 1][Y - 1]
        if not len(possible_closest) <= X + 1:
            possible_closest = possible_closest + accel_struct[X+1][Y]
            if not len(possible_closest[0]) <= Y + 1:
                possible_closest = possible_closest + accel_struct[X][Y + 1]
                possible_closest = possible_closest + accel_struct[X + 1][Y + 1]
                if not X - 1 < 0:
                    possible_closest = possible_closest + accel_struct[X - 1][Y + 1]

        if 0 < len(possible_closest):

            pt = (x, y)
            closest_row = None
            closest_dist = None
            second_closest_row = None
            second_closest_dist = None

            for row in possible_closest:

                test_pt = ((row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X, SCREEN_HEIGHT - (row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y)

                this_distance = math.sqrt((pt[0] - test_pt[0]) * (pt[0] - test_pt[0]) + (pt[1] - test_pt[1]) * (pt[1] - test_pt[1]))

                if closest_row is None or this_distance < closest_dist:
                    second_closest_row = closest_row
                    second_closest_dist = closest_dist
                    closest_dist = this_distance
                    closest_row = row
                elif second_closest_row is None or this_distance < second_closest_dist:
                    second_closest_dist = this_distance
                    second_closest_row = row

            #if closest_dist < ACCEL_MAX_DIST:
            DISPLAY.set_at(pt, dis_color[closest_row[REGION]])

            if not second_closest_row is None and (not second_closest_row[REGION] == closest_row[REGION]):
                flipables.add((second_closest_row['zip'], closest_row[REGION]))
                flipables.add((closest_row['zip'], second_closest_row[REGION]))

                # lon = (closest_row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X
                # lat = SCREEN_HEIGHT - (closest_row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y
                # size = 3 if math.log(closest_row['population']) < 3 else math.log(closest_row['population'])
                # pygame.draw.circle(DISPLAY, (255,0,0), (lon, lat), size)

                # lon = (second_closest_row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X
                # lat = SCREEN_HEIGHT - (second_closest_row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y
                # size = 3 if math.log(second_closest_row['population']) < 3 else math.log(second_closest_row['population'])
                # pygame.draw.circle(DISPLAY, (255,0,0), (lon, lat), size)

    pygame.display.update()
    


def flip_district(zipp, district):


    row = zip_dict[zipp]
    x = (row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X
    y = SCREEN_HEIGHT - (row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y
    X = int(x) // ACCEL_MAX_DIST
    Y = int(y) // ACCEL_MAX_DIST

    pygame.draw.circle(DISPLAY, (255, 255, 255), (x, y), 5)
    pygame.display.update()

    sheesh = list()

    for entry in accel_struct[X][Y]:
        sheesh.append(entry)
    if not X - 1 < 0:
        for entry in accel_struct[X-1][Y]:
            sheesh.append(entry)
            
        if not Y - 1 < 0:
            for entry in accel_struct[X][Y-1]:
                sheesh.append(entry)
                
            for entry in accel_struct[X-1][Y-1]:
                sheesh.append(entry)

            if not SCREEN_WIDTH // ACCEL_MAX_DIST <= X + 1:
                for entry in accel_struct[X+1][Y-1]:
                    sheesh.append(entry)

    if not SCREEN_WIDTH // ACCEL_MAX_DIST  <= X + 1:
        for entry in accel_struct[X+1][Y]:
            sheesh.append(entry)

        if not SCREEN_HEIGHT // ACCEL_MAX_DIST  <= Y + 1:
            for entry in accel_struct[X][Y+1]:
                sheesh.append(entry)

            for entry in accel_struct[X+1][Y+1]:
                sheesh.append(entry)

            if not X - 1 < 0:
                for entry in accel_struct[X-1][Y+1]:
                    sheesh.append(entry)

    removing = list()
    for entry in sheesh:                
        for pair in flipables:
            if pair[0] == entry['zip']:
                removing.append(pair)
    for item in removing:
        flipables.remove(item)

    possible_closest = sheesh


    for i in range(len(zips_in_districts[row[REGION]])-1):
        if len(zips_in_districts[row[REGION]]) == 0:
            break
        if zips_in_districts[row[REGION]][i]['zip'] == row['zip']:
            zips_in_districts[row[REGION]].pop(i)
    row[REGION] = district
    zips_in_districts[district].append(row)

    for y_ in range((Y-1)*ACCEL_MAX_DIST,(Y+2)*ACCEL_MAX_DIST):
        for x_ in range((X-1)*ACCEL_MAX_DIST,(X+2)*ACCEL_MAX_DIST):

            pt = (x_, y_)
            closest_row = None
            closest_dist = None
            second_closest_row = None
            second_closest_dist = None

            for row in possible_closest:

                test_pt = ((row['lon'] + LON_OFFSET) * SCALE_H + DRAW_OFFSET_X, SCREEN_HEIGHT - (row['lat'] + LAT_OFFSET) * SCALE_V + DRAW_OFFSET_Y)

                this_distance = math.sqrt((pt[0] - test_pt[0]) * (pt[0] - test_pt[0]) + (pt[1] - test_pt[1]) * (pt[1] - test_pt[1]))

                if closest_row is None or this_distance < closest_dist:
                    second_closest_row = closest_row
                    second_closest_dist = closest_dist
                    closest_dist = this_distance
                    closest_row = row
                elif second_closest_row is None or this_distance < second_closest_dist:
                    second_closest_dist = this_distance
                    second_closest_row = row

            #if closest_dist < ACCEL_MAX_DIST:
            DISPLAY.set_at(pt, dis_color[closest_row[REGION]])

            if not second_closest_row is None and (not second_closest_row[REGION] == closest_row[REGION]):
                flipables.add((second_closest_row['zip'], closest_row[REGION]))
                flipables.add((closest_row['zip'], second_closest_row[REGION]))


# updates county boundaries to maximize fairness
def fit_boundaries(percentPartyA, partySwitchScore, maxEpochs, temperature):
    
    ''' use simulated annealing to increase fairness in boundary drawings
    
    Args:
        percentPartyA (float): percent of people in party A
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
        numDistrictsForA = np.floor(NUM_DISTRICTS * percentPartyA)
    else:
        numDistrictsForA = np.ceil(NUM_DISTRICTS * percentPartyA)
    
    print("percent A: ", percentPartyA)
    print("want ", numDistrictsForA, " A districts and ", NUM_DISTRICTS - numDistrictsForA, " B districts")
    print()
   
    ################ calculate party percentage within each boundary ################
    # get oldAByDistrict
    oldAByDistrict = list()  # percent of population in a boundary voting for A

    # for each 
    for key in zips_in_districts.keys():  # for each district
        votesPartyA = 0.0
        totalVotes = 0.0
        for element in zips_in_districts[key]:  # for each zip code in district
            votesPartyA += element['dem']
            totalVotes += element['votes_count']
        oldAByDistrict.append(votesPartyA / totalVotes)
    oldAByDistrict.sort(reverse=True)  # put counties w/ highest percent A at top
    
    #print("initial sorted districts by A", oldAByDistrict)
    print()
    
    ############################## simulated annealing ##############################
    for epoch in range(maxEpochs):

        #### INSERTED PYGAME CODE ###
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        
        print("epoch: ", epoch)
   
        ########## pick boundary point and move ##########
        originalRegion = ''
        while True:
            flippedZip = random.choice(list(flipables))
            # cant flip a zipcode that is the only zipcode of a region
            if len(zips_in_districts[zip_dict[flippedZip[0]][REGION]]) == 1:
                flipables.remove(flippedZip)
            # this point is flippable
            else:
                originalRegion = zip_dict[flippedZip[0]][REGION]
                break
        
        flip_district(flippedZip[0], flippedZip[1])  # updates district assignment and flippable set
        
        ########## re calculate boundary percentages ##########
        newAByDistrict = list()
        for key in zips_in_districts.keys():  # for each district
            votesPartyA = 0.0
            totalVotes = 0.0
            for element in zips_in_districts[key]:  # for each zip code in district
                votesPartyA += element['dem']
                totalVotes += element['votes_count']
            newAByDistrict.append(votesPartyA / totalVotes)
        newAByDistrict.sort(reverse=True)  # put counties w/ highest percent A at top
        
        #print("\t new district percentages: ", newAByDistrict)
        print("\t change:",end = " ")
        for i in range(len(oldAByDistrict)):
            print("{:.2f}".format(newAByDistrict[i]-oldAByDistrict[i]),end = " ")
        print()

        ########## calculate change in representation ##########
        totalChange = 0  # total change in representation
        districtChange = 0  # change in representation in one district
        # loop thru each district, sum scores
        for i in range(NUM_DISTRICTS):
            
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
        #print("\t old: ", oldAByDistrict)
        #print("\t new: ", newAByDistrict)
  
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
            flip_district(flippedZip[0], originalRegion)

    # function done
    return 0


fit_boundaries(1 - get_overall_rep(), 2, 100, .001)


# while True:
    
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
   