from curses.ascii import isdigit
from bs4 import BeautifulSoup
import re,requests,calendar,tweepy,config
from datetime import date
from helper import sort_public, sort_sharp

def getClient():
    client = tweepy.Client(
        consumer_key = config.consumer_key,
        consumer_secret= config.consumer_secret,
        access_token= config.access_token,
        access_token_secret= config.access_token_secret
        )
    return client

nhl_teams = {}

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
#------------------------#---------VSIN-ODDS---------------#------------------------#------------------------#------------------------

#Goal:Scrape vsin return top 5 discrepancy in money report

html_text = requests.get('https://www.vsin.com/all-access/consensus-money-report/nhl/').text
soup_games = BeautifulSoup(html_text,'lxml')
rows = soup_games.find_all('tr')[1:]
for game in rows:
    metrics = game.find_all('td',class_='standTD')

    #Date of game
    date = metrics[0].text
    #Regex first instance of number and add space right before
    date = re.sub("[1-9]", lambda ele: " "+ele[0], date,1)

    if (date.split()[0] != curr_day) or metrics[1].text[0] == "\xa0" or metrics[2].text[0] == "\xa0" or metrics[3].text[0] == "\xa0" or metrics[4].text[0] == "\xa0" or metrics[5].text[0] == "\xa0" or metrics[6].text[0] == "\xa0" or metrics[7].text[0] == "\xa0" or metrics[8].text[0] == "\xa0" or metrics[9].text[0] == "\xa0" or metrics[10].text[0] == "\xa0" :
        continue


    #Clean team 1 numbers out
    clean_names = metrics[1].text
    clean_names_split = re.split('(\d+)',clean_names)
    team1_name = clean_names_split[2].strip()
    team2_name = clean_names_split[-1].strip()

    
    nhl_teams[team1_name] = {}
    nhl_teams[team2_name] = {}

    nhl_teams[team1_name]['name'] = team1_name
    nhl_teams[team2_name]['name'] = team2_name

    #set home and away
    nhl_teams[team1_name]['home'] = False
    nhl_teams[team2_name]['home'] = True


    nhl_teams[team1_name]['opponent'] = team2_name
    nhl_teams[team2_name]['opponent'] = team1_name
    

    
    nhl_teams[team1_name]['date'] = date
    nhl_teams[team2_name]['date'] = date
    
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
    
    nhl_teams[team1_name]['spread'] = team1_spread
    nhl_teams[team2_name]['spread'] = team2_spread
      
    
    #If double digits in beggning split in 3s METRIC 3: HANDLE IN %
    
    team1_handle_spread, team2_handle_spread = split_percent(3)
    nhl_teams[team1_name]['handle_spread'] = team1_handle_spread
    nhl_teams[team2_name]['handle_spread'] = team2_handle_spread

    # Same as metric 3 except BET % in %    
    team1_betP_spread,team2_betP_spread = split_percent(4)
    nhl_teams[team1_name]['betP_spread'] = team1_betP_spread
    nhl_teams[team2_name]['betP_spread'] = team2_betP_spread
    
    #metric 5 the Money line will always be -+ followed by 3 digits
    if isdigit(metrics[5].text[4]):
        team1_ML = metrics[5].text[:5]
        team2_ML = metrics[5].text[5:]
    else:
        team1_ML = metrics[5].text[:4]
        team2_ML = metrics[5].text[4:]
        
    nhl_teams[team1_name]['ML'] = team1_ML
    nhl_teams[team2_name]['ML'] = team2_ML
    
    #metric 6 is again handle for ML same as 3
    team1_handle_ML,team2_handle_ML = split_percent(6)
    nhl_teams[team1_name]['handle_ML'] = team1_handle_ML
    nhl_teams[team2_name]['handle_ML'] = team2_handle_ML
    

    #metric 7 bet % same as 4    
    team1_betP_ML, team2_betP_ML = split_percent(7)
    nhl_teams[team1_name]['betP_ML'] = team1_betP_ML
    nhl_teams[team2_name]['betP_ML'] = team2_betP_ML
    
    #metric 8 involves O/U
    
    if metrics[8].text[3] == '.':
        over_under = 'O/U ' + metrics[8].text[2:5]
    else:
        over_under = 'O/U ' + metrics[8].text[2:3]
    
   
    nhl_teams[team1_name]['over_under'] = over_under
    nhl_teams[team2_name]['over_under'] = over_under
        
    #metric 9 is handle for over/under
    over_handle,under_handle = split_percent(9)

    nhl_teams[team1_name]['over_handle'] = over_handle
    nhl_teams[team1_name]['under_handle'] = under_handle
    nhl_teams[team2_name]['over_handle'] = over_handle
    nhl_teams[team2_name]['under_handle'] = under_handle

    #metric 10 bet% over/under
    over_betP,under_betP = split_percent(10)
    nhl_teams[team1_name]['over_betP'] = over_betP
    nhl_teams[team1_name]['under_betP'] = under_betP
    nhl_teams[team2_name]['over_betP'] = over_betP
    nhl_teams[team2_name]['under_betP'] = under_betP

    if int(team1_handle_ML) - int(team1_betP_ML) > 0:
        nhl_teams[team1_name]['sharp_ML'] = int(team1_handle_ML) - int(team1_betP_ML)
    else:
        nhl_teams[team1_name]['sharp_ML'] = 0
    
    if int(team2_handle_ML) - int(team2_betP_ML) > 0:
        nhl_teams[team2_name]['sharp_ML'] = int(team2_handle_ML) - int(team2_betP_ML)
    else:
        nhl_teams[team2_name]['sharp_ML'] = 0
    
    if int(team1_handle_spread) - int(team1_betP_spread) > 0:
        nhl_teams[team1_name]['sharp_spread'] = int(team1_handle_spread) - int(team1_betP_spread)
    else:
        nhl_teams[team1_name]['sharp_spread'] = 0
    
    if int(team2_handle_spread) - int(team2_betP_spread) > 0:
        nhl_teams[team2_name]['sharp_spread'] = int(team2_handle_spread) - int(team2_betP_spread)
    else:
        nhl_teams[team2_name]['sharp_spread'] = 0
        
    if int(over_handle) - int(over_betP) > 0:
        nhl_teams[team1_name]['sharp_over'] = int(over_handle) - int(over_betP)
        nhl_teams[team2_name]['sharp_over'] = int(over_handle) - int(over_betP)
    else:
        nhl_teams[team1_name]['sharp_over'] = 0
        nhl_teams[team2_name]['sharp_over'] = 0
    
    if int(under_handle) - int(under_betP) > 0:
        nhl_teams[team1_name]['sharp_under'] = int(under_handle) - int(under_betP)
        nhl_teams[team2_name]['sharp_under'] = int(under_handle) - int(under_betP)
    else:
        nhl_teams[team1_name]['sharp_under'] = 0
        nhl_teams[team2_name]['sharp_under'] = 0


