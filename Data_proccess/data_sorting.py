#Data sorting file
#This file will return teams of stacks with a maximum n

#Library imports
from Data_proccess import random_groups as rg

def sort_teams(data):
    while True:
        n = 0
        for  i in range(1, len(data)):
            if data[i - 1]["score"] > data[i]["score"]:
                temp = data[i - 1]
                data[i - 1] = data[i]
                data[i] = temp
                n + 1
            
        if n == 0 : break

    return data

def create_teams(players, num_teams, n):
    # Sort the list of players by score in descending order.
    sorted_players = sort_teams(players)
    
    # Initialize teams with their members.
    teams = [[] for _ in range(num_teams)]
    i = num_teams - 1
    
    # Calculate the target average score for each team.
    total_score = sum(player['score'] for player in sorted_players)
    target_avg = total_score / num_teams
    
    # Iterate through the players and assign them to teams.
    for player in sorted_players:
        
        min_diff_team = min(teams, key=lambda team: abs(sum(member['score'] for member in team) + player['score'] - target_avg * len(team)))
        min_diff_team.append(player)

    #Correct teams, it chechs whetther a teams exceed teh disire amount of team member of if there is a member alone

    while True:
        try:
            max_arg_team = max(teams, key=lambda team: abs(sum(member["score"] for member in team) / len(team)))
        except:
            return rg.create_random_teams(players, n)
        
        if len(max_arg_team) > n:
            if len(teams[i]) >= int(n / 2):
                max_score = max(max_arg_team, key = lambda player : player["score"])
                teams[i].append(max_score)
                max_arg_team.remove(max_score)
            
            i = num_teams if i == 0 else i - 1
            continue

        i = 0
        
        for team in teams:
            if len(team) == 1:
                teams[-1].append(team[0])
                teams.pop(i)
            i += 1

        break
    
    return teams

def parse_notes(score, bounderies):
    parse_score = 0
    for bound in bounderies:
        parse_score += 1
        if score < bound[1] and score >= bound[0] :
            return parse_score
        
    return parse_score

def get_teams(data, n):
    teams = int(len(data) / n) + 1 if len(data) % n else int(len(data) / n)
    # bounderies = gb.get_team_bounderies([int(i["score"]) for i in data], n)
    for member in data:
         member["score"] = int(member["score"])

    return rg.create_teams_pos(data, n)
