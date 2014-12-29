import urllib2
import re
from bs4 import BeautifulSoup

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
            player_info['page'] = cells[0].a['href']
            player_info['name'] = cells[0].text
            hall_of_fame = False
            if '*' in player_info['name']:
                hall_of_fame = True
                player_info['name'] = player_info['name'].replace("*","")
            player_info['from'] = int(cells[1].text)
            player_info['to'] = int(cells[2].text)
            player_info['position'] = cells[3].text
            player_info['height'] = cells[4].text
            player_info['weight'] = cells[5].text
            player_info['birthdate'] = cells[6].text
            player_info['college'] = cells[7].text
            player_info['hall_of_fame'] = hall_of_fame
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
    # print GetBRPlayers()
    # print GetTables("http://www.basketball-reference.com/players/d/duncati01.html")
    print GetAllPlayersStats()
