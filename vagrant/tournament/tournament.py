#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("DELETE FROM matches")
    cursor.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute(
        '''
            SELECT count(*) as num
            FROM players
        '''
    )
    playerCount = cursor.fetchone()[0]
    db.commit()
    db.close()
    return playerCount


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    cursor.execute("INSERT INTO players (p_name) VALUES (%s)", (name,))
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
    cursor.execute(
        '''
            SELECT
                p_id
                , p_name
                , wins
                , total_matches
            FROM
                standings;
        '''
    )
    results = cursor.fetchall()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Note: Although the matches table schema supports the winner being either
    p1 or p2 this function will always record the winner as p1.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    cursor.execute(
        '''
            INSERT INTO matches
                (p1, p2, m_results) VALUES
                (%s, %s, 1)
            ;
        ''',
        (winner, loser)
    )
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

    # Use views odd_standings and even_standings to generate swiss pairs
    # See this post for original idea behind implementation:
    # https://goo.gl/T1cB6B
    db, cursor = connect()
    cursor.execute('''
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
    ''')
    pairings = cursor.fetchall()
    db.close()
    return pairings
