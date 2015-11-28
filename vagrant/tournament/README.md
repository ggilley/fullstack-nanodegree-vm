
#Quickstart

    run "psql -f tournament.sql" to create the database
    run "python tournament_test.py" to test the swiss pairings

#What's Included

Within the zip file, you'll find the following files:

    README.md - this file
    tournament.py - functions to generate a swiss tournament pairing
    tournament.sql - creates the tables for the tournament database
    tournament_test.py - a set of tests to validate the functions in tournament
    
#How to use

Import the tournament package.

Start by calling deleteMatches() and deletePlayers() to make sure the database
is clean.

Register each player by calling registerPlayer() with the player's name.

Call swissPairings() to generate a set of matches.

After the matches have been played, call reportMatch() with the winner id and
loser id for each match.

After reporting the match results, call swissPairings() again to create the next
set of pairings.

You can call playerStandings() at any time to see the current player standings.


