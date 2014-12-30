import urllib2
import re
from bs4 import BeautifulSoup
from NBADatabase import *
from PlayerMongo import *

## Constants
#B_R stands for Basketball-Reference.com
B_R_PAGE = "http://www.basketball-reference.com/"
B_R_PLAYERS_PAGE = B_R_PAGE + "players/"


def GetBRPlayers():
    all_letters = list(map(chr, range(97, 123)))
    all_players = []
    for letter in all_letters:
        letter_page = B_R_PLAYERS_PAGE + letter
        response = urllib2.urlopen(letter_page)
        letter_soup = BeautifulSoup(response.read())
        table = letter_soup.find(id='players')
        if table == None:
            continue
        rows = table.find_all('tr')
        for row in rows:
            player_info = {}
            cells = row.find_all('td')
            if len(cells) != 8:
                continue
            player_info['Page'] = cells[0].a['href']
            player_info['Name'] = cells[0].text
            hall_of_fame = False
            if '*' in player_info['Name']:
                hall_of_fame = True
                player_info['Name'] = player_info['Name'].replace("*","")
            player_info['FromYear'] = int(cells[1].text)
            player_info['ToYear'] = int(cells[2].text)
            player_info['Position'] = cells[3].text
            player_info['Height'] = cells[4].text
            player_info['Weight'] = cells[5].text
            player_info['Birthdate'] = cells[6].text
            player_info['College'] = cells[7].text
            player_info['HallOfFame'] = hall_of_fame
            all_players.append(player_info)
    return all_players

def TableToDictionary(table):
    headers = table.find_all('th')
    headers_text = []
    for header in headers:
        headers_text.append(header.text)
    rows = table.find_all('tr')
    entire_table = []
    for row in rows:
        cells = row.find_all('td')
        cells_text = []
        for cell in cells:
            text = cell.text
            text = text.replace(u'\xa0\u2605', u'')
            cells_text.append(text)
        stats = dict(zip(headers_text, cells_text))
        entire_table.append(stats)
    return entire_table

def GetTables(url):
    all_tables_as_dictionaries = []
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    tables = soup.find_all("div", { "class" : "table_container" })
    for table in tables:
        all_tables_as_dictionaries.append(TableToDictionary(table))
    return all_tables_as_dictionaries

def GetAllPlayersStats():
    all_players = GetBRPlayers()
    all_links = []
    all_players_stats = []
    for player in all_players:
        all_links.append(B_R_PAGE + player['page'][1:])
    for link in all_links:
        all_players_stats.append(GetTables(link))
    return all_players_stats




if __name__ == "__main__":
    players = GetBRPlayers()
    #print GetTables("http://www.basketball-reference.com/players/d/duncati01.html")
    #print "creating db table"
    #CreatePlayersDB(players)
    CreatePlayersMongo(players)
