def sort_total(nba_sorted,nhl_sorted,ncaambb_sorted,ncaafb_sorted,t_count):
    pointer1 = 0
    pointer2 = 0

    sorted_nba_nhl = []

    while pointer1 < len(nba_sorted) and pointer2 < len(nhl_sorted):
        team1,spread_ou1,percent1,league1 = nba_sorted[pointer1]
        team2,spread_ou2,percent2,league2 = nhl_sorted[pointer2]

        if percent1 >= percent2:
            sorted_nba_nhl.append((team1,spread_ou1,percent1,league1))
            pointer1+=1
        else:
            sorted_nba_nhl.append((team2,spread_ou2,percent2,league2))
            pointer2+=1


    if pointer1 < len(nba_sorted):
        for team,spread_ou,percent,league in nba_sorted[pointer1:]:
            sorted_nba_nhl.append((team,spread_ou,percent,league))

    if pointer2 < len(nhl_sorted):
        for team,spread_ou,percent,league in nhl_sorted[pointer2:]:
            sorted_nba_nhl.append((team,spread_ou,percent,league))


    pointer1 = 0
    pointer2 = 0

    sorted_ncaa = []

    while pointer1 < len(ncaambb_sorted) and pointer2 < len(ncaafb_sorted):
        team1,spread_ou1,percent1,league1 = ncaambb_sorted[pointer1]
        team2,spread_ou2,percent2,league2 = ncaafb_sorted[pointer2]

        if percent1 >= percent2:
            sorted_ncaa.append((team1,spread_ou1,percent1,league1))
            pointer1+=1
        else:
            sorted_ncaa.append((team2,spread_ou2,percent2,league2))
            pointer2+=1


    if pointer1 < len(ncaambb_sorted):
        for team,spread_ou,percent,league in ncaambb_sorted[pointer1:]:
            sorted_ncaa.append((team,spread_ou,percent,league))

    if pointer2 < len(ncaafb_sorted):
        for team,spread_ou,percent,league in ncaafb_sorted[pointer2:]:
            sorted_ncaa.append((team,spread_ou,percent,league))


    #SORT TOTAL UP TO 5 
    count = 0
    pointer1 = 0
    pointer2 = 0

    sorted_total = []


    while pointer1 < len(sorted_nba_nhl) and pointer2 < len(sorted_ncaa) and count < t_count:
        team1,spread_ou1,percent1,league1 = sorted_nba_nhl[pointer1]
        team2,spread_ou2,percent2,league2 = sorted_ncaa[pointer2]

        if int(percent1) >= int(percent2):
            sorted_total.append((team1,spread_ou1,percent1,league1))
            pointer1+=1
            count+=1
        else:
            sorted_total.append((team2,spread_ou2,percent2,league2))
            pointer2+=1
            count+=1

    if pointer2 < len(sorted_ncaa) and count < t_count:
        for team,spread_ou,percent,league in sorted_ncaa[pointer2:]:
            if count>5:
                break
            sorted_total.append((team,spread_ou,percent,league))
            count+=1

    if pointer1 < len(sorted_nba_nhl) and count < t_count:
        for team,spread_ou,percent,league in sorted_nba_nhl[pointer1:]:
            if count > 5:
                break
            sorted_total.append((team,spread_ou,percent,league))
            count+=1

    return sorted_total