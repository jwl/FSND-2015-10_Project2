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

-- View for playerStandings()
CREATE VIEW standings AS
    SELECT 
        ROW_NUMBER() OVER() as rank,
        m1.p_id, m1.p_name, m2.wins, m1.total_matches
    FROM
    (
        SELECT
            players.p_id,
            players.p_name,
            count(matches.match_id) as total_matches
        FROM players
        LEFT JOIN matches
            ON players.p_id = matches.p1 OR players.p_id = matches.p2
        GROUP BY players.p_id
    ) m1 -- Table with total matches
    JOIN
    (
        SELECT players.p_id, count(matches.match_id) as wins
        FROM players
        LEFT JOIN matches
            ON
            (players.p_id = p1 AND matches.m_results = 1) OR
            (players.p_id = p2 AND matches.m_results = 2)
        GROUP BY players.p_id
    ) m2
    ON
    m1.p_id = m2.p_id
    GROUP BY m1.p_id, m1.p_name, m1.total_matches, m2.wins
    ORDER BY m2.wins DESC
;


-- View for showing odd-numbered standings in placements
CREATE VIEW odd_standings AS 
    SELECT
        standings.rank, p_id, p_name, wins, ROW_NUMBER() OVER() as match_number
    FROM
        standings
    WHERE
        mod(standings.rank, 2) = 1
    ORDER BY standings.rank
;

-- View for showing even-numbered standings in placements
CREATE VIEW even_standings AS 
    SELECT
        standings.rank, p_id, p_name, wins, ROW_NUMBER() OVER() as match_number
    FROM
        standings
    WHERE
        mod(standings.rank, 2) = 0
;


