#Will need to do this for every league so make function

def sort_public(league_teams,league):

    league_teams_spread = sorted(league_teams,key=lambda x: int(league_teams[x]['betP_spread']),reverse=True)

    league_teams_ML = sorted(league_teams,key=lambda x: int(league_teams[x]['betP_ML']),reverse=True)
    
    league_teams_over = sorted(league_teams,key=lambda x: int(league_teams[x]['over_betP']),reverse=True)

    league_teams_under = sorted(league_teams,key=lambda x: int(league_teams[x]['under_betP']),reverse=True)

    checked_teams_spread = set()
    clean_league_teams_spread = []

    for team in league_teams_spread:
        if team in checked_teams_spread:
            continue
        clean_league_teams_spread.append(team)
        checked_teams_spread.add(team)
        checked_teams_spread.add(league_teams[team]['opponent'])
    
    checked_teams_ML = set()
    clean_league_teams_ML = []

    for team in league_teams_ML:
        if team in checked_teams_ML:
            continue
        clean_league_teams_ML.append(team)
        checked_teams_ML.add(team)
        checked_teams_ML.add(league_teams[team]['opponent'])
    

    list_len = len(clean_league_teams_spread)

    pointer1 = 0
    pointer2 = 0

    sorted_ML_spread = []

    while pointer1 < list_len and pointer2 < list_len:
        if int(league_teams[clean_league_teams_spread[pointer1]]['betP_spread']) > int(league_teams[clean_league_teams_ML[pointer2]]['betP_ML']):
            sorted_ML_spread.append((clean_league_teams_spread[pointer1],'betP_spread'))
            pointer1+=1
        else:
            sorted_ML_spread.append((clean_league_teams_ML[pointer2],'betP_ML'))
            pointer2+=1

    if pointer1 < list_len:
        for team in clean_league_teams_spread[pointer1:]:
            sorted_ML_spread.append((team,'betP_spread'))

    if pointer2 < list_len:
        for team in clean_league_teams_ML[pointer2:]:
            sorted_ML_spread.append((team,'betP_ML'))

    #Clean Over under as both team and opponent only need to account for 1 

    checked_teams = set()
    clean_league_teams_over = []

    for team in league_teams_over:
        if team in checked_teams:
            continue
        clean_league_teams_over.append(team)
        checked_teams.add(team)
        checked_teams.add(league_teams[team]['opponent'])

    checked_teams_under = set()
    clean_league_teams_under = []

    for team in league_teams_under:
        if team in checked_teams_under:
            continue
        clean_league_teams_under.append(team)
        checked_teams_under.add(team)
        checked_teams_under.add(league_teams[team]['opponent'])

    pointer1 = 0
    pointer2 = 0
    sorted_over_under = []

    list_len_ou = len(clean_league_teams_over)

    while pointer1 < list_len_ou and pointer2 < list_len_ou:
        if int(league_teams[clean_league_teams_over[pointer1]]['over_betP']) >= int(league_teams[clean_league_teams_under[pointer2]]['under_betP']):
            sorted_over_under.append((clean_league_teams_over[pointer1],'over_betP'))
            pointer1+=1
        else:
            sorted_over_under.append((clean_league_teams_under[pointer2],'under_betP'))
            pointer2+=1

    if pointer1 < list_len_ou:
        for team in clean_league_teams_over[pointer1:]:
            sorted_over_under.append((team,'over_betP'))

    if pointer2 < list_len_ou:
        for team in clean_league_teams_under[pointer2:]:
            sorted_over_under.append((team,'under_betP'))

    #Combine and sort sorted_over_under and sorted_ML_spread

    pointer1 = 0
    pointer2 = 0
    
    public_league_sorted = []

    list_len_ou =len(sorted_over_under)
    list_len_spread = len(sorted_ML_spread)

    while pointer1 < list_len_spread and pointer2 < list_len_ou:
        team1,ml_spread = sorted_ML_spread[pointer1]
        team2,ou = sorted_over_under[pointer2]
        team1_percent = league_teams[team1][ml_spread]
        team2_percent = league_teams[team2][ou]

        if int(team1_percent) >= int(team2_percent):
            public_league_sorted.append((team1,ml_spread,team1_percent,league))
            pointer1+=1
        else:
            public_league_sorted.append((team2,ou,team2_percent,league))
            pointer2+=1

    if pointer1 < list_len_spread:
        for team,ml_spread in sorted_ML_spread[pointer1:]:
            public_league_sorted.append((team,ml_spread,league_teams[team][ml_spread],league))

    if pointer2 < list_len_ou:
        for team,ou in sorted_over_under[pointer2:]:
            public_league_sorted.append((team,ou,league_teams[team][ou],league))

    return public_league_sorted

