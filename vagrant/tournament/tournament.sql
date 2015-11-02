-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Create tournaments database (and drop it if it already exists)
DROP DATABASE IF EXISTS tournaments;
CREATE DATABASE tournaments;

-- Connect to our new database
\c tournaments

-- Create tables
CREATE TABLE registered_players (
	player_id SERIAL PRIMARY KEY,
	player_name TEXT
);

CREATE TABLE tournaments (
	tourney_id SERIAL PRIMARY KEY,
	tourney_desc TEXT
);

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	t_id INTEGER references tournaments(tourney_id),
	p1 INTEGER references registered_players(player_id),
	p2 INTEGER references registered_players(player_id),
	-- Possible values for m_results:
	-- * "unplayed"
	-- * "in-progress"
	-- * "p1" (p1 is winner)
	-- * "p2" (p2 is winner)
	-- * "tie"
	m_results text
);


-- CREATE TABLE posts ( content TEXT,
                     -- time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     -- id SERIAL );


