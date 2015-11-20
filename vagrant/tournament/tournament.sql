-- Table definitions for the tournament project.
--

create table players
(
    name text,
    id serial primary key
);

create table matches
(
    winner integer references players(id),
    loser integer references players(id)
);

