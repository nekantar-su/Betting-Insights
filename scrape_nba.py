from bs4 import BeautifulSoup
from datetime import date
import calendar,re,requests,tweepy,config
from curses.ascii import isdigit
from helper import sort_public,sort_sharp

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

def getClient():
    client = tweepy.Client(
        consumer_key = config.consumer_key,
        consumer_secret= config.consumer_secret,
        access_token= config.access_token,
        access_token_secret= config.access_token_secret
        )
    return client


html_text = requests.get('https://www.vsin.com/all-access/consensus-money-report/nba/').text
soup_games = BeautifulSoup(html_text,'lxml')
rows = soup_games.find_all('tr')[1:]


nba_teams = {}

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

    cleaned_names = re.findall('(76ers|[A-Za-z]+| [A-Za-z]+ [A-Za-z]+)',clean_names)
  
    team1_name,team2_name = cleaned_names[0].strip(),cleaned_names[1].strip()
 
    
    
    nba_teams[team1_name] = {}
    nba_teams[team2_name] = {}

    nba_teams[team1_name]['name'] = team1_name
    nba_teams[team2_name]['name'] = team2_name

    #set home and away
    nba_teams[team1_name]['home'] = False
    nba_teams[team2_name]['home'] = True


    nba_teams[team1_name]['opponent'] = team2_name
    nba_teams[team2_name]['opponent'] = team1_name
    
    
    nba_teams[team1_name]['date'] = date
    nba_teams[team2_name]['date'] = date
    
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
    
    nba_teams[team1_name]['spread'] = team1_spread
    nba_teams[team2_name]['spread'] = team2_spread
      
    
    #If double digits in beggning split in 3s METRIC 3: HANDLE IN %
    
    team1_handle_spread, team2_handle_spread = split_percent(3)
    nba_teams[team1_name]['handle_spread'] = team1_handle_spread
    nba_teams[team2_name]['handle_spread'] = team2_handle_spread

    # Same as metric 3 except BET % in %    
    team1_betP_spread,team2_betP_spread = split_percent(4)
    nba_teams[team1_name]['betP_spread'] = team1_betP_spread
    nba_teams[team2_name]['betP_spread'] = team2_betP_spread
    
    #metric 5 the Money line will always be -+ followed by 3 digits
    if isdigit(metrics[5].text[4]):
        team1_ML = metrics[5].text[:5]
        team2_ML = metrics[5].text[5:]
    else:
        team1_ML = metrics[5].text[:4]
        team2_ML = metrics[5].text[4:]
        
    nba_teams[team1_name]['ML'] = team1_ML
    nba_teams[team2_name]['ML'] = team2_ML
    
    #metric 6 is again handle for ML same as 3
    team1_handle_ML,team2_handle_ML = split_percent(6)
    nba_teams[team1_name]['handle_ML'] = team1_handle_ML
    nba_teams[team2_name]['handle_ML'] = team2_handle_ML
    

    #metric 7 bet % same as 4    
    team1_betP_ML, team2_betP_ML = split_percent(7)
    nba_teams[team1_name]['betP_ML'] = team1_betP_ML
    nba_teams[team2_name]['betP_ML'] = team2_betP_ML
    
    #metric 8 involves O/U
    
    

    if metrics[8].text[5] == '.':
        over_under = 'O/U ' + metrics[8].text[2:7]
    else:
        over_under = 'O/U ' + metrics[8].text[2:5]
    
    nba_teams[team1_name]['over_under'] = over_under
    nba_teams[team2_name]['over_under'] = over_under
        
    #metric 9 is handle for over/under
    over_handle,under_handle = split_percent(9)

    nba_teams[team1_name]['over_handle'] = over_handle
    nba_teams[team1_name]['under_handle'] = under_handle
    nba_teams[team2_name]['over_handle'] = over_handle
    nba_teams[team2_name]['under_handle'] = under_handle

    #metric 10 bet% over/under
    over_betP,under_betP = split_percent(10)
    nba_teams[team1_name]['over_betP'] = over_betP
    nba_teams[team1_name]['under_betP'] = under_betP
    nba_teams[team2_name]['over_betP'] = over_betP
    nba_teams[team2_name]['under_betP'] = under_betP

    if int(team1_handle_ML) - int(team1_betP_ML) > 0:
        nba_teams[team1_name]['sharp_ML'] = int(team1_handle_ML) - int(team1_betP_ML)
    else:
        nba_teams[team1_name]['sharp_ML'] = 0
    
    if int(team2_handle_ML) - int(team2_betP_ML) > 0:
        nba_teams[team2_name]['sharp_ML'] = int(team2_handle_ML) - int(team2_betP_ML)
    else:
        nba_teams[team2_name]['sharp_ML'] = 0
    
    if int(team1_handle_spread) - int(team1_betP_spread) > 0:
        nba_teams[team1_name]['sharp_spread'] = int(team1_handle_spread) - int(team1_betP_spread)
    else:
        nba_teams[team1_name]['sharp_spread'] = 0
    
    if int(team2_handle_spread) - int(team2_betP_spread) > 0:
        nba_teams[team2_name]['sharp_spread'] = int(team2_handle_spread) - int(team2_betP_spread)
    else:
        nba_teams[team2_name]['sharp_spread'] = 0
        
    if int(over_handle) - int(over_betP) > 0:
        nba_teams[team1_name]['sharp_over'] = int(over_handle) - int(over_betP)
        nba_teams[team2_name]['sharp_over'] = int(over_handle) - int(over_betP)
    else:
        nba_teams[team1_name]['sharp_over'] = 0
        nba_teams[team2_name]['sharp_over'] = 0
    
    if int(under_handle) - int(under_betP) > 0:
        nba_teams[team1_name]['sharp_under'] = int(under_handle) - int(under_betP)
        nba_teams[team2_name]['sharp_under'] = int(under_handle) - int(under_betP)
    else:
        nba_teams[team1_name]['sharp_under'] = 0
        nba_teams[team2_name]['sharp_under'] = 0
    

