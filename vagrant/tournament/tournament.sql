-- Table definitions for the tournament project.
--

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- players in a tournament
CREATE TABLE players
(
    name TEXT NOT NULL,
    id SERIAL PRIMARY KEY
);

-- the set of matches in a tournament with winners and losers
CREATE TABLE matches
(
    winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
    loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
    CHECK (winner <> loser)
);

-- create a view for the number of player wins computation
CREATE VIEW number_of_wins AS SELECT players.id, COUNT(matches.winner) AS wins
    FROM players LEFT JOIN matches ON players.id = matches.winner
    GROUP BY players.id;

-- create a view for number of matches each player has played
CREATE VIEW number_of_matches AS SELECT players.id, COUNT(matches) AS matchcount
    FROM players LEFT JOIN matches ON players.id = matches.winner OR
    players.id = matches.loser GROUP BY players.id;
