from bs4 import BeautifulSoup
from datetime import date
import calendar,re,requests,tweepy,config
from curses.ascii import isdigit
from helper import sort_public,sort_sharp
from twitter import getClient

curr_date = date.today()
curr_day = (calendar.day_name[curr_date.weekday()])



def split_percent(num):
    #100% case
    if isdigit(metrics[num].text[2]):
        team1 = metrics[num].text[:3]
        team2 = metrics[num].text[4:-1]

    #double digit case
    if isdigit(metrics[num].text[1]):
        team1 = metrics[num].text[:2]
        team2 = metrics[num].text[3:-1]
    else:
        team1 = metrics[num].text[:1]
        team2 = metrics[num].text[2:-1]
    
    return [team1,team2]


html_text = requests.get('https://www.vsin.com/all-access/consensus-money-report/ncaambb/').text

soup_games = BeautifulSoup(html_text,'lxml')
rows = soup_games.find_all('tr')[1:]


ncaambb_teams = {}

for game in rows:
    metrics = game.find_all('td',class_='standTD')

    #Date of game
    date = metrics[0].text
    #Regex first instance of number and add space right before
    date = re.sub("[1-9]", lambda ele: " "+ele[0], date,1)
    #check for missing data
    if (date.split()[0] != curr_day) or metrics[1].text == "\xa0" or metrics[1].text == "" or metrics[2].text == "\xa0" or metrics[2].text == "" or metrics[3].text == "\xa0" or metrics[3].text == "" or metrics[4].text == "\xa0" or  metrics[4].text == "" or metrics[5].text == "\xa0" or metrics[5].text == "" or metrics[6].text == "\xa0" or metrics[6].text == "" or metrics[7].text == "\xa0" or metrics[7].text == "" or metrics[8].text == "\xa0" or metrics[8].text == "" or metrics[9].text == "\xa0" or metrics[9].text == "" or metrics[10].text == "" or metrics[10].text == "\xa0" :
        continue

    #Only nba team that begins with numbers is 76ers sort by them and then everyone else, Trail Blazers two letter name scrape them out
    clean_names = metrics[1].text
    name_list = re.split(r"\d+",clean_names)[1:]
    if not name_list:
        continue
    team1_name,team2_name = name_list[0].strip(),name_list[1].strip()

    
    ncaambb_teams[team1_name] = {}
    ncaambb_teams[team2_name] = {}

    ncaambb_teams[team1_name]['name'] = team1_name
    ncaambb_teams[team2_name]['name'] = team2_name

    #set home and away
    ncaambb_teams[team1_name]['home'] = False
    ncaambb_teams[team2_name]['home'] = True


    ncaambb_teams[team1_name]['opponent'] = team2_name
    ncaambb_teams[team2_name]['opponent'] = team1_name
    
    
    ncaambb_teams[team1_name]['date'] = date
    ncaambb_teams[team2_name]['date'] = date
    
    #metrics 2 is spreads needs data cleaning
    #4 cases either +1/-1, +1.5/-1.5, +11/-11, +11.5/-11.5
    #Each case the len of text is different
    
    #CASE +1/-1
    if len(metrics[2].text) == 4:
        team1_spread = metrics[2].text[:2]
        team2_spread = metrics[2].text[2:]

    #CASE +1.5/-1.5
    elif len(metrics[2].text) == 8:
        team1_spread = metrics[2].text[:4]
        team2_spread = metrics[2].text[4:]
    
    #CASE +11/-11
    elif len(metrics[2].text) == 6:
        team1_spread = metrics[2].text[:3]
        team2_spread = metrics[2].text[3:]
        
    #CASE +11.5/-11.5
    elif len(metrics[2].text) == 10:
        team1_spread = metrics[2].text[:5]
        team2_spread = metrics[2].text[5:]
    
    ncaambb_teams[team1_name]['spread'] = team1_spread
    ncaambb_teams[team2_name]['spread'] = team2_spread
      
    
    #If double digits in beggning split in 3s METRIC 3: HANDLE IN %
    
    team1_handle_spread, team2_handle_spread = split_percent(3)
    ncaambb_teams[team1_name]['handle_spread'] = team1_handle_spread
    ncaambb_teams[team2_name]['handle_spread'] = team2_handle_spread

    # Same as metric 3 except BET % in %    
    team1_betP_spread,team2_betP_spread = split_percent(4)
    ncaambb_teams[team1_name]['betP_spread'] = team1_betP_spread
    ncaambb_teams[team2_name]['betP_spread'] = team2_betP_spread
    
    #metric 5 the Money line will always be -+ followed by 3 digits

    if isdigit(metrics[5].text[4]):
        team1_ML = metrics[5].text[:5]
        team2_ML = metrics[5].text[5:]
    else:
        team1_ML = metrics[5].text[:4]
        team2_ML = metrics[5].text[4:]

    ncaambb_teams[team1_name]['ML'] = team1_ML
    ncaambb_teams[team2_name]['ML'] = team2_ML
    
    #metric 6 is again handle for ML same as 3
    team1_handle_ML,team2_handle_ML = split_percent(6)
    ncaambb_teams[team1_name]['handle_ML'] = team1_handle_ML
    ncaambb_teams[team2_name]['handle_ML'] = team2_handle_ML
    

    #metric 7 bet % same as 4    
    team1_betP_ML, team2_betP_ML = split_percent(7)
    ncaambb_teams[team1_name]['betP_ML'] = team1_betP_ML
    ncaambb_teams[team2_name]['betP_ML'] = team2_betP_ML
    
    #metric 8 involves O/U
    
    

    if metrics[8].text[5] == '.':
        over_under = 'O/U ' + metrics[8].text[2:7]
    else:
        over_under = 'O/U ' + metrics[8].text[2:5]
    
    ncaambb_teams[team1_name]['over_under'] = over_under
    ncaambb_teams[team2_name]['over_under'] = over_under
        
    #metric 9 is handle for over/under
    over_handle,under_handle = split_percent(9)

    ncaambb_teams[team1_name]['over_handle'] = over_handle
    ncaambb_teams[team1_name]['under_handle'] = under_handle
    ncaambb_teams[team2_name]['over_handle'] = over_handle
    ncaambb_teams[team2_name]['under_handle'] = under_handle

    #metric 10 bet% over/under
    over_betP,under_betP = split_percent(10)
    ncaambb_teams[team1_name]['over_betP'] = over_betP
    ncaambb_teams[team1_name]['under_betP'] = under_betP
    ncaambb_teams[team2_name]['over_betP'] = over_betP
    ncaambb_teams[team2_name]['under_betP'] = under_betP

    if int(team1_handle_ML) - int(team1_betP_ML) > 0:
        ncaambb_teams[team1_name]['sharp_ML'] = int(team1_handle_ML) - int(team1_betP_ML)
    else:
        ncaambb_teams[team1_name]['sharp_ML'] = 0
    
    if int(team2_handle_ML) - int(team2_betP_ML) > 0:
        ncaambb_teams[team2_name]['sharp_ML'] = int(team2_handle_ML) - int(team2_betP_ML)
    else:
        ncaambb_teams[team2_name]['sharp_ML'] = 0
    
    if int(team1_handle_spread) - int(team1_betP_spread) > 0:
        ncaambb_teams[team1_name]['sharp_spread'] = int(team1_handle_spread) - int(team1_betP_spread)
    else:
        ncaambb_teams[team1_name]['sharp_spread'] = 0
    
    if int(team2_handle_spread) - int(team2_betP_spread) > 0:
        ncaambb_teams[team2_name]['sharp_spread'] = int(team2_handle_spread) - int(team2_betP_spread)
    else:
        ncaambb_teams[team2_name]['sharp_spread'] = 0
        
    if int(over_handle) - int(over_betP) > 0:
        ncaambb_teams[team1_name]['sharp_over'] = int(over_handle) - int(over_betP)
        ncaambb_teams[team2_name]['sharp_over'] = int(over_handle) - int(over_betP)
    else:
        ncaambb_teams[team1_name]['sharp_over'] = 0
        ncaambb_teams[team2_name]['sharp_over'] = 0
    
    if int(under_handle) - int(under_betP) > 0:
        ncaambb_teams[team1_name]['sharp_under'] = int(under_handle) - int(under_betP)
        ncaambb_teams[team2_name]['sharp_under'] = int(under_handle) - int(under_betP)
    else:
        ncaambb_teams[team1_name]['sharp_under'] = 0
        ncaambb_teams[team2_name]['sharp_under'] = 0



