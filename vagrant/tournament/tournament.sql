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
    id SERIAL PRIMARY KEY
    winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
    loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
    CHECK (winner <> loser)
);

