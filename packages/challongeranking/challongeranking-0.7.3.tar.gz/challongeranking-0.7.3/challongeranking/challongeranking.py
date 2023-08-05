import challonge
import os.path
import sqlite3

# The rating that previously unrated players start at
_newPlayerRating = 1200


def setCredentials(username, apikey):
    challonge.set_credentials(username, apikey)


def processTournament(tournamentName, dbName):
    """Calculate new ratings for a single tournament.

    Goes through all matches of a tournament and calculates changes in
    participant ratings throughout the tournament.

    Arguments:
        tournamentName:
            tournament name (e.g. 'mytournament' if the tournament
            URL is 'challonge.com/mytournament').
            If the tournament is in a sub-domain then the argument should be
            of form 'subdomain-tournament' (e.g. myorganisation-mytournament
            for 'myorganisation.challonge.com/mytournament')

        dbName:
            database filename.
            If the file doesn't exist, it will be created.
    """
    global __playerCache, __ratingCache
    __playerCache = dict()
    __ratingCache = dict()

    if not os.path.exists(dbName):
        db = __createDatabase(dbName)
    else:
        db = sqlite3.connect(dbName)

    # Do not process tournaments that have already been processed
    tournament = challonge.tournaments.show(tournamentName)
    if __findTournament(tournament['id'], db) == True:
        return

    # Do not process tournaments that have not been completed yet
    if tournament['completed-at'] == None:
        return

    players = filter(lambda player: player['email-hash'] is not None,
                     challonge.participants.index(tournament['id']))
    for player in players:
        __playerCache[player['id']] = player
        __updatePlayerName(db, player)
        __addParticipation(db, tournament, player)

    for match in challonge.matches.index(tournament['id']):
        __processMatch(match, db)

    __addTournament(tournament['id'], db)
    db.commit()
    db.close()


def __addParticipation(db, tournament, player):
    c = db.cursor()
    c.execute('INSERT INTO participations VALUES (?,?)',
              (tournament['id'], player['email-hash']))


def __uniqueMatchId(match):
    """ Generate an unique id for a match.
    Arguments:
        match: match object as fetched from challonge API

        Returns ID as an integer
    """
    k1 = match['tournament-id']
    k2 = match['id']
    id = ((k1 + k2) * (k1 + k2 + 1)) / 2 + k2
    return id


def __addMatch(db, match, oldRatings, newRatings):
    """Inserts a match record into the database.
    Arguments:
        db: previously opened database connection
        match: match object as fetched from the challonge API
        old_ratings: Elo ratings for players before playing the match,
                     as a tuple
        new_ratings: Elo ratings for players after playing the match
    """
    c = db.cursor()
    player1EloChange = newRatings[0] - oldRatings[0]
    player2EloChange = newRatings[1] - oldRatings[1]

    player1 = __playerCache[match['player1-id']]
    player2 = __playerCache[match['player2-id']]
    winner = __playerCache[match['winner-id']]

    c.execute('INSERT INTO matches VALUES(?,?,?,?,?,?,?,?,?,?)',
              (__uniqueMatchId(match), match['tournament-id'],
               match['updated-at'],
               player1['email-hash'], player2['email-hash'],
               winner['email-hash'],
               oldRatings[0], oldRatings[1],
               player1EloChange, player2EloChange))


def __processMatch(match, db):
    c = db.cursor()

    if (match['player1-id'] not in __playerCache or
       match['player2-id'] not in __playerCache):
        return

    player1 = __playerCache[match['player1-id']]
    player2 = __playerCache[match['player2-id']]

    if match['winner-id'] == player1['id']:
        winner = 0
    else:
        winner = 1

    player1Rating = __playerRating(player1, db)
    player2Rating = __playerRating(player2, db)

    player1NewRating, player2NewRating = __updateRatings((player1Rating,
                                                         player2Rating),
                                                         winner)
    c.execute('UPDATE players SET rating=? WHERE id=?',
              (player1NewRating, player1['email-hash']))
    c.execute('UPDATE players SET rating=? WHERE id=?',
              (player2NewRating, player2['email-hash']))

    __ratingCache[player1['id']] = player1NewRating
    __ratingCache[player2['id']] = player2NewRating

    __addMatch(db, match, (player1Rating, player2Rating),
               (player1NewRating, player2NewRating))


