from scrape_nba import nba_teams,public_nba_sorted,sharp_nba_sorted
from scrape_nhl import nhl_teams,public_nhl_sorted,sharp_nhl_sorted
#from scrape_nfl import nfl_teams
from scrape_ncaafb import ncaafb_teams,public_ncaafb_sorted,sharp_ncaafb_sorted
from scrape_ncaambb import ncaambb_teams,public_ncaambb_sorted,sharp_ncaambb_sorted
from pshelper import sort_total
from twitter import getClient

public_sorted_total = sort_total(public_nba_sorted,public_nhl_sorted,public_ncaambb_sorted,public_ncaafb_sorted,4)
sharp_sorted_total = sort_total(sharp_nba_sorted,sharp_nhl_sorted,sharp_ncaambb_sorted,sharp_ncaafb_sorted,3)

#11AM weekends 6PM weekdays
t_text_public = "Overall Top Public Plays of the Day:\n"

for team,bet,percent,league in public_sorted_total:
    
    if bet == "betP_ML":
        t_line = f"#{team} ML ({eval(league)[team]['ML']}) is getting {percent}% of wagers \n"
    if bet == "betP_spread":
        t_line = f"#{team} spread ({eval(league)[team]['spread']}) is getting {percent}% of wagers \n"
    if bet == "over_betP":
        t_line = f"#{team} over ({eval(league)[team]['over_under']}) is getting {percent}% of wagers \n"
    if bet == "under_betP":
        t_line = f"#{team} under ({eval(league)[team]['over_under']}) is getting {percent}% of wagers \n"
    t_text_public+= t_line

t_text_public+="#GamblingTwitter"
client = getClient()
client.create_tweet(text = t_text_public,user_auth=True)

#SHARP Twitter text

t_text_sharp = "Top Money Difference of the Day:\n"

for team,bet,percent,league in sharp_sorted_total:

    if bet == "sharp_ML":
        t_line = f"#{team} ML ({eval(league)[team]['ML']}) is getting {eval(league)[team]['betP_ML']}% of wagers and {eval(league)[team]['handle_ML']}% of the money. \n"
    if bet == "sharp_spread":
        t_line = f"#{team} spread ({eval(league)[team]['spread']}) is getting {eval(league)[team]['betP_spread']}% of wagers {eval(league)[team]['handle_spread']}% of the money. \n"
    if bet == "sharp_over":
        t_line = f"#{team} over ({eval(league)[team]['over_under']}) is getting {eval(league)[team]['over_betP']}% of wagers {eval(league)[team]['over_handle']}% of the money. \n"
    if bet == "sharp_under":
        t_line = f"#{team} under ({eval(league)[team]['over_under']}) is getting {eval(league)[team]['under_betP']}% of wagers {eval(league)[team]['under_handle']}% of the money. \n"
    t_text_sharp+= t_line

t_text_sharp+="#GamblingTwitter"
client = getClient()
client.create_tweet(text = t_text_sharp,user_auth=True)