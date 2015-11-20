#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

fifty_random_names = [ "Frederica Paley",
		"Tonie Vannatter",
		"Ted Heth",
		"Franklyn Rene",
		"Kiara Rossbach",
		"Pamala Bien",
		"Leia Rase",
		"Margarete Oldfield",
		"Chan Bolender",
		"Shaina Bostic",
		"Daniele Franson",
		"Tanesha Ringo",
		"Illa Jaworski",
		"Christiana Straley",
		"Mitchell Legaspi",
		"Eufemia Reasor",
		"Dudley Tovar",
		"Regena Wernick",
		"Evette Scharf",
		"Alix Messerly",
		"Shamika Leigh",
		"Annemarie Faivre",
		"Dale Lackner",
		"Aura Conwell",
		"Shantel Fryer",
		"Mikel Weeks",
		"Claude Tarter",
		"Christy Pates",
		"Inell Moss",
		"Nathan Miers",
		"Bruce Vong",
		"Kerri Chenail",
		"Lashawn Crosslin",
		"Madelyn Mucha",
		"Holli Defazio",
		"Jacqueline Curlee",
		"Brande Oberg",
		"Corene Stermer",
		"Lianne Mcleod",
		"Allyson Tolan",
		"Adolph Petit",
		"Emilio Hayashi",
		"Darrick Steckel",
		"Blossom Devane",
		"Destiny Brimmer",
		"Meghann Lecroy",
		"Long Hennings",
		"Kimberly Olivar",
		"Ralph Dice",
		"Theodore Conant"
		]

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def comparePairings(matches, pairings):
    wins = {}
    losses = {}
    # initialize the wins and losses dicts
    for m in matches:
	wins[m[0]] = 0
	wins[m[1]] = 0
	losses[m[0]] = 0
	losses[m[1]] = 0
    for m in matches:
	wins[m[0]] = wins[m[0]] + 1
	losses[m[1]] = losses[m[1]] + 1
    print "wins = ", wins
    print "losses = ", losses
    # if even number of matches, then all of the pairings should have the
    # same score
    if len(matches) % 2 == 0:
    	for p in pairings:
	    if wins[p[0]] != wins[p[2]]:
	   	return False
    else:
	wincount = 0
	for p in pairings:
	    if wins[p[0]] == wins[p[2]]:
		wincount = wincount + 1
    return True
    
def testTournament(number_of_players):
    """ test a complete swiss pairing tournament
	supports up to 50 players
    """
    deleteMatches()
    deletePlayers()
    for i in range(0, number_of_players):
	registerPlayer(fifty_random_names[i])
    standings = playerStandings()
    print "standings = ", standings
    player_ids = [row[0] for row in standings]
    matches = []
    for i in range(0, number_of_players, 2):
	matches.append((player_ids[i], player_ids[i+1]))
    for m in matches:
	reportMatch(m[0], m[1])
    pairings = swissPairings()
    if len(pairings) != len(matches):
	raise ValueError(
	    "For %s players, swissPairing should return %s pairs.",
	    number_of_players, len(matches))
    if comparePairings(matches, pairings) == False:
    	print "matches = ", matches
	print "pairs = ", pairings
        raise ValueError(
            "After one match, players with one win should be paired.")

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testTournament(6)
    print "Success!  All tests pass!"

  
