#This file is for getting the group average and making n bounderies

#Average function
average_nums = lambda x : round(sum(x) / len(x), 2)

#Bounderies function
def get_team_bounderies(scores, n):

    #Variables declaration
    bounderies = []
    min_num = min(scores)
    max_num = max(scores)
    temp = min_num

    step = [int((max_num - min_num) / n) for _ in range(n)]

    for i in step:
        bounderies.append((temp, temp + i))
        temp += i

    return bounderies

#Team limit
def get_teams_limit(members_num, n):

    #Variable declaration
    teams_number = int(members_num / n) if members_num % n == 0 else int(members_num / n) + 1
    limits_mode = members_num % n
    limits = []

    #Teams setting
    for i in range(teams_number) :
        if i == teams_number - 1:
            limits.append(limits_mode)
            continue
        limits.append(n)

    #Last team organization
    if limits[-1] == 0:
        limits[-1] = n
    elif limits[-1] == 1:
        limits[-1] += 1
        limits[-2] -= 1

    return limits
