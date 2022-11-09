#DATA is pulled from Action network, Vsin, and scoreandodds none of the stats or odds are my own
from curses.ascii import isdigit
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re,tweepy,requests,config,calendar
from datetime import date
from helper import sort_public,sort_sharp

nfl_teams = {}

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

#------------------------#---------VSIN-ODDS---------------#------------------------#------------------------#------------------------

#Goal:Scrape vsin return top 5 discrepancy in money report

html_text = requests.get('https://www.vsin.com/all-access/consensus-money-report/nfl/').text
soup_games = BeautifulSoup(html_text,'lxml')
rows = soup_games.find_all('tr')[1:]
for game in rows:
    metrics = game.find_all('td',class_='standTD')

    #Date of game
    date = metrics[0].text
    #Regex first instance of number and add space right before
    date = re.sub("[1-9]", lambda ele: " "+ele[0], date,1)
    #(date.split()[0] != curr_day) or
    if metrics[1].text == "\xa0" or metrics[1].text == "" or metrics[2].text == "\xa0" or metrics[2].text == "" or metrics[3].text == "\xa0" or metrics[3].text == "" or metrics[4].text == "\xa0" or  metrics[4].text == "" or metrics[5].text == "\xa0" or metrics[5].text == "" or metrics[6].text == "\xa0" or metrics[6].text == "" or metrics[7].text == "\xa0" or metrics[7].text == "" or metrics[8].text == "\xa0" or metrics[8].text == "" or metrics[9].text == "\xa0" or metrics[9].text == "" or metrics[10].text == "" or metrics[10].text == "\xa0" :
        continue


    #Clean team 1 numbers out
    clean_names = metrics[1].text
    clean_names_split = re.split('(\d+ )',clean_names)
    
    
    team1_name = clean_names_split[2].strip()
    team2_name = clean_names_split[-1].strip()
    
    
    nfl_teams[team1_name] = {}
    nfl_teams[team2_name] = {}

    nfl_teams[team1_name]['name'] = team1_name
    nfl_teams[team2_name]['name'] = team2_name

    #set home and away
    nfl_teams[team1_name]['home'] = False
    nfl_teams[team2_name]['home'] = True


    nfl_teams[team1_name]['opponent'] = team2_name
    nfl_teams[team2_name]['opponent'] = team1_name
    

    
    nfl_teams[team1_name]['date'] = date
    nfl_teams[team2_name]['date'] = date
    
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
    
    nfl_teams[team1_name]['spread'] = team1_spread
    nfl_teams[team2_name]['spread'] = team2_spread
      
    
    #If double digits in beggning split in 3s METRIC 3: HANDLE IN %
    
    team1_handle_spread, team2_handle_spread = split_percent(3)
    nfl_teams[team1_name]['handle_spread'] = team1_handle_spread
    nfl_teams[team2_name]['handle_spread'] = team2_handle_spread

    # Same as metric 3 except BET % in %    
    team1_betP_spread,team2_betP_spread = split_percent(4)
    nfl_teams[team1_name]['betP_spread'] = team1_betP_spread
    nfl_teams[team2_name]['betP_spread'] = team2_betP_spread
    
    #metric 5 the Money line will always be -+ followed by 3 digits
    if isdigit(metrics[5].text[4]):
        team1_ML = metrics[5].text[:5]
        team2_ML = metrics[5].text[5:]
    else:
        team1_ML = metrics[5].text[:4]
        team2_ML = metrics[5].text[4:]
        
    nfl_teams[team1_name]['ML'] = team1_ML
    nfl_teams[team2_name]['ML'] = team2_ML
    
    #metric 6 is again handle for ML same as 3
    team1_handle_ML,team2_handle_ML = split_percent(6)
    nfl_teams[team1_name]['handle_ML'] = team1_handle_ML
    nfl_teams[team2_name]['handle_ML'] = team2_handle_ML
    

    #metric 7 bet % same as 4    
    team1_betP_ML, team2_betP_ML = split_percent(7)
    nfl_teams[team1_name]['betP_ML'] = team1_betP_ML
    nfl_teams[team2_name]['betP_ML'] = team2_betP_ML
    
    #metric 8 involves O/U
    
    if metrics[8].text[4] == '.':
        over_under = 'O/U ' + metrics[8].text[2:6]
    else:
        over_under = 'O/U ' + metrics[8].text[2:4]
    
    nfl_teams[team1_name]['over_under'] = over_under
    nfl_teams[team2_name]['over_under'] = over_under
        
    #metric 9 is handle for over/under
    over_handle,under_handle = split_percent(9)

    nfl_teams[team1_name]['over_handle'] = over_handle
    nfl_teams[team1_name]['under_handle'] = under_handle
    nfl_teams[team2_name]['over_handle'] = over_handle
    nfl_teams[team2_name]['under_handle'] = under_handle

    #metric 10 bet% over/under
    over_betP,under_betP = split_percent(10)
    nfl_teams[team1_name]['over_betP'] = over_betP
    nfl_teams[team1_name]['under_betP'] = under_betP
    nfl_teams[team2_name]['over_betP'] = over_betP
    nfl_teams[team2_name]['under_betP'] = under_betP

    if int(team1_handle_ML) - int(team1_betP_ML) > 0:
        nfl_teams[team1_name]['sharp_ML'] = int(team1_handle_ML) - int(team1_betP_ML)
    else:
        nfl_teams[team1_name]['sharp_ML'] = 0
    
    if int(team2_handle_ML) - int(team2_betP_ML) > 0:
        nfl_teams[team2_name]['sharp_ML'] = int(team2_handle_ML) - int(team2_betP_ML)
    else:
        nfl_teams[team2_name]['sharp_ML'] = 0
    
    if int(team1_handle_spread) - int(team1_betP_spread) > 0:
        nfl_teams[team1_name]['sharp_spread'] = int(team1_handle_spread) - int(team1_betP_spread)
    else:
        nfl_teams[team1_name]['sharp_spread'] = 0
    
    if int(team2_handle_spread) - int(team2_betP_spread) > 0:
        nfl_teams[team2_name]['sharp_spread'] = int(team2_handle_spread) - int(team2_betP_spread)
    else:
        nfl_teams[team2_name]['sharp_spread'] = 0
        
    if int(over_handle) - int(over_betP) > 0:
        nfl_teams[team1_name]['sharp_over'] = int(over_handle) - int(over_betP)
        nfl_teams[team2_name]['sharp_over'] = int(over_handle) - int(over_betP)
    else:
        nfl_teams[team1_name]['sharp_over'] = 0
        nfl_teams[team2_name]['sharp_over'] = 0
    
    if int(under_handle) - int(under_betP) > 0:
        nfl_teams[team1_name]['sharp_under'] = int(under_handle) - int(under_betP)
        nfl_teams[team2_name]['sharp_under'] = int(under_handle) - int(under_betP)
    else:
        nfl_teams[team1_name]['sharp_under'] = 0
        nfl_teams[team2_name]['sharp_under'] = 0


