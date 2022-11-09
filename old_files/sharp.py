from scrape_nba import nba_teams,sharp_nba_sorted
from scrape_nhl import nhl_teams,sharp_nhl_sorted
#from scrape_nfl import nfl_teams
from scrape_ncaafb import ncaafb_teams,sharp_ncaafb_sorted
from scrape_ncaambb import ncaambb_teams, sharp_ncaambb_sorted

pointer1 = 0
pointer2 = 0

sorted_nba_nhl = []

while pointer1 < len(sharp_nba_sorted) and pointer2 < len(sharp_nhl_sorted):
    team1,spread_ou1,percent1,league1 = sharp_nba_sorted[pointer1]
    team2,spread_ou2,percent2,league2 = sharp_nhl_sorted[pointer2]

    if percent1 >= percent2:
        sorted_nba_nhl.append((team1,spread_ou1,percent1,league1))
        pointer1+=1
    else:
        sorted_nba_nhl.append((team2,spread_ou2,percent2,league2))
        pointer2+=1


if pointer1 < len(sharp_nba_sorted):
    for team,spread_ou,percent,league in sharp_nba_sorted[pointer1:]:
        sorted_nba_nhl.append((team,spread_ou,percent,league))

if pointer2 < len(sharp_nhl_sorted):
    for team,spread_ou,percent,league in sharp_nhl_sorted[pointer2:]:
        sorted_nba_nhl.append((team,spread_ou,percent,league))


pointer1 = 0
pointer2 = 0

sorted_ncaa = []

while pointer1 < len(sharp_ncaambb_sorted) and pointer2 < len(sharp_ncaafb_sorted):
    team1,spread_ou1,percent1,league1 = sharp_ncaambb_sorted[pointer1]
    team2,spread_ou2,percent2,league2 = sharp_ncaafb_sorted[pointer2]

    if percent1 >= percent2:
        sorted_ncaa.append((team1,spread_ou1,percent1,league1))
        pointer1+=1
    else:
        sorted_ncaa.append((team2,spread_ou2,percent2,league2))
        pointer2+=1


if pointer1 < len(sharp_ncaambb_sorted):
    for team,spread_ou,percent,league in sharp_ncaambb_sorted[pointer1:]:
        sorted_ncaa.append((team,spread_ou,percent,league))

if pointer2 < len(sharp_ncaafb_sorted):
    for team,spread_ou,percent,league in sharp_ncaafb_sorted[pointer2:]:
        sorted_ncaa.append((team,spread_ou,percent,league))


#SORT TOTAL UP TO 5 
count = 0
pointer1 = 0
pointer2 = 0

sorted_total = []


while pointer1 < len(sorted_nba_nhl) and pointer2 < len(sorted_ncaa) and count < 3:
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

if pointer2 < len(sorted_ncaa) and count < 3:
    for team,spread_ou,percent,league in sorted_ncaa[pointer2:]:
        if count>4:
            break
        sorted_total.append((team,spread_ou,percent,league))
        count+=1

if pointer1 < len(sorted_nba_nhl) and count < 3:
    for team,spread_ou,percent,league in sorted_nba_nhl[pointer1:]:
        if count > 4:
            break
        sorted_total.append((team,spread_ou,percent,league))
        count+=1

#11AM weekends 6PM weekdays

t_text = "Top Money Difference of the Day:\n"

for team,bet,percent,league in sorted_total:

    if bet == "sharp_ML":
        t_line = f"#{team} ML ({eval(league)[team]['ML']}) is getting {eval(league)[team]['betP_ML']}% of wagers and {eval(league)[team]['handle_ML']}% of the money. \n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({eval(league)[team]['spread']}) is getting {eval(league)[team]['betP_spread']}% of wagers {eval(league)[team]['handle_spread']}% of the money. \n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({eval(league)[team]['over_under']}) is getting {eval(league)[team]['over_betP']}% of wagers {eval(league)[team]['over_handle']}% of the money. \n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({eval(league)[team]['over_under']}) is getting {eval(league)[team]['under_betP']}% of wagers {eval(league)[team]['under_handle']}% of the money. \n"
    t_text+= t_line

t_text+="#GamblingTwitter"
print(t_text)
