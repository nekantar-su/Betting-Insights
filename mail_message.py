from scrape_nfl import nfl_teams

added_teams = set()
html = """\
    <html>
    <head>
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    padding:15px;
    
    }
    </style>   
    </head>
    <body>
    <p>PSA: ALL lines are pulled from action network. All money and handle statistics are pulled from VSIN. All trends are pulled from www.scoresandodds.com and donbest.com.</p>
    """
for team in nfl_teams:
    #Set to ensure we dont add games twice listed below is the order in which sentences will be formed
    if team in added_teams:
        continue

    if nfl_teams[team]['home']:
        one = f"{nfl_teams[team]['opponent']} at {team} "
    else:
        one = f"{team} at {nfl_teams[team]['opponent']} "
    
    added_teams.add(team)
    added_teams.add(nfl_teams[team]['opponent'])
    
    

    one+= f"at {nfl_teams[team]['date']}"

    html += "<h3> <u>"+ one + "</u></h3>"



    if int(nfl_teams[team]['handle_spread']) - int(nfl_teams[team]['betP_spread']) > 20:
        sharp = f"<b>Sharp action</b> tracked on {team}"
        html+="<p>"+sharp+'</p>'
    
    if int(nfl_teams[nfl_teams[team]['opponent']]['handle_spread']) - int(nfl_teams[nfl_teams[team]['opponent']]['betP_spread']) > 20:
        sharp = f"<b>Sharp action</b> tracked on {nfl_teams[team]['opponent']}"
        html+="<p>"+sharp+'</p>'
    
    if int(nfl_teams[team]['betP_spread']) > 70:
        public_play = team+" is a <b>BIG public play</b>!"
        html+="<p>"+public_play+"</p>"
    
    if int(nfl_teams[nfl_teams[team]['opponent']]['betP_spread']) > 70:
        public_play = nfl_teams[team]['opponent']+" is a <b>BIG public play</b>!"
        html+="<p>"+public_play+"</p>"
    
    
    two = f"{nfl_teams[team]['name']} opened at {nfl_teams[team]['open']} and are currently at {nfl_teams[team]['current']}."
    
    html+="<ul>"
    html+= "<li>" + two + "</li>"
    #get back into nfl_teams after getting opponent name
    three = f"{nfl_teams[team]['opponent']} opened at {nfl_teams[nfl_teams[team]['opponent']]['open']} and are currently at {nfl_teams[nfl_teams[team]['opponent']]['current']}."
    
    html+= "<li>" + three + "</li>"

    four = f"{nfl_teams[team]['name']} {nfl_teams[team]['current']} is getting {nfl_teams[team]['betP_spread']}% of the bets and {nfl_teams[team]['handle_spread']}% of the handle."

    html+= "<li>" + four + "</li>"

    five = f"{nfl_teams[team]['opponent']} {nfl_teams[nfl_teams[team]['opponent']]['current']} is getting {nfl_teams[nfl_teams[team]['opponent']]['betP_spread']}% of the bets and {nfl_teams[nfl_teams[team]['opponent']]['handle_spread']}% of the handle."

    html+= "<li>" + five + "</li>"

    six = f"{nfl_teams[team]['name']} moneyline ({nfl_teams[team]['ML']}) is getting {nfl_teams[team]['betP_ML']}% of the bets and {nfl_teams[team]['handle_ML']}% of the handle."

    html+= "<li>" + six + "</li>"

    seven = f"{nfl_teams[team]['opponent']} moneyline ({nfl_teams[nfl_teams[team]['opponent']]['ML']}) is getting {nfl_teams[nfl_teams[team]['opponent']]['betP_ML']}% of the bets and {nfl_teams[nfl_teams[team]['opponent']]['handle_ML']}% of the handle."
    
    html+= "<li>" + seven + "</li>"

    eight = f"The over/under is sitting at {nfl_teams[team]['over_under']}. The over is receiving {nfl_teams[team]['over_betP']}% of the bets and {nfl_teams[team]['over_handle']}% of the handle. "

    html+= "<li>" + eight + "</li>"

    nine = f"The under is receiving {nfl_teams[team]['under_betP']}% of the bets and {nfl_teams[team]['under_handle']}% of the handle. "

    html+="<li>"+ nine + "</li>"

    html+="""\
        </ul>
        <table>
        <tr>
        <th> TRENDS </th>
        </tr> """
    
    #game_trends += nfl_teams[[team]['opponent']]['trends']

    if 'trends' in nfl_teams[team]:
        game_trends = nfl_teams[team]['trends']

        if 'trends' in nfl_teams[nfl_teams[team]['opponent']]:
            game_trends.extend(nfl_teams[nfl_teams[team]['opponent']]['trends'])

        count = 0
        for trend in game_trends:
            if count == 4:
                break
            html+= "<tr>" + trend +"</tr>"
            count+=1
    else:
        html+="<p>NO TRENDS AVAILABLE</p>"

    html+="""\
        
        </table>
        </body>
        </html>"""