def sort_sharp(league_teams,league):

    sharp_spread = sorted(league_teams,key=lambda x: int(league_teams[x]['sharp_spread']),reverse=True)

    sharp_ML = sorted(league_teams,key=lambda x: int(league_teams[x]['sharp_ML']),reverse=True)

    sharp_over = sorted(league_teams,key=lambda x: int(league_teams[x]['sharp_over']),reverse=True)

    sharp_under = sorted(league_teams,key=lambda x: int(league_teams[x]['sharp_under']),reverse=True)

    list_len = len(sharp_spread)

    pointer1 = 0
    pointer2 = 0

    sorted_ML_spread = []

    while pointer1 < list_len and pointer2 < list_len:
        if int(league_teams[sharp_spread[pointer1]]['sharp_spread']) > int(league_teams[sharp_ML[pointer2]]['sharp_ML']):
            sorted_ML_spread.append((sharp_spread[pointer1],'sharp_spread'))
            pointer1+=1
        else:
            sorted_ML_spread.append((sharp_ML[pointer2],'sharp_ML'))
            pointer2+=1

    if pointer1 < list_len:
        for team in sharp_spread[pointer1:]:
            sorted_ML_spread.append((team,'sharp_spread'))

    if pointer2 < list_len:
        for team in sharp_ML[pointer2:]:
            sorted_ML_spread.append((team,'sharp_ML'))
    
    checked_teams = set()
    clean_league_teams_over = []

    for team in sharp_over:
        if team in checked_teams:
            continue
        clean_league_teams_over.append(team)
        checked_teams.add(team)
        checked_teams.add(league_teams[team]['opponent'])

    checked_teams_under = set()
    clean_league_teams_under = []

    for team in sharp_under:
        if team in checked_teams_under:
            continue
        clean_league_teams_under.append(team)
        checked_teams_under.add(team)
        checked_teams_under.add(league_teams[team]['opponent'])
    
    pointer1 = 0
    pointer2 = 0
    sorted_over_under = []

    list_len_ou = len(clean_league_teams_over)

    while pointer1 < list_len_ou and pointer2 < list_len_ou:
        if int(league_teams[clean_league_teams_over[pointer1]]['sharp_over']) >= int(league_teams[clean_league_teams_under[pointer2]]['sharp_under']):
            sorted_over_under.append((clean_league_teams_over[pointer1],'sharp_over'))
            pointer1+=1
        else:
            sorted_over_under.append((clean_league_teams_under[pointer2],'sharp_under'))
            pointer2+=1

    if pointer1 < list_len_ou:
        for team in clean_league_teams_over[pointer1:]:
            sorted_over_under.append((team,'sharp_over'))

    if pointer2 < list_len_ou:
        for team in clean_league_teams_under[pointer2:]:
            sorted_over_under.append((team,'sharp_under'))


    pointer1 = 0
    pointer2 = 0

    sharp_league_sorted = []

    list_len_ou =len(sorted_over_under)
    list_len_spread = len(sorted_ML_spread)

    while pointer1 < list_len_spread and pointer2 < list_len_ou:
        team1,ml_spread = sorted_ML_spread[pointer1]
        team2,ou = sorted_over_under[pointer2]
        team1_percent = league_teams[team1][ml_spread]
        team2_percent = league_teams[team2][ou]

        if int(team1_percent) >= int(team2_percent):
            sharp_league_sorted.append((team1,ml_spread,team1_percent,league))
            pointer1+=1
        else:
            sharp_league_sorted.append((team2,ou,team2_percent,league))
            pointer2+=1

    if pointer1 < list_len_spread:
        for team,ml_spread in sorted_ML_spread[pointer1:]:
            sharp_league_sorted.append((team,ml_spread,league_teams[team][ml_spread],league))

    if pointer2 < list_len_ou:
        for team,ou in sorted_over_under[pointer2:]:
            sharp_league_sorted.append((team,ou,league_teams[team][ou],league))

    sharp_league_sorted = [tup for tup in sharp_league_sorted if tup[2]>0]

    return sharp_league_sorted


