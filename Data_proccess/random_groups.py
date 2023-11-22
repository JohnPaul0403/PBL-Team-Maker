#This file is to create teams tottaly random
#Without any parameters in case the semester just started and student have no scoere yet

#Library imports
from Data_proccess import groups_bounderies as gb
import random as rd

#This function checks if all scores are the same in the given, case it is, that should mean that student haven't been graded or student almost have the same scores
def scores_same(data):

    #Variable declaration
    scores = [int(i["score"]) for i in data]
    average = gb.average_nums(scores)

    #Return value
    return max(scores) == average or max(scores) - 10 < min(scores)

#In case there is no score bounderies or minimum changes, it will just create random groups
def create_random_teams(data, n):

    #Variable declaration
    step = int(len(data) / n)
    team_list = list(range(1, step + 1))
    teams = []

    #shuffle data inside the list
    rd.shuffle(data)

    #Arrange data by teams
    teams.extend(data[i - 1::step] for i in team_list)
    return teams

def create_teams_pos(data, n):
    teams = create_random_teams(data, n)
    averages = [int(sum(i["score"] for i in members) / len(members)) for members in teams]

    if max(averages) - 10 <= min(averages):
        return teams, averages
    else:
        return create_teams_pos(data, n)

