#This file is to create teams tottaly random
#Without any parameters in case the semester just started and student have no scoere yet

#Library imports
import random as rd

#Average function
average_nums = lambda x : round(sum(x) / len(x), 2)

#This function checks if all scores are the same in the given, case it is, that should mean that student haven't been graded or student almost have the same scores
def scores_same(data):

    #Variable declaration
    scores = [int(i["score"]) for i in data]
    average = average_nums(scores)

    #Return value
    return max(scores) == average or max(scores) - 10 < min(scores)

#In case there is no score bounderies or minimum changes, it will just create random groups
def create_random_teams(data, n):
    """
    Creates random teams from given data.

    Args:
        data: The data used to create teams.
        n: The number of members per group to create.

    Returns:
        List: The randomly created teams.

    Examples:
        # Create random teams of 4 from data
        teams = create_random_teams(data, 4)
    """

    #Variable declaration
    step = int(len(data) / n)
    team_list = list(range(1, step + 1))
    teams = []

    #shuffle data inside the list
    rd.shuffle(data)

    #Arrange data by teams
    teams.extend(data[i - 1::step] for i in team_list)
    return teams

def get_all_arragements(data):
    """
    Gets all possible arrangements of members in a group.

    Args:
        data: The data used to create teams.

    Returns:
        List: All possible arrangements of members in a group.

    Examples:
        # Get all possible arrangements of members in a group
        arrangements = get_all_arragements(data)
    """
    return permutations(data)

def get_team_template(data, n):
    #Variable declaration
    step = int(len(data) / n)
    team_list = list(range(1, step + 1))
    teams = []

    #Arrange data by teams
    teams.extend(data[i - 1::step] for i in team_list)
    return teams

def create_teams(optimaze, n, data):
    """
    Create teams based on optimization criteria.

    Args:
        optimaze (int): The optimization threshold.
        n (int): The number of teams to create.
        data (list): The data used for team creation.

    Returns:
        list: The created teams that satisfy the optimization criteria.
    """
    r_teams = create_random_teams(data, n)
    r_average = [int(sum(i["score"] for i in members) / len(members)) for members in r_teams]
    r_optimaze = max(r_average) - min(r_average)
    print(optimaze, r_optimaze)
    i = 0

    for _ in range(1000):
        if r_optimaze < optimaze:
            break
        r_teams = create_random_teams(data, n)
        r_average = [int(sum(i["score"] for i in members) / len(members)) for members in r_teams]
        r_optimaze = max(r_average) - min(r_average)
        i += 1

    return r_teams

def get_score(teams):
    return [sum(i["score"] for i in members) // len(members) for members in teams]

def create_teams_pos(data, n):
    """
    Creates teams from given data and optimizes the team composition based on the average scores of the members.

    Args:
        data: The data used to create teams.
        n: The number of teams to create.

    Returns:
        Tuple: The optimized teams and their average scores.

    Examples:
        # Create teams of 4 from data
        teams, averages = create_teams_pos(data, 4)
    """

    #Variable declaration
    for member in data:
        member["score"]  = int(member["score"])
    iters = 100
    teams: list
    averages: list
    optimize = 100

    #Loop
    for _ in range(iters):
        new_teams = create_teams(optimize, n, data)
        new_averages = [sum(i["score"] for i in members) // len(members) for members in new_teams]
        new_optimze = max(new_averages) - min(new_averages)
        if new_optimze == 0:
            teams = new_teams
            averages = new_averages
            break
        if new_optimze < optimize:
            optimize = new_optimze
            teams = new_teams
            averages = new_averages
    return teams, averages

