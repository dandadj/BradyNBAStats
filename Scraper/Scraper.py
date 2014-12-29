import urllib2
import re
from bs4 import BeautifulSoup

## Contants
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
            print player_info['name']
            all_players.append(player_info)
    return all_players


GetBRPlayers()