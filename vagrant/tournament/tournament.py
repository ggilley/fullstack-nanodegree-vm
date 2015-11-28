#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from itertools import combinations


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Failed to connect to database: ", database_name)

def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("select count(*) from players;")
    count = cursor.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("insert into players values (%s);", (name, ))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()
    # create a view for the number of player wins computation
    cursor.execute("create view number_of_wins as select players.id, count(matches.winner) as wins from players left join matches on players.id = matches.winner group by players.id;") # noqa
    # create a view for number of matches each player has played
    cursor.execute("create view number_of_matches as select players.id, count(matches) as matchcount from players left join matches on players.id = matches.winner or players.id = matches.loser group by players.id;") # noqa
    # now join the number of wins and matches and order by the number of wins
    cursor.execute("select players.id, players.name, number_of_wins.wins, number_of_matches.matchcount from players join number_of_wins on players.id = number_of_wins.id join number_of_matches on players.id = number_of_matches.id order by number_of_wins.wins desc;") # noqa
    result = cursor.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    cursor.execute("insert into matches values (%s,%s);", (winner, loser))
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

    # create a set of combinations of players
    combo = combinations(standings, 2)
    # create a set of pairings making sure that each player only plays once
    for c in combo:
        if pairings == [] or (lambda x=[item for item in
                                pairings if c[0][0] == item[0] or
                                c[0][0] == item[2] or c[1][0] == item[0] or
                                c[1][0] == item[2]]: 0 if x else 1)():
            pairings.append((c[0][0], c[0][1], c[1][0], c[1][1]))

    return pairings