#for team in nfl_teams:
#    print(team)

#------------------------#---------END-OF-VSIN---------------#------------------------#------------------------#------------------------

#------------------------#---------TRENDS---------------#------------------------#------------------------#------------------------

#Scrape all top trends and formulate into nfl_teams
#Can also scrape vsin Trends and add on

html_text_trends = requests.get('https://www.scoresandodds.com/nfl/trends').text
soup_trends = BeautifulSoup(html_text_trends,'lxml')
trends = soup_trends.find_all('div',class_='trend-card-details')
#Lists trends for each team
for x in trends:
    text = x.find('p').text
    team = text.split()[0]
    if team not in nfl_teams:
        continue
    if 'trends' in nfl_teams[team]:
        nfl_teams[team]['trends'].append(text)
    else:
        nfl_teams[team]['trends'] = [text]


#------------------------#------END-OF-TRENDS---------------#------------------------#------------------------#------------------------

#----------------------------Donbest----------------------------------------------------------

html_don_best = requests.get('https://legacy.donbest.com/nfl/trends-classic/').text

html_don_trends = BeautifulSoup(html_don_best,'lxml')
don_trends = html_don_trends.find_all('td',class_='matchupCells')

team_name = {
    'TAMPA' : 'Buccaneers',
    'BALTIMORE' : 'Ravens',
    'DENVER' :  'Broncos',
    'JACKSONVILLE' : 'Jaguars',
    'CHICAGO' : 'Bears',
    'DALLAS' : 'Cowboys',
    'LAS': 'Raiders',
    'ORLEANS': 'Saints',
    'CAROLINA' : 'Panthers',
    'ATLANTA' : 'Falcons',
    'PITTSBURGH': 'Steelers',
    'PHILADELPHIA' : 'Eagles',
    'MIAMI' : 'Dolphins',
    'DETROIT' : 'Lions',
    'ARIZONA' : 'Cardinals',
    'MINNESOTA' : 'Vikings',
    'ENGLAND' : 'Patriots',
    'JETS' : 'Jets',
    'TENNESSEE' : 'Titans',
    'HOUSTON' : 'Texans',
    'GIANTS' : 'Giants',
    'SEATTLE' : 'Seahawks',
    'WASHINGTON' : 'Commanders',
    'INDIANAPOLIS' : 'Colts',
    'SAN' : '49ers',
    'RAMS' : 'Rams',
    'GREEN' : 'Packers',
    'BUFFALO' : 'Bills',
    'CINCINNATI' : 'Bengals',
    'CLEVELAND' : 'Browns',
    'KANSAS' : 'Chiefs',
    'CHARGERS': 'Chargers'

}