public_nhl_sorted = sort_public(nhl_teams,'nhl_teams')
t_text = "#NHL Top Public Plays of the Day:\n"
count = 0
for team,bet,percent,league in public_nhl_sorted:
    if count == 4:
        break
    count+=1
    if bet == "betP_ML":
        t_line = f"#{team} ML ({nhl_teams[team]['ML']}) is getting {percent}% of wagers \n"
    if bet == "betP_spread":
        t_line = f"#{team} spread ({nhl_teams[team]['spread']}) is getting {percent}% of wagers \n"
    if bet == "over_betP":
        t_line = f"#{team} over ({nhl_teams[team]['over_under']}) is getting {percent}% of wagers \n"
    if bet == "under_betP":
        t_line = f"#{team} under ({nhl_teams[team]['over_under']}) is getting {percent}% of wagers \n"
    t_text+= t_line

t_text+="#GamblingTwitter"
#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)

    print('tweet sending')
sharp_nhl_sorted = sort_sharp(nhl_teams,'nhl_teams')

t_text = "#NHL Top Money Difference of the Day:\n"

count = 0
for team,bet,percent,league in sharp_nhl_sorted:
    if count == 3:
        break
    count+=1
    if bet == "sharp_ML":
        t_line = f"#{team} ML ({nhl_teams[team]['ML']}) is getting {nhl_teams[team]['betP_ML']}% of wagers and {nhl_teams[team]['handle_ML']}% of the money. \n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({nhl_teams[team]['spread']}) is getting {nhl_teams[team]['betP_spread']}% of wagers {nhl_teams[team]['handle_spread']}% of the money. \n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({nhl_teams[team]['over_under']}) is getting {nhl_teams[team]['over_betP']}% of wagers {nhl_teams[team]['over_handle']}% of the money. \n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({nhl_teams[team]['over_under']}) is getting {nhl_teams[team]['under_betP']}% of wagers {nhl_teams[team]['under_handle']}% of the money. \n"
    t_text+= t_line

t_text+="#GamblingTwitter"
#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)

    print('tweet sending')