def __playerRating(player, db):
    """Returns the rating of a player.
    Arguments:
        player = the player as returned by the challonge API
        db = previously opened database connection
    """
    key = player['id']
    if key not in __ratingCache:
        c = db.cursor()
        c.execute('SELECT rating FROM PLAYERS WHERE id=?',
                  (player['email-hash'],))
        rating = c.fetchone()[0]
        __ratingCache[key] = rating
    else:
        rating = __ratingCache[key]

    return rating


def __addTournament(tournamentId, db):
    c = db.cursor()
    c.execute('INSERT INTO tournaments VALUES(?)', (tournamentId,))


def __findTournament(tournamentId, db):
    c = db.cursor()
    c.execute('SELECT id FROM tournaments WHERE id=?', (tournamentId,))

    return c.fetchone() is not None


def __updateRatings(oldRatings, winner):
    """Calculate new ratings for players.

    Args: ratings - tuple of current player ratings before match
    winner - index of the winner's rating
    (i.e. 0 = player1 and 1 = player2)

    Returns a tuple containing new ratings.
    """
    r1, r2 = oldRatings
    R1 = 10 ** (float(r1) / 400)
    R2 = 10 ** (float(r2) / 400)
    E1 = R1 / (R1 + R2)
    E2 = R2 / (R1 + R2)

    S1 = 0
    S2 = 0
    if winner == 0:
        S1 = 1
    else:
        S2 = 1

    K = 32
    player1NewRating = int(round(r1 + K * (S1 - E1)))
    player2NewRating = int(round(r2 + K * (S2 - E2)))

    return (player1NewRating, player2NewRating)


def __updatePlayerName(db, player):
    """Keeps list of names (aliases) used by a player up to date.

    Arguments:
        db - previously opened database connection
        player - the player as returned by challonge API
    """
    c = db.cursor()
    id = player['email-hash']

    if player['name'] is not None:
        playerTournamentName = player['name']
    else:
        playerTournamentName = player['challonge-username']

    c.execute('SELECT id FROM players WHERE id=?', (id,))
    row = c.fetchone()
    if row is None:
        newPlayerRecord = (player['email-hash'],
                           playerTournamentName,
                           _newPlayerRating)
        c.execute('INSERT INTO players VALUES(?,?,?)', newPlayerRecord)
    else:
        c.execute('SELECT nick FROM players WHERE id=?', (id,))
        storedName = c.fetchone()[0]
        if storedName != playerTournamentName:
            c.execute('SELECT alias FROM aliases WHERE player_id=?', (id,))
            if c.fetchone() is None:
                c.execute('INSERT INTO aliases VALUES(?,?)',
                          (playerTournamentName, id))


def __createDatabase(dbName):
    """Sets up a fresh sqlite3 database with the filename dbName.
    Returns a connection to the created database.
    """

    newdb = sqlite3.connect(dbName)
    c = newdb.cursor()

    queries = [
        "CREATE TABLE players(id TEXT PRIMARY KEY, nick TEXT, rating INT)",

        "CREATE TABLE aliases(alias TEXT, player_id TEXT,"
        " FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE)",

        "CREATE TABLE tournaments(id INT PRIMARY KEY)",

        "CREATE TABLE participations(player_id INT, tournament_id INT,"
        " FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE,"
        " FOREIGN KEY(tournament_id) REFERENCES tournaments(id)"
        " ON DELETE CASCADE)",

        "CREATE TABLE matches"
        "(id INT PRIMARY KEY, tournament_id INT,"
        " date INT,"
        " player1_id TEXT, player2_id TEXT, winner_id TEXT,"
        " player1_elo INT, player2_elo INT,"
        " player1_elo_change INT, player2_elo_change INT,"
        " FOREIGN KEY(tournament_id) REFERENCES tournaments(id)"
        "  ON DELETE CASCADE,"
        " FOREIGN KEY(player1_id) REFERENCES players(id),"
        " FOREIGN KEY(player2_id) REFERENCES players(id))"

    ]
    for query in queries:
        c.execute(query)
        newdb.commit()

    return newdb
