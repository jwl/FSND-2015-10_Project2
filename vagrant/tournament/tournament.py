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
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()



def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute('''
        SELECT count(*) as num
        FROM players
    ''')
    playerCount = c.fetchone()[0]
    conn.commit()
    conn.close()
    return playerCount




def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT into players (p_name) values (%s)", (name,))
    conn.commit()
    conn.close()



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
    conn = connect()
    c = conn.cursor()
    c.execute('''
        SELECT m1.p_id, m1.p_name, m2.wins, m1.total_matches
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
    ''')
    results = c.fetchall()
    # print results
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Note: Although the matches table schema supports the winner being either
    p1 or p2 this function will always record the winner as p1.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO matches
            (p1, p2, m_results) VALUES
            (%s, %s, 1)
        ;
        ''',
        (winner, loser)
    )
    conn.commit()
    conn.close()


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

    # Use views odd_standings and even_standings to generate swiss pairs
    conn = connect()
    c = conn.cursor()
    c.execute('''
        SELECT 
            odd_standings.p_id as oddPlayerID
            , odd_standings.p_name as oddPlayerName
            , even_standings.p_id as evenPlayerID
            , even_standings.p_name as evenPlayerName
        FROM
            odd_standings
            JOIN
            even_standings
            ON
                odd_standings.match_number = even_standings.match_number
        ;
        '''
    )
    pairings = c.fetchall()
    conn.close()
    return pairings