public_nba_sorted = sort_public(nba_teams,'nba_teams')
t_text = "#NBA Top Public Plays of the Day:\n"
count = 0
for team,bet,percent,league in public_nba_sorted:
    if count == 4:
        break
    count+=1
    if bet == "betP_ML":
        t_line = f"#{team} ML ({nba_teams[team]['ML']}) is getting {percent}% of wagers\n"
    if bet == "betP_spread":
        t_line = f"#{team} spread ({nba_teams[team]['spread']}) is getting {percent}% of wagers\n"
    if bet == "over_betP":
        t_line = f"#{team} over ({nba_teams[team]['over_under']}) is getting {percent}% of wagers\n"
    if bet == "under_betP":
        t_line = f"#{team} under ({nba_teams[team]['over_under']}) is getting {percent}% of wagers\n"
    t_text+= t_line

t_text+="#GamblingTwitter"
#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    print('tweet sending')
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)


sharp_nba_sorted = sort_sharp(nba_teams,'nba_teams')

t_text = "#NBA Top Money Difference of the Day:\n"

count = 0
for team,bet,percent,league in sharp_nba_sorted:
    if count == 3:
        break
    count+=1
    if bet == "sharp_ML":
        t_line = f"#{team} ML ({nba_teams[team]['ML']}) is getting {nba_teams[team]['betP_ML']}% of wagers and {nba_teams[team]['handle_ML']}% of the money\n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({nba_teams[team]['spread']}) is getting {nba_teams[team]['betP_spread']}% of wagers {nba_teams[team]['handle_spread']}% of the money\n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({nba_teams[team]['over_under']}) is getting {nba_teams[team]['over_betP']}% of wagers {nba_teams[team]['over_handle']}% of the money\n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({nba_teams[team]['over_under']}) is getting {nba_teams[team]['under_betP']}% of wagers {nba_teams[team]['under_handle']}% of the money\n"
    t_text+= t_line

t_text+="#GamblingTwitter"

#Ensure games are in before sending tweet
if len(t_text) > 60:
    #Send tweet
    print('tweet sending')
    client = getClient()
    client.create_tweet(text = t_text,user_auth=True)

