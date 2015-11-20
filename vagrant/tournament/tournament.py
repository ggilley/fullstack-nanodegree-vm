#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("select count(*) from players;")
    counts = cursor.fetchall()
    db.close()
    return counts[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("insert into players values (%s);",(name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("select players.id, players.name, count(matches.winner) as wins from players,  matches where players.id = matches.winner group by players.id;")
    wins = cursor.fetchall()
    cursor.execute("select players.id, players.name, count(matches) from players left join  matches on players.id = matches.winner or players.id = matches.loser group by players.id;")
    matches = cursor.fetchall()
    db.close()
    result = [(row[0], row[1], (lambda x = [item[2] for item in wins if item[0] == row[0]]: (x[0] if x else 0))(), row[2]) for row in matches]
    result = sorted(result, key=lambda tup: tup[2], reverse = True)
    return result


def reportMatch(winner, loser):
    
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("insert into matches values (%s,%s);",(winner,loser))
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []
    standings = playerStandings()
    print "standings = ", standings
    for (id1, name1, win1, loss1) in standings:
	for (id2, name2, win2, loss2) in standings:
	    if (id1 != id2 and 
		(pairings == [] or
		 (lambda x = [item for item in pairings if id2 == item[0] or id2 == item[2] or id1 == item[0] or id1 == item[2]]: 0 if x else 1)())):
	 	pairings.append((id1, name1, id2, name2))
		break
    print "pairings = ", pairings	
    return pairings
    