public_ncaambb_sorted = sort_public(ncaambb_teams,'ncaambb_teams')

t_text = "#CBB Top Public Plays of the Day:\n"
count = 0
for team,bet,percent,league in public_ncaambb_sorted:
    if count == 4:
        break
    count+=1
    if bet == "betP_ML":
        t_line = f"#{team} ML ({ncaambb_teams[team]['ML']}) is getting {percent}% of wagers\n"
    if bet == "betP_spread":
        t_line = f"#{team} spread ({ncaambb_teams[team]['spread']}) is getting {percent}% of wagers\n"
    if bet == "over_betP":
        t_line = f"#{team} over ({ncaambb_teams[team]['over_under']}) is getting {percent}% of wagers\n"
    if bet == "under_betP":
        t_line = f"#{team} under ({ncaambb_teams[team]['over_under']}) is getting {percent}% of wagers\n"
    t_text+= t_line

t_text+="#GamblingTwitter"

#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)

    print('tweet sending')

sharp_ncaambb_sorted = sort_sharp(ncaambb_teams,'ncaambb_teams')

t_text = "#CBB Top Money Difference of the Day:\n"

count = 0
for team,bet,percent,league in sharp_ncaambb_sorted:
    if count == 3:
        break
    count+=1
    if bet == "sharp_ML":
        t_line = f"#{team} ML ({ncaambb_teams[team]['ML']}) is getting {ncaambb_teams[team]['betP_ML']}% of wagers and {ncaambb_teams[team]['handle_ML']}% of the money\n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({ncaambb_teams[team]['spread']}) is getting {ncaambb_teams[team]['betP_spread']}% of wagers {ncaambb_teams[team]['handle_spread']}% of the money\n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({ncaambb_teams[team]['over_under']}) is getting {ncaambb_teams[team]['over_betP']}% of wagers {ncaambb_teams[team]['over_handle']}% of the money\n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({ncaambb_teams[team]['over_under']}) is getting {ncaambb_teams[team]['under_betP']}% of wagers {ncaambb_teams[team]['under_handle']}% of the money\n"
    t_text+= t_line

t_text+="#GamblingTwitter"
#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)

    print('tweet sending')
    

