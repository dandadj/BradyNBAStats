import sqlite3 as lite
import sys


def CreatePlayersDB(playersList):
    con = lite.connect('NBA.db')

    with con:    
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Players")
        cur.execute("CREATE TABLE Players(Id INTEGER PRIMARY KEY, Name TEXT, FromYear INT, ToYear INT, Position TEXT, Height INT, Weight INT, Birthdate TEXT, College TEXT, HallOfFame INT, Page TEXT)")
        for player in playersList:
            #cur.execute("INSERT INTO Players(Name, FromYear, ToYear, Position, Height, Weight, Birthdate, College) VALUES (:Name, :FromYear, :ToYear, :Position, :Height, :Weight, :Birthdate, :College);"), values)
            try:
                cur.execute('INSERT INTO Players(Name, FromYear, ToYear, Position, Height, Weight, Birthdate, College, HallOfFame, Page) VALUES (:Name, :FromYear, :ToYear, :Position, :Height, :Weight, :Birthdate, :College, :HallOfFame, :Page);', player)
            except Exception as e:
                print e
                print player
                sys.exit()