for trend in don_trends:
    #filter out non team names
    if trend.text[1].isupper():
        don_name_split = trend.text.split()
        if don_name_split[0] == 'NY' or don_name_split[0] == 'LA' or don_name_split[0] == 'NEW':
            don_name = (team_name[don_name_split[1]])

        else:
            don_name = (team_name[don_name_split[0]])
        
        if  don_name not in nfl_teams:
            continue

        
        if 'trends' in nfl_teams[don_name]:
            nfl_teams[don_name]['trends'].append(trend.text)
        else:
            nfl_teams[don_name]['trends'] = [trend.text]




#-----------------------#---------ACTION-OPEN-CLOSE-ODDS---------------#------------------------#------------------------#------------------------

ua = UserAgent()

headers = {
    'user-agent': ua.random
}

html_odds = requests.get('https://www.actionnetwork.com/nfl/odds',headers=headers).text
soup_odds = BeautifulSoup(html_odds,'lxml')


rows = soup_odds.find_all('tr')
for row in rows:
    team_name = row.find_all('div',class_='game-info__team--desktop')
    open_odds = row.find_all('div',class_='best-odds__open-cell')
    current_odds = row.find_all('div',class_='book-cell__odds')[:2]
   
    #zip to get odds and team together
    team_odds = zip(team_name,open_odds,current_odds)
    #more optimal way to delete all {} in zip
    for team,open,current in list(team_odds):

        name = team.text
        if name not in nfl_teams:
            nfl_teams[name] = {}

        
        open = open.text[:-4] + ' ('+open.text[-4:] + ')'
        current = current.text[:-4] + ' ('+current.text[-4:] + ')'
        
        nfl_teams[name]['open'] = open
        nfl_teams[name]['current'] = current

public_nfl_sorted = sort_public(nfl_teams,'nfl_teams')

t_text = '#NFL Top Public Plays of the Day:\n'
count = 0
for team,bet,percent,league in public_nfl_sorted:
    if count == 5:
        break
    count+=1
    if bet == "betP_ML":
        t_line = f"#{team} ML ({nfl_teams[team]['ML']}) is getting {percent}% of wagers \n"
    if bet == "betP_spread":
        t_line = f"#{team} spread ({nfl_teams[team]['spread']}) is getting {percent}% of wagers \n"
    if bet == "over_betP":
        t_line = f"#{team} over ({nfl_teams[team]['over_under']}) is getting {percent}% of wagers \n"
    if bet == "under_betP":
        t_line = f"#{team} under ({nfl_teams[team]['over_under']}) is getting {percent}% of wagers \n"
    t_text+= t_line

t_text+="#GamblingTwitter"

#Ensure games are in before sending tweet
#if len(t_text) > 60:
    #Send tweet
    #print('tweet sending')
    #client = getClient()
    #client.create_tweet(text = t_text,user_auth=True)

sharp_nfl_sorted = sort_sharp(nfl_teams,'nfl_teams')

t_text = "#NFL Top Money Difference of the Day:\n"
count = 0
for team,bet,percent,league in sharp_nfl_sorted:
    if count == 3:
        break
    count+=1
    if bet == "sharp_ML":
        t_line = f"#{team} ML ({nfl_teams[team]['ML']}) is getting {nfl_teams[team]['betP_ML']}% of wagers and {nfl_teams[team]['handle_ML']}% of the money. \n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({nfl_teams[team]['spread']}) is getting {nfl_teams[team]['betP_spread']}% of wagers {nfl_teams[team]['handle_spread']}% of the money. \n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({nfl_teams[team]['over_under']}) is getting {nfl_teams[team]['over_betP']}% of wagers {nfl_teams[team]['over_handle']}% of the money. \n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({nfl_teams[team]['over_under']}) is getting {nfl_teams[team]['under_betP']}% of wagers {nfl_teams[team]['under_handle']}% of the money. \n"
    t_text+= t_line

t_text+="#GamblingTwitter"
#Ensure games are in before sending tweet
#if len(t_text) > 60:
    #Send tweet
    #print('tweet sending')
    #client = getClient()
    #client.create_tweet(text = t_text,user_auth=True)


'''
    #Create tweet for twitter followers
    t_text = ""

    if nfl_teams[team]['home']:
        tline1 = f"#{nfl_teams[team]['opponent']} at #{team} \n"
    else:
        tline1 = f"#{team} at #{nfl_teams[team]['opponent']} \n"

    tline2 = two +" \n"
    tline3 = four + " \n"
    tline4 = eight + " \n"
    #two,three,eight
    #t_end = "#GamblingTwitter"

    client = getClient()
    client.create_tweet(text=tline1+tline2+tline3+tline4,user_auth=True)
'''