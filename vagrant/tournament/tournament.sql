-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Create tournaments database (and drop it if it already exists)
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connect to our new database
\c tournament

-- Create tables
CREATE TABLE players (
	p_id SERIAL PRIMARY KEY,
	p_name TEXT
);

-- for clarity's sake, in the context of tables call tournaments 'tourneys'
CREATE TABLE tourneys (
	tourney_id SERIAL PRIMARY KEY,
	tourney_desc TEXT
);

CREATE TABLE matches (
	match_id SERIAL PRIMARY KEY,
	t_id INTEGER references tourneys(tourney_id),
	p1 INTEGER references players(p_id),
	p2 INTEGER references players(p_id),
	-- Possible values for m_results:
	-- * -2: "unplayed"
	-- * -1: "in-progress"
	-- * 0: "tie"
	-- * 1: p1 is winner
	-- * 2: p2 is winner
	-- Note: For this project, all matches in this table are assumed to be
	-- completed with either a winner or a tie.
	m_results INTEGER
);


-- Views
-- CREATE VIEW



