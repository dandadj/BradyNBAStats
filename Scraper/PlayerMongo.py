from pymongo import MongoClient

def CreatePlayersMongo(playersList):
    client = MongoClient()
    db = client['NBAStats']
    players = db['players']
    for player in playersList:
        players.insert(player)
    print players
    print db.collection_names()


    

