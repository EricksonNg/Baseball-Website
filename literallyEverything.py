from os import path, makedirs, system
import statsapi
import datetime
import sqlite3

start = datetime.datetime.now()
suspended = []
gl = sqlite3.connect('2021/Games Logged 2021.db')
g = gl.cursor()
g.execute('create table if not exists "Games Logged" ("Away Team" text, "Home Team" text, Date text, "Game ID" integer, "Away Score" integer, "Home Score" integer, "Innings" integer, "Status" text, "Winning Team" text, "Losing Team" text, "Winning Pitcher" text, "Losing Pitcher" text, "Save Pitcher" text, "Home Probable" text, "Away Probable" text, "Away Team ID" integer, "Home Team ID" integer, "Venue Name" text, "Venue ID" integer)')

def checkGamesLogged(gameID):
    g.execute('select * from "Games Logged" where "Game ID" = ?', (gameID,))
    fetch = g.fetchone()
    if fetch is None:
        return False
    else:
        if 'Suspended' in fetch[7]:
            return fetch[2] # gameDate is returned if the game is a suspended game (so when game is resumed, we can set the gameDate to the original game date
        return True

def everything():
    year = '2021'
    today = datetime.date.today()
    theDayBefore = today - datetime.timedelta(days=2)
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    sched = statsapi.schedule(start_date= theDayBefore, end_date = yesterday)
    for game in sched:
        gameId = game["game_id"]
        gameDate = game["game_date"]
        gameData = statsapi.get('game', {'gamePk': gameId})
        boxscore = gameData['liveData']['boxscore']
        splitDate = gameDate.split("-")
        gameDate = str(int(splitDate[1]))+"/"+splitDate[2]+"/"+splitDate[0][2:4]
        if game['doubleheader'] != 'N':
            gameDate += "(" + str(game["game_num"]) + ")" # adds number to the back of the game date if the game is a part of a doubleheader

        homeId = game["home_id"]
        awayId = game["away_id"]
        homeAbbrev = statsapi.get('team', {'teamId': homeId})['teams'][0]['abbreviation']
        awayAbbrev = statsapi.get('team', {'teamId': awayId})['teams'][0]['abbreviation']

        homeGameDate = gameDate + " vs " + awayAbbrev
        awayGameDate = gameDate + " @ " + homeAbbrev

        if (game['status'] == "Final" or game['status'] == "Game Over" or 'Completed' in game['status']):
            isGameLogged = checkGamesLogged(gameId)
            if isGameLogged is not True:
                if game['game_type'] == "R":
                    if isGameLogged is not False:
                        gameDate = isGameLogged
                    hit(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore)
                    pitch(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore)
                    field(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore)
                    pitchData(game)
                    if isGameLogged is False:
                        g.execute('insert into "Games Logged" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (game['away_name'], game['home_name'], gameDate, gameId, game['away_score'], game['home_score'], game['current_inning'], game['status'], game['winning_team'], game['losing_team'], game['winning_pitcher'], game['losing_pitcher'], game['save_pitcher'], game['home_probable_pitcher'], game['away_probable_pitcher'], game['away_id'], game['home_id'], game['venue_name'], game['venue_id']))
                    else:
                        g.execute('update "Games Logged" set "Away Score" = ?, "Home Score" = ?, "Innings" = ?, "Status" = ?, "Winning Team" = ?, "Losing Team" = ?, "Winning Pitcher" = ?, "Losing Pitcher" = ?, "Save Pitcher" = ? where "Game ID" = ?', (game['away_score'], game['home_score'], game['current_inning'], game['status'], game['winning_team'], game['losing_team'], game['winning_pitcher'], game['losing_pitcher'], game['save_pitcher'], gameId))
                    gl.commit()
                    print("=============================================================")
                else:
                    input("Game type: " + game['game_type'])
            else:
                print(awayAbbrev, "and", homeAbbrev, "stats already added for", homeGameDate)
                print("=============================================================")
        else:
            # gameDate.split(" ")[0] is used to get the date without the opposing team (the opposing team's abbreviation is at the end of gameDate)
            if 'Postponed' in game['status']:
                print(awayAbbrev, "@", homeAbbrev, "on", gameDate.split(" ")[0], "is/was postponed")
            elif 'Suspended' in game['status']:
                print(awayAbbrev, "@", homeAbbrev, "on", gameDate.split(" ")[0], "WAS SUSPENDED")
                # input("Press enter to continue for other teams: ")
                if checkGamesLogged(gameId) is False:
                    g.execute('insert into "Games Logged" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (game['away_name'], game['home_name'], gameDate, gameId, game['away_score'], game['home_score'], game['current_inning'], game['status'], None, None, None, None, None, game['home_probable_pitcher'], game['away_probable_pitcher'], game['away_id'], game['home_id'], game['venue_name'], game['venue_id']))
                    gl.commit()
                    print("Added suspended game to Games Logged")
            else:
                print(awayAbbrev, "@", homeAbbrev, "on", gameDate.split(" ")[0], "hasn't been played (or finished) yet")
            print("=============================================================")

def springTraining2021():
    year = '2021'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    sched = statsapi.schedule(start_date=yesterday, end_date=today)
    for game in sched:
        gameId = game["game_id"]
        gameDate = game["game_date"]
        gameData = statsapi.get('game', {'gamePk': gameId})
        boxscore = gameData['liveData']['boxscore']
        if game['doubleheader'] != 'N':
            gameDate = game["game_date"] + "(" + str(game["game_num"]) + ")"  # adds number to the back of the game date if the game is a part of a doubleheader

        homeId = game["home_id"]
        awayId = game["away_id"]
        homeAbbrev = statsapi.get('team', {'teamId': homeId})['teams'][0]['abbreviation']
        awayAbbrev = statsapi.get('team', {'teamId': awayId})['teams'][0]['abbreviation']

        homeGameDate = gameDate + " vs. " + awayAbbrev
        awayGameDate = gameDate + " @ " + homeAbbrev

        if game['game_type'] == "S":
            createDir("ST", homeAbbrev, year)  # if needed
            createDir("ST", awayAbbrev, year)  # if needed

            hit(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "ST")
            pitch(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "ST")
            field(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "ST")
        else:
            input("Game type: " + game['game_type'])

def everything2019():
    year = '2019'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    sched = statsapi.schedule(start_date= '03/28/2019', end_date = '09/29/2019')
    for game in sched:
        gameId = game["game_id"]
        gameDate = game["game_date"]
        dateYear, dateMonth, dateDay = gameDate.split("-")
        gameDate = dateMonth+"-"+dateDay+"-"+dateYear
        gameData = statsapi.get('game', {'gamePk': gameId})
        boxscore = gameData['liveData']['boxscore']
        if game['doubleheader'] != 'N':
            gameDate = game["game_date"] + "(" + str(game["game_num"]) + ")" # adds number to the back of the game date if the game is a part of a doubleheader

        homeId = game["home_id"]
        awayId = game["away_id"]
        homeAbbrev = statsapi.get('team', {'teamId': homeId})['teams'][0]['abbreviation']
        awayAbbrev = statsapi.get('team', {'teamId': awayId})['teams'][0]['abbreviation']

        homeGameDate = gameDate + " vs. " + awayAbbrev
        awayGameDate = gameDate + " @ " + homeAbbrev

        if game['game_type'] == "R":
            createDir("Teams",homeAbbrev, year) #if needed
            createDir("Teams",awayAbbrev, year) #if needed

            hit(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
            pitch(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
            field(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
        else:
            input("Game type: "+ game['game_type'])

def everything2020():
    year = '2020'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=2)
    tomorrow = today + datetime.timedelta(days=1)
    sched = statsapi.schedule(start_date= '07/23/2020', end_date = '09/27/2020')
    for game in sched:
        skip = False
        gameId = game["game_id"]
        gameDate = game["game_date"]
        if gameId == 630882:
            if gameDate == '2020-08-14':
                skip = True
        gameData = statsapi.get('game', {'gamePk': gameId})
        boxscore = gameData['liveData']['boxscore']
        splitDate = gameDate.split("-")
        gameDate = str(int(splitDate[1]))+"/"+splitDate[2]+"/"+splitDate[0][2:4]
        if game['doubleheader'] != 'N':
            gameDate += "(" + str(game["game_num"]) + ")" # adds number to the back of the game date if the game is a part of a doubleheader

        homeId = game["home_id"]
        awayId = game["away_id"]
        homeAbbrev = statsapi.get('team', {'teamId': homeId})['teams'][0]['abbreviation']
        awayAbbrev = statsapi.get('team', {'teamId': awayId})['teams'][0]['abbreviation']

        homeGameDate = gameDate + " vs " + awayAbbrev
        awayGameDate = gameDate + " @ " + homeAbbrev

        if game['game_type'] == "R" and skip == False:

            # hit(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
            pitch(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
            # field(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore, "Teams")
        else:
            print(game)
            print("Is this the suspended game?")
            input("Game type: " + game['game_type'])

def createDir(directory, teamAbbrev, year):
    if path.exists(directory+"/" + teamAbbrev + "/" + year):
        # print(year + " " + teamAbbrev + " directory exists")
        pass
    else:
        makedirs(directory+"/" + teamAbbrev + "/" + year)
        # print(year + " " + teamAbbrev + " directory created")

def hit(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore):

    conn = sqlite3.connect('2021/Hitting 2021.db')
    c = conn.cursor()

    try:
        c.execute(""" CREATE TABLE 'Season Hitting' (
            Name text,
            'Player ID' integer,
            Team text,
            Date text,
            'Game ID' integer,
            AVG float,
            Hits integer,
            OBP float, 
            SLG float,
            OPS float,
            BABIP float,
            '2B' integer,
            '3B' integer, 
            HR integer, 
            XBH integer,
            ISO float,
            RBI integer, 
            Runs integer, 
            Strikeouts integer,
            'K%' float,
            Walks integer,
            'BB%' float,
            HBP integer,
            SB integer,
            CS integer,
            'SB%' float,
            TB integer,
            LOB integer,
            PA integer,
            AB integer, 
            'AB/HR' float,
            IBB integer,
            'Sac Flies' integer,
            'Ground Outs' integer,
            'Fly Outs' integer,
            'Double Plays' integer,
            'Triple Plays' integer,
            'Sac Bunts' integer,
            Pickoffs integer,
            CI integer
        )""")
    except Exception as e:
        pass

    try:
        c.execute(""" CREATE TABLE 'Per Game Hitting' (
            Name text,
            'Player ID' integer,
            Team text,
            Date text,
            'Game ID' integer,
            Hits integer,
            AB integer, 
            PA integer,
            RBI integer, 
            Runs integer, 
            Strikeouts integer,
            Walks integer,
            '2B' integer,
            '3B' integer, 
            HR integer, 
            XBH integer,
            TB integer,
            LOB integer,
            HBP integer,
            SB integer,
            CS integer,
            'SB%' float,
            IBB integer,
            'Sac Flies' integer,
            'Ground Outs' integer,
            'Fly Outs' integer,
            'Double Plays' integer,
            'Triple Plays' integer,
            'Sac Bunts' integer,
            Pickoffs integer,
            CI integer
        )""")
    except Exception as e:
        pass

    def findLastFlyOut(teamAbbrev, playername, year):
        c.execute('select "Fly Outs", Date from "Season Hitting" where name = ? order by Date DESC', (playername,))
        category = c.fetchone()
        if category == None:
            return 0
        return category[0]

    def add(homeOrAway, gameDate, boxscore, ID, teamAbbrev, year):
        index = boxscore['teams'][homeOrAway]['players'][ID]
        playername = index['person']['fullName']
        numberID = int(ID.split("ID")[1]) # ID is split at "ID" and indexed at 1 to get the number value of ID (Player ID is an integer in the table)
        c.execute('select * from "Season Hitting" where "Player ID" = ? and Date = ?', (numberID, gameDate))
        if c.fetchone() == None:
            print(playername, gameDate)
            perGameStats = index['stats']['batting']
            seasonStats = index['seasonStats']['batting']
            # progressive
            p_flyOuts = findLastFlyOut(teamAbbrev, playername, year) + int(perGameStats['flyOuts'])
            p_groundOuts = int(seasonStats['groundOuts'])
            p_runs = int(seasonStats['runs'])
            p_doubles = int(seasonStats['doubles'])
            p_triples = int(seasonStats['triples'])
            p_homeRuns = int(seasonStats['homeRuns'])
            p_strikeOuts = int(seasonStats['strikeOuts'])
            p_baseOnBalls = int(seasonStats['baseOnBalls'])
            p_intentionalWalks = int(seasonStats['intentionalWalks'])
            p_hits = int(seasonStats['hits'])
            p_hitByPitch = int(seasonStats['hitByPitch'])
            p_avg = float(seasonStats['avg'])
            p_atBats = int(seasonStats['atBats'])
            p_obp = float(seasonStats['obp'])
            p_slg = float(seasonStats['slg'])
            p_ops = float(seasonStats['ops'])
            p_caughtStealing = int(seasonStats['caughtStealing'])
            p_stolenBases = int(seasonStats['stolenBases'])
            try:
                p_stolenBasePercentage = float(seasonStats['stolenBasePercentage'])
            except ValueError:
                p_stolenBasePercentage = 0.000
            p_groundIntoDoublePlay = int(seasonStats['groundIntoDoublePlay'])
            p_groundIntoTriplePlay = int(seasonStats['groundIntoTriplePlay'])
            p_plateAppearances = int(seasonStats['plateAppearances'])
            p_totalBases = int(seasonStats['totalBases'])
            p_rbi = int(seasonStats['rbi'])
            p_leftOnBase = int(seasonStats['leftOnBase'])
            p_sacBunts = int(seasonStats['sacBunts'])
            p_sacFlies = int(seasonStats['sacFlies'])
            try:
                p_babip = float(seasonStats['babip'])
            except ValueError:
                p_babip = .000
            p_catchersInterference = int(seasonStats['catchersInterference'])
            p_pickoffs = int(seasonStats['pickoffs'])
            try:
                p_atBatsPerHomeRun = float(seasonStats['atBatsPerHomeRun'])
            except ValueError:
                p_atBatsPerHomeRun = 0.00
            p_iso = round(p_slg - p_avg, 3)
            p_extraBaseHits = p_doubles+p_triples+p_homeRuns
            try:
                p_strikeOutPercentage = round(p_strikeOuts/p_plateAppearances, 3)
            except ZeroDivisionError:
                p_strikeOutPercentage = 0.00
            try:
                p_walkPercentage = round((p_baseOnBalls+p_intentionalWalks)/p_plateAppearances, 3)
            except ZeroDivisionError:
                p_walkPercentage = (p_baseOnBalls+p_intentionalWalks) * 1.000

            # ID is split at "ID" and indexed at 1 to get the number value of ID
            progressive.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], p_avg, p_hits, p_obp, p_slg, p_ops, p_babip, p_doubles, p_triples, p_homeRuns, p_extraBaseHits, p_iso, p_rbi, p_runs, p_strikeOuts, p_strikeOutPercentage, p_baseOnBalls, p_walkPercentage, p_hitByPitch, p_stolenBases, p_caughtStealing, p_stolenBasePercentage, p_totalBases, p_leftOnBase, p_plateAppearances, p_atBats, p_atBatsPerHomeRun, p_intentionalWalks, p_sacFlies, p_groundOuts, p_flyOuts, p_groundIntoDoublePlay, p_groundIntoTriplePlay, p_sacBunts, p_pickoffs, p_catchersInterference))
        c.execute('select * from "Per Game Hitting" where "Player ID" = ? and Date = ?', (numberID, gameDate))
        if c.fetchone() == None:
            perGameStats = index['stats']['batting']
            # per game
            pg_flyOuts = int(perGameStats['flyOuts'])
            pg_groundOuts = int(perGameStats['groundOuts'])
            pg_runs = int(perGameStats['runs'])
            pg_doubles = int(perGameStats['doubles'])
            pg_triples = int(perGameStats['triples'])
            pg_homeRuns = int(perGameStats['homeRuns'])
            pg_strikeOuts = int(perGameStats['strikeOuts'])
            pg_baseOnBalls = int(perGameStats['baseOnBalls'])
            pg_intentionalWalks = int(perGameStats['intentionalWalks'])
            pg_hits = int(perGameStats['hits'])
            pg_hitByPitch = int(perGameStats['hitByPitch'])
            pg_atBats = int(perGameStats['atBats'])
            pg_caughtStealing = int(perGameStats['caughtStealing'])
            pg_stolenBases = int(perGameStats['stolenBases'])
            try:
                pg_stolenBasePercentage = float(perGameStats['stolenBasePercentage'])
            except ValueError:
                pg_stolenBasePercentage = 0.000
            pg_groundIntoDoublePlay = int(perGameStats['groundIntoDoublePlay'])
            pg_groundIntoTriplePlay = int(perGameStats['groundIntoTriplePlay'])
            pg_plateAppearances = int(perGameStats['plateAppearances'])
            pg_totalBases = int(perGameStats['totalBases'])
            pg_rbi = int(perGameStats['rbi'])
            pg_leftOnBase = int(perGameStats['leftOnBase'])
            pg_sacBunts = int(perGameStats['sacBunts'])
            pg_sacFlies = int(perGameStats['sacFlies'])
            pg_catchersInterference = int(perGameStats['catchersInterference'])
            pg_pickoffs = int(perGameStats['pickoffs'])
            try:
                pg_atBatsPerHomeRun = float(perGameStats['atBatsPerHomeRun'])
            except ValueError:
                pg_atBatsPerHomeRun = 0.00
            pg_extraBaseHits = pg_doubles+pg_triples+pg_homeRuns

            perGame.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], pg_hits, pg_atBats, pg_plateAppearances, pg_rbi, pg_runs, pg_strikeOuts, pg_baseOnBalls, pg_doubles, pg_triples, pg_homeRuns, pg_extraBaseHits, pg_totalBases, pg_leftOnBase, pg_hitByPitch, pg_stolenBases, pg_caughtStealing, pg_stolenBasePercentage, pg_intentionalWalks, pg_sacFlies, pg_groundOuts, pg_flyOuts, pg_groundIntoDoublePlay, pg_groundIntoTriplePlay, pg_sacBunts, pg_pickoffs, pg_catchersInterference))
        playerInfo(numberID, teamAbbrev, game)

    progressive = []
    perGame = []

    awayPlayers = boxscore['teams']['away']['players']
    homePlayers = boxscore['teams']['home']['players']

    if homeAbbrev not in suspended:
        for ID in homePlayers:
            if homePlayers[ID]['stats']['batting'] != {}:
                add('home', homeGameDate, boxscore, ID, homeAbbrev, year)
    if awayAbbrev not in suspended:
        for ID in awayPlayers:
            if awayPlayers[ID]['stats']['batting'] != {}:
                add('away', awayGameDate, boxscore, ID, awayAbbrev, year)

    c.executemany("insert into 'Season Hitting' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", progressive)
    c.executemany("insert into 'Per Game Hitting' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", perGame)

    conn.commit()
    conn.close()

    if len(progressive) == 0:
        print(awayAbbrev, "and", homeAbbrev, "season hitting stats already added for", homeGameDate)
    if len(perGame) == 0:
        print(awayAbbrev, "and", homeAbbrev, "per game hitting stats already added for", homeGameDate)

def pitch(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore):

    conn = sqlite3.connect('2021/Pitching 2021.db')
    c = conn.cursor()

    try:
        c.execute(""" CREATE TABLE 'Season Pitching' (
                Name text,
                'Player ID' integer,
                Team text,
                Date text,
                'Game ID' integer,
                'GS' integer,
                'G' integer,
                'Wins' integer,
                'Losses' integer,
                'Win%' float,
                'ERA' float,
                'Pitches' integer,
                'Balls' integer,
                'Strikes' integer,
                'IP' float,
                'ER' integer,
                'Runs' integer,
                'Hits' integer,
                '2B' integer,
                '3B' integer,
                'HR' integer,
                'Strikeouts' integer,
                'Walks' integer,
                'K/BB' float,
                'BAA' float,
                'OBP' float,
                'K%' float,
                'Pitches/IP' float,
                'WHIP' float,
                'Strike%' float,
                'IR' integer,
                'IRS' integer,
                'Games Finished' integer,
                'Saves' integer,
                'Save Opp.' integer,
                'Blown Saves' integer,
                'Holds' integer,
                'CG' integer,
                'Shutouts' integer,
                'IBB' integer,
                'HBP' integer,
                'AB' integer,
                'Batters Faced' integer,
                'Outs' integer,
                'Ground Outs' integer,
                'Air Outs' integer,
                'GO/AO' float,
                'SB' integer,
                'CS' integer,
                'SB%' integer,
                'Balks' integer,
                'Pickoffs' integer,
                'WP' integer, 
                'RBI' integer,
                'CI' integer,
                'Sac Bunts' integer,
                'Sac Flies' integer,
                'Hits Per 9' float,
                'Runs Per 9' float,
                'HR Per 9' float,
                'Strikeouts Per 9' float,
                'Walks Per 9' float
            )""")
    except Exception as e:
        pass

    try:
        c.execute(""" CREATE TABLE 'Per Game Pitching' (
                Name text,
                'Player ID' integer,
                Team text,
                Date text,
                'Game ID' integer,
                'GS' integer,
                'Wins' integer,
                'Losses' integer,
                'Pitches' integer,
                'Balls' integer,
                'Strikes' integer,
                'IP' float,
                'ER' integer,
                'Runs' integer,
                'Hits' integer,
                '2B' integer,
                '3B' integer,
                'HR' integer,
                'Strikeouts' integer,
                'Walks' integer,
                'BAA' float,
                'Pitches/IP' float,
                'WHIP' float,
                'Strike%' float,
                'IR' integer,
                'IRS' integer,
                'Games Finished' integer,
                'Saves' integer,
                'Save Opp.' integer,
                'Blown Saves' integer,
                'Holds' integer,
                'CG' integer,
                'Shutouts' integer,
                'IBB' integer,
                'HBP' integer,
                'AB' integer,
                'Batters Faced' integer,
                'Outs' integer,
                'Ground Outs' integer,
                'Air Outs' integer,
                'SB' integer,
                'CS' integer,
                'SB%' integer,
                'Balks' integer,
                'Pickoffs' integer,
                'WP' integer, 
                'RBI' integer,
                'CI' integer,
                'Sac Bunts' integer,
                'Sac Flies' integer,
                'Hits Per 9' float,
                'Runs Per 9' float,
                'HR Per 9' float,
                'Strikeouts Per 9' float,
                'Walks Per 9' float
            )""")
    except Exception as e:
        pass

    def findLast(teamAbbrev, playername, year, category):
        c.execute('select "SB%", "Balls", "Strikes", "Batters Faced", "Pitches", "RBI" Date from "Season Pitching" where name = ? order by Date DESC', (playername,))
        fetch = c.fetchone()
        if fetch == None:
            return 0
        else:
            categories = {'p_stolenBasePercentage': fetch[0], 'p_balls': fetch[1], 'p_strikes': fetch[2], 'p_battersFaced': fetch[3], 'p_numberOfPitches': fetch[4], 'p_rbi': fetch[5]}
            return categories[category]

    def add(homeOrAway, gameDate, boxscore, ID, teamAbbrev, year):
        index = boxscore['teams'][homeOrAway]['players'][ID]
        playername = index['person']['fullName']
        numberID = int(ID.split("ID")[1]) # ID is split at "ID" and indexed at 1 to get the number value of ID (Player ID is an integer in the table)
        perGameStats = index['stats']['pitching']
        seasonStats = index['seasonStats']['pitching']
        if perGameStats['numberOfPitches'] != 0:
            # per game
            c.execute('select * from "Season Pitching" where "Player ID" = ? and Date = ?', (numberID, gameDate))
            if c.fetchone() == None:
                print(playername, gameDate)
                pg_gamesStarted = int(perGameStats['gamesStarted'])
                pg_groundOuts = int(perGameStats['groundOuts'])
                pg_airOuts = int(perGameStats['airOuts'])
                pg_runs = int(perGameStats['runs'])
                pg_doubles = int(perGameStats['doubles'])
                pg_triples = int(perGameStats['triples'])
                pg_homeRuns = int(perGameStats['homeRuns'])
                pg_strikeOuts = int(perGameStats['strikeOuts'])
                pg_baseOnBalls = int(perGameStats['baseOnBalls'])
                pg_intentionalWalks = int(perGameStats['intentionalWalks'])
                pg_hits = int(perGameStats['hits'])
                pg_hitByPitch = int(perGameStats['hitByPitch'])
                pg_atBats = int(perGameStats['atBats'])
                pg_caughtStealing = int(perGameStats['caughtStealing'])
                pg_stolenBases = int(perGameStats['stolenBases'])
                try:
                    pg_stolenBasePercentage = float(perGameStats['stolenBasePercentage'])
                except ValueError: # if value is a string instead of a number value
                    pg_stolenBasePercentage = 0.000
                pg_numberOfPitches = int(perGameStats['numberOfPitches'])
                if pg_numberOfPitches == 0:
                    input(playername + " has no pitches!")
                pg_inningsPitched = float(perGameStats['inningsPitched'])
                if ".1" in str(pg_inningsPitched):
                    pg_inningsPitched = int(pg_inningsPitched) + 0.33
                if ".2" in str(pg_inningsPitched):
                    pg_inningsPitched = int(pg_inningsPitched) + 0.67
                try:
                    pg_whip = round(((pg_hits + pg_hitByPitch + pg_baseOnBalls + pg_intentionalWalks)/pg_inningsPitched),2)
                except ZeroDivisionError:
                    pg_whip = float(pg_hits + pg_hitByPitch + pg_baseOnBalls + pg_intentionalWalks)
                pg_wins = int(perGameStats['wins'])
                pg_losses = int(perGameStats['losses'])
                pg_saves = int(perGameStats['saves'])
                pg_saveOpportunities = int(perGameStats['saveOpportunities'])
                pg_holds = int(perGameStats['holds'])
                pg_blownSaves = int(perGameStats['blownSaves'])
                pg_earnedRuns = int(perGameStats['earnedRuns'])
                pg_battersFaced = int(perGameStats['battersFaced'])
                pg_outs = int(perGameStats['outs'])
                pg_completeGames = int(perGameStats['completeGames'])
                pg_shutouts = int(perGameStats['shutouts'])
                pg_balls = int(perGameStats['balls'])
                pg_strikes = int(perGameStats['strikes'])
                try:
                    pg_strikePercentage = float(perGameStats['strikePercentage'])
                except ValueError:
                    pg_strikePercentage = 0.000
                pg_balks = int(perGameStats['balks'])
                pg_wildPitches = int(perGameStats['wildPitches'])
                pg_pickoffs = int(perGameStats['pickoffs'])
                pg_rbi = int(perGameStats['rbi'])
                pg_gamesFinished = int(perGameStats['gamesFinished'])
                try:
                    pg_runsScoredPer9 = float(perGameStats['runsScoredPer9'])
                except ValueError:
                    pg_runsScoredPer9 = float(perGameStats['runs'])*27
                try:
                    pg_homeRunsPer9 = float(perGameStats['homeRunsPer9'])
                except ValueError:
                    pg_homeRunsPer9 = float(perGameStats['homeRuns'])*27
                try:
                    pg_strikeOutsPer9 = round(((9/pg_inningsPitched)*pg_strikeOuts),2)
                except ZeroDivisionError:
                    pg_strikeOutsPer9 = float(pg_strikeOuts)*27
                try:
                    pg_walksPer9 = round(((9/pg_inningsPitched)*pg_baseOnBalls), 2)
                except ZeroDivisionError:
                    pg_walksPer9 = float(pg_baseOnBalls*27)
                try:
                    pg_hitsPer9 = round(((9/pg_inningsPitched)*pg_hits),2)
                except ZeroDivisionError:
                    pg_hitsPer9 = float(pg_hits)*27

                pg_inheritedRunners = int(perGameStats['inheritedRunners'])
                if pg_inheritedRunners > 0:
                    print("Inherited Runners is actually greater than 0 at", pg_inheritedRunners, "for", playername)

                pg_inheritedRunnersScored = int(perGameStats['inheritedRunnersScored'])
                pg_catchersInterference = int(perGameStats['catchersInterference'])
                pg_sacBunts = int(perGameStats['sacBunts'])
                pg_sacFlies = int(perGameStats['sacFlies'])
                try:
                    pg_pitchesPerInning = float(seasonStats['pitchesPerInning'])
                except ValueError:
                    pg_pitchesPerInning = float(pg_numberOfPitches)  # Pitches per inning in seasonStats gives the pitches per innings for the pitcher for that one game (it's a per game average, not a season average)
                try:
                    pg_battingAverageAgainst = round(pg_hits/pg_atBats, 3)
                except ZeroDivisionError:
                    pg_battingAverageAgainst = 0.000

                perGame.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], pg_gamesStarted, pg_wins, pg_losses, pg_numberOfPitches, pg_balls, pg_strikes, pg_inningsPitched, pg_earnedRuns, pg_runs, pg_hits, pg_doubles, pg_triples, pg_homeRuns, pg_strikeOuts, pg_baseOnBalls, pg_battingAverageAgainst, pg_pitchesPerInning, pg_whip, pg_strikePercentage, pg_inheritedRunners, pg_inheritedRunnersScored, pg_gamesFinished, pg_saves, pg_saveOpportunities, pg_blownSaves, pg_holds, pg_completeGames, pg_shutouts, pg_intentionalWalks, pg_hitByPitch, pg_atBats, pg_battersFaced, pg_outs, pg_groundOuts, pg_airOuts, pg_stolenBases, pg_caughtStealing, pg_stolenBasePercentage, pg_balks, pg_pickoffs, pg_wildPitches, pg_rbi, pg_catchersInterference, pg_sacBunts, pg_sacFlies, pg_hitsPer9, pg_runsScoredPer9, pg_homeRunsPer9, pg_strikeOutsPer9, pg_walksPer9))
            # progressive
            c.execute('select * from "Per Game Pitching" where "Player ID" = ? and Date = ?', (numberID, gameDate))
            if c.fetchone() == None:
                p_gamesPlayed = int(seasonStats['gamesPlayed'])
                p_gamesStarted = int(seasonStats['gamesStarted'])
                p_groundOuts = int(seasonStats['groundOuts'])
                p_airOuts = int(seasonStats['airOuts'])
                p_runs = int(seasonStats['runs'])
                p_doubles = int(seasonStats['doubles'])
                p_triples = int(seasonStats['triples'])
                p_homeRuns = int(seasonStats['homeRuns'])
                p_strikeOuts = int(seasonStats['strikeOuts'])
                p_baseOnBalls = int(seasonStats['baseOnBalls'])
                p_intentionalWalks = int(seasonStats['intentionalWalks'])
                p_hits = int(seasonStats['hits'])
                p_hitByPitch = int(seasonStats['hitByPitch'])
                p_atBats = int(seasonStats['atBats'])
                p_obp = float(seasonStats['obp'])
                p_caughtStealing = int(seasonStats['caughtStealing'])
                p_stolenBases = int(seasonStats['stolenBases'])
                try:
                    p_stolenBasePercentage = float(seasonStats['stolenBasePercentage'])
                except ValueError:
                    p_stolenBasePercentage = float(findLast(teamAbbrev, playername, year, 'p_stolenBasePercentage'))
                p_earnedRuns = int(seasonStats['earnedRuns']) # p_earnRuns has to be put above p_era to use in the calculation of p_era if there is a ValueError
                try:
                    p_era = float(seasonStats['era'])
                except ValueError:
                    p_era = pg_earnedRuns*27
                p_inningsPitched = float(seasonStats['inningsPitched'])
                if ".1" in str(p_inningsPitched):
                    p_inningsPitched = int(p_inningsPitched) + 0.33
                if ".2" in str(p_inningsPitched):
                    p_inningsPitched = int(p_inningsPitched) + 0.67
                p_wins = int(seasonStats['wins'])
                p_losses = int(seasonStats['losses'])
                p_saves = int(seasonStats['saves'])
                p_saveOpportunities = int(seasonStats['saveOpportunities'])
                p_holds = int(seasonStats['holds'])
                p_blownSaves = int(seasonStats['blownSaves'])
                try:
                    p_whip = float(seasonStats['whip'])
                except ValueError:
                    p_whip = float(p_hits + p_hitByPitch + p_baseOnBalls + p_intentionalWalks)
                p_battersFaced = findLast(teamAbbrev, playername, year, 'p_battersFaced') + pg_battersFaced
                p_outs = int(seasonStats['outs'])
                p_completeGames = int(seasonStats['completeGames'])
                p_shutouts = int(seasonStats['shutouts'])

                try:
                    p_balls = findLast(teamAbbrev, playername, year, "p_balls") + pg_balls
                except Exception:
                    input("Something is wrong with p_balls")
                try:
                    p_strikes = findLast(teamAbbrev, playername, year, "p_strikes") + pg_strikes
                except Exception:
                    input("Something is wrong with p_strikes")
                try:
                    p_numberOfPitches = findLast(teamAbbrev, playername, year, "p_numberOfPitches") + pg_numberOfPitches
                except Exception:
                    input("Something is wrong with p_numberOfPitches")
                try:
                    p_strikePercentage = round(p_strikes/p_numberOfPitches,3)
                except Exception:
                    input("Something is wrong with p_strikePercentage")
                try:
                    p_pitchesPerInning = round((p_numberOfPitches/p_inningsPitched), 2)
                except ZeroDivisionError:
                    p_pitchesPerInning = float(pg_numberOfPitches)

                p_balks = int(seasonStats['balks'])
                p_wildPitches = int(seasonStats['wildPitches'])
                p_pickoffs = int(seasonStats['pickoffs'])
                try:
                    p_groundOutsToAirouts = float(seasonStats['groundOutsToAirouts'])
                except ValueError:
                    if p_groundOuts == 0 and p_airOuts == 0:
                        p_groundOutsToAirouts = 0.00
                    elif p_airOuts == 0:
                        p_groundOutsToAirouts = float(p_groundOuts)
                    elif p_groundOuts == 0:
                        p_groundOutsToAirouts = 1.0/p_airOuts
                try:
                    p_rbi = findLast(teamAbbrev, playername, year, 'p_rbi') + pg_rbi
                except Exception:
                    input("Something is wrong with p_rbi")
                try:
                    p_winPercentage = float(seasonStats['winPercentage'])
                except ValueError:
                    if p_wins == 0:
                        p_winPercentage = 0.00
                    else:
                        input("We have a problem")
                p_gamesFinished = int(seasonStats['gamesFinished'])
                try:
                    p_strikeoutWalkRatio = float(seasonStats['strikeoutWalkRatio'])
                except ValueError:
                    if p_strikeOuts == 0 and p_baseOnBalls == 0:
                        p_strikeoutWalkRatio = 0.00
                    elif p_baseOnBalls == 0:
                        p_strikeoutWalkRatio = float(p_strikeOuts)
                    elif p_strikeOuts == 0:
                        p_strikeoutWalkRatio = 1.0/p_baseOnBalls
                try:
                    p_strikeoutsPer9Inn = float(seasonStats['strikeoutsPer9Inn'])
                except ValueError:
                    p_strikeoutsPer9Inn = float(pg_strikeOuts)*27 # Relates to pg_strikeOutsPer9
                try:
                    p_walksPer9Inn = float(seasonStats['walksPer9Inn'])
                except ValueError:
                    p_walksPer9Inn = float(pg_baseOnBalls)*27 # Relates to pg_walksPer9
                try:
                    p_hitsPer9Inn = float(seasonStats['hitsPer9Inn'])
                except ValueError:
                    p_hitsPer9Inn = float(pg_hits)*27 # Relates to pg_hitsPer9
                try:
                    p_runsScoredPer9 = float(seasonStats['runsScoredPer9'])
                except ValueError:
                    p_runsScoredPer9 = float(pg_runs)*27
                try:
                    p_homeRunsPer9 = float(seasonStats['homeRunsPer9'])
                except ValueError:
                    p_homeRunsPer9 = float(pg_homeRuns)*27
                p_inheritedRunners = int(seasonStats['inheritedRunners'])
                p_inheritedRunnersScored = int(seasonStats['inheritedRunnersScored'])
                p_catchersInterference = int(seasonStats['catchersInterference'])
                p_sacBunts = int(seasonStats['sacBunts'])
                p_sacFlies = int(seasonStats['sacFlies'])
                try:
                    p_battingAverageAgainst = round(p_hits/p_atBats, 3)
                except ZeroDivisionError:
                    p_battingAverageAgainst = 0.000
                p_strikeOutPercentage = round(p_strikeOuts/p_battersFaced, 3)

                progressive.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], p_gamesStarted, p_gamesPlayed, p_wins, p_losses, p_winPercentage, p_era, p_numberOfPitches, p_balls, p_strikes, p_inningsPitched, p_earnedRuns, p_runs, p_hits, p_doubles, p_triples, p_homeRuns, p_strikeOuts, p_baseOnBalls, p_strikeoutWalkRatio, p_battingAverageAgainst, p_obp, p_strikeOutPercentage, p_pitchesPerInning, p_whip, p_strikePercentage, p_inheritedRunners, p_inheritedRunnersScored, p_gamesFinished, p_saves, p_saveOpportunities, p_blownSaves, p_holds, p_completeGames, p_shutouts, p_intentionalWalks, p_hitByPitch, p_atBats, p_battersFaced, p_outs, p_groundOuts, p_airOuts, p_groundOutsToAirouts, p_stolenBases, p_caughtStealing, p_stolenBasePercentage, p_balks, p_pickoffs, p_wildPitches, p_rbi, p_catchersInterference, p_sacBunts, p_sacFlies, p_hitsPer9Inn, p_runsScoredPer9, p_homeRunsPer9, p_strikeoutsPer9Inn, p_walksPer9Inn))
            playerInfo(numberID, teamAbbrev, game)

    progressive = []
    perGame = []

    awayPlayers = boxscore['teams']['away']['players']
    homePlayers = boxscore['teams']['home']['players']

    if homeAbbrev not in suspended:
        for ID in homePlayers:
            if homePlayers[ID]['stats']['pitching'] != {}:
                add('home', homeGameDate, boxscore, ID, homeAbbrev, year)
    if awayAbbrev not in suspended:
        for ID in awayPlayers:
            if awayPlayers[ID]['stats']['pitching'] != {}:
                add('away', awayGameDate, boxscore, ID, awayAbbrev, year)

    c.executemany("insert into 'Season Pitching' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", progressive)
    c.executemany("insert into 'Per Game Pitching' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", perGame)

    conn.commit()
    conn.close()

    if len(progressive) == 0:
        print(awayAbbrev, "and", homeAbbrev, "season pitching stats already added for", homeGameDate)
    if len(perGame) == 0:
        print(awayAbbrev, "and", homeAbbrev, "per game pitching stats already added for", homeGameDate)

def field(homeAbbrev, awayAbbrev, year, homeGameDate, awayGameDate, game, boxscore):

    conn = sqlite3.connect('2021/Fielding 2021.db')
    c = conn.cursor()

    try:
        c.execute(""" CREATE TABLE 'Season Fielding' (
                Name text,
                'Player ID' integer,
                Team text,
                Date text,
                'Game ID' integer,
                'GS' integer,
                Assists integer,
                Putouts integer,
                Chances integer,
                Errors integer,
                'Fielding%' float,
                'Passed Balls' integer,
                'CS' integer,
                'SB' integer,
                'SB%' float,
                Pickoffs integer
            )""")
    except Exception as e:
        pass

    try:
        c.execute(""" CREATE TABLE 'Per Game Fielding' (
                Name text,
                'Player ID' integer,
                Team text,
                Date text,
                'Game ID' integer, 
                'Positions' text,
                'GS' integer,
                Assists integer, 
                Putouts integer,
                Chances integer,
                Errors integer, 
                'Passed Balls' integer,
                'CS' integer,
                'SB' integer, 
                'SB%' float,
                Pickoffs integer
            )""")
    except Exception as e:
        pass

    def findLastGameStart(teamAbbrev, playername, year):
        c.execute('select "GS", Date from "Season Fielding" where name = ? order by Date DESC', (playername,))
        category = c.fetchone()
        if category == None:
            return 0
        return category[0]

    def add(homeOrAway, gameDate, boxscore, ID, teamAbbrev, year):
        index = boxscore['teams'][homeOrAway]['players'][ID]
        playername = index['person']['fullName']
        numberID = int(ID.split("ID")[1]) # ID is split at "ID" and indexed at 1 to get the number value of ID (Player ID is an integer in the table)
        c.execute('select * from "Per Game Fielding" where "Player ID" = ? and Date = ?', (numberID, gameDate))
        if c.fetchone() == None:
            print(playername, gameDate)
            perGameStats = index['stats']['fielding']
            # per game (placed above progressive so p_gamesStarted can get value of pg_gamesStarted)
            pg_assists = int(perGameStats['assists'])
            pg_putOuts = int(perGameStats['putOuts'])
            pg_errors = int(perGameStats['errors'])
            pg_chances = int(perGameStats['chances'])
            pg_caughtStealing = int(perGameStats['caughtStealing'])
            pg_passedBall = int(perGameStats['passedBall'])
            try:
                pg_gamesStarted = int(perGameStats['gamesStarted'])
            except KeyError:
                pg_gamesStarted = 0
            pg_stolenBases = int(perGameStats['stolenBases'])
            try:
                pg_stolenBasePercentage = float(perGameStats['stolenBasePercentage'])
            except ValueError:
                pg_stolenBasePercentage = 0.000
            pg_pickoffs = int(perGameStats['pickoffs'])
            position = index['allPositions'][0]['abbreviation']
            if len(index['allPositions']) > 1:
                for i in range(1, len(index['allPositions'])):
                    position += "-" + index['allPositions'][i]['abbreviation']

            perGame.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], position, pg_gamesStarted, pg_assists, pg_putOuts, pg_chances, pg_errors, pg_passedBall, pg_caughtStealing, pg_stolenBases, pg_stolenBasePercentage, pg_pickoffs))
        c.execute('select * from "Season Fielding" where "Player ID" = ? and Date = ?', (numberID, gameDate))
        if c.fetchone() == None:
            # progressive
            seasonStats = index['seasonStats']['fielding']
            p_assists = int(seasonStats['assists'])
            p_putOuts = int(seasonStats['putOuts'])
            p_errors = int(seasonStats['errors'])
            p_chances = int(seasonStats['chances'])
            p_fielding = float(seasonStats['fielding'])
            p_caughtStealing = int(seasonStats['caughtStealing'])
            p_passedBall = int(seasonStats['passedBall'])
            p_gamesStarted = findLastGameStart(teamAbbrev, playername, year) + pg_gamesStarted
            p_stolenBases = int(seasonStats['stolenBases'])
            try:
                p_stolenBasePercentage = float(seasonStats['stolenBasePercentage'])
            except ValueError:
                p_stolenBasePercentage = 0.000
            p_pickoffs = int(seasonStats['pickoffs'])

            progressive.append((playername, numberID, teamAbbrev, gameDate, game['game_id'], p_gamesStarted, p_assists, p_putOuts, p_chances, p_errors, p_fielding, p_passedBall, p_caughtStealing, p_stolenBases, p_stolenBasePercentage, p_pickoffs))
        playerInfo(numberID, teamAbbrev, game)

    progressive = []
    perGame = []

    awayPlayers = boxscore['teams']['away']['players']
    homePlayers = boxscore['teams']['home']['players']

    if homeAbbrev not in suspended:
        for ID in homePlayers:
            if homePlayers[ID]['stats']['fielding'] != {}:
                add('home', homeGameDate, boxscore, ID, homeAbbrev, year)
    if awayAbbrev not in suspended:
        for ID in awayPlayers:
            if awayPlayers[ID]['stats']['fielding'] != {}:
                add('away', awayGameDate, boxscore, ID, awayAbbrev, year)

    c.executemany("insert into 'Season Fielding' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", progressive)
    c.executemany("insert into 'Per Game Fielding' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", perGame)

    conn.commit()
    conn.close()

    if len(progressive) == 0:
        print(awayAbbrev, "and", homeAbbrev, "season fielding stats already added for", homeGameDate)
    if len(perGame) == 0:
        print(awayAbbrev, "and", homeAbbrev, "per game fielding stats already added for", homeGameDate)

def playerInfo(id, teamAbbrev, game):
        pi = sqlite3.connect('2021/Player Info 2021.db')
        p = pi.cursor()

        try:
            p.execute(""" CREATE TABLE '2021' (
            'First Name' text,
            'Last Name' text,
            'Pronunciation' text,
            'Player ID' integer,
            'Team' text,
            'Bat Side' text,
            'Throw Side' text,
            'Height' text,
            'Weight' integer,
            'Number' text,
            'Position' text,
            'MLB Debut' text,
            'Birth Date' text,
            'Birth City' text,
            'Birth State' text,
            'Birth Country' text,
            'Draft Year' integer,
            'Nickname' text,
            'Full Name' text,
            'Strike Zone Top' float,
            'Strike Zone Bottom' float
        )""")
        except Exception as e:
            pass

        p.execute('select Team from "2021" where "Player ID" = ?', (id,))
        fetch = p.fetchone()
        if fetch == None:
            playerInfo = statsapi.player_stat_data(id)
            firstName = playerInfo['first_name']
            lastName = playerInfo['last_name']
            mlbDebut = playerInfo['mlb_debut']
            if mlbDebut == None:
                mlbDebut = game["game_date"]
            batSide = playerInfo['bat_side']
            throwSide = playerInfo['pitch_hand']
            otherInfo = statsapi.get('person', {'personId': id})['people'][0]
            birthDate = otherInfo['birthDate']
            birthCity = otherInfo['birthCity']
            if 'birthStateProvince' in otherInfo:
                birthStateProvince = otherInfo['birthStateProvince']
            else:
                birthStateProvince = ""
            birthCountry = otherInfo['birthCountry']
            height = otherInfo['height']
            weight = otherInfo['weight']
            if 'primaryNumber' in otherInfo:
                primaryNumber = str(otherInfo['primaryNumber'])
            else:
                primaryNumber = ""
            primaryPosition = otherInfo['primaryPosition']['abbreviation']
            if 'pronunciation' in otherInfo:
                pronunciation = otherInfo['pronunciation']
            else:
                pronunciation = ""
            if 'draftYear' in otherInfo:
                draftYear = otherInfo['draftYear']
            else:
                draftYear = ""
            if 'nickName' in otherInfo:
                nickName = otherInfo['nickName']
            else:
                nickName = ""
            strikeZoneTop = otherInfo['strikeZoneTop']
            strikeZoneBottom = otherInfo['strikeZoneBottom']
            fullName = otherInfo['fullFMLName']
            allInfo = (firstName, lastName, pronunciation, id, teamAbbrev, batSide, throwSide, height, weight, primaryNumber, primaryPosition,
            mlbDebut, birthDate, birthCity, birthStateProvince, birthCountry, draftYear, nickName, fullName,
            strikeZoneTop, strikeZoneBottom)
            p.execute("insert into '2021' values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", allInfo)

            pi.commit()
            pi.close()
            print("Player Info added for " + firstName + " " + lastName)
        else:
            team = fetch[0]
            if teamAbbrev not in team:
                newTeam = team + "-" + teamAbbrev
                p.execute('update "2021" set Team = ? where "Player ID" = ?', (newTeam, id))
                pi.commit()
                pi.close()
                print("Team updated")

def pitchData(game):
    conn = sqlite3.connect('2021/Season Pitch Data 2021.db')
    c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS 'All Batters' (
            Name text,
            'Player ID' integer,
            Team text,
            'Game ID' integer,
            Pitch text,
            'Balls' integer,
            'Strikes' integer,
            Amount integer,
            'Pitch%' float,
            'S%' float,
            'AVG Speed' float,
            'AVG Spin' float,
            'Hits' integer,
            'At Bats' integer,
            'BAA' float,
            'Whiffs' integer,
            'Swings' integer,
            'Whiff%' float,
            'SO' integer,
            '1B' integer,
            '2B' integer,
            '3B' integer,
            'HR' integer,
            'SLG' float,
            'CK' integer,
            'SK' integer,
            'Fastest Speed' float,
            'Slowest Speed' float,
            '0-0' integer,
            '0-1' integer,
            '0-2' integer,
            '1-0' integer,
            '1-1' integer,
            '1-2' integer,
            '2-0' integer,
            '2-1' integer,
            '2-2' integer,
            '3-0' integer,
            '3-1' integer,
            '3-2' integer,
            'AVG Break Angle' float,
            'AVG Break Length' float,
            'AVG Plate Time' float,
            'AVG Extension' float,
            'Total Bases' integer,
            'Total Speed' float,
            'Total Spin' integer,
            'Total Break Angle' float,
            'Total Break Length' float,
            'Total Plate Time' float,
            'Total Extension' float,
            'SRP' integer,
            'EP' integer
        )""")

    c.execute(""" CREATE TABLE IF NOT EXISTS 'LH Batters' (
            Name text,
            'Player ID' integer,
            Team text,
            'Game ID' integer,
            Pitch text,
            'Balls' integer,
            'Strikes' integer,
            Amount integer,
            'Pitch%' float,
            'S%' float,
            'AVG Speed' float,
            'AVG Spin' float,
            'Hits' integer,
            'At Bats' integer,
            'BAA' float,
            'Whiffs' integer,
            'Swings' integer,
            'Whiff%' float,
            'SO' integer,
            '1B' integer,
            '2B' integer,
            '3B' integer,
            'HR' integer,
            'SLG' float,
            'CK' integer,
            'SK' integer,
            'Fastest Speed' float,
            'Slowest Speed' float,
            '0-0' integer,
            '0-1' integer,
            '0-2' integer,
            '1-0' integer,
            '1-1' integer,
            '1-2' integer,
            '2-0' integer,
            '2-1' integer,
            '2-2' integer,
            '3-0' integer,
            '3-1' integer,
            '3-2' integer,
            'AVG Break Angle' float,
            'AVG Break Length' float,
            'AVG Plate Time' float,
            'AVG Extension' float,
            'Total Bases' integer,
            'Total Speed' float,
            'Total Spin' integer,
            'Total Break Angle' float,
            'Total Break Length' float,
            'Total Plate Time' float,
            'Total Extension' float,
            'SRP' integer,
            'EP' integer
        )""")

    c.execute(""" CREATE TABLE IF NOT EXISTS 'RH Batters' (
            Name text,
            'Player ID' integer,
            Team text,
            'Game ID' integer,
            Pitch text,
            'Balls' integer,
            'Strikes' integer,
            Amount integer,
            'Pitch%' float,
            'S%' float,
            'AVG Speed' float,
            'AVG Spin' float,
            'Hits' integer,
            'At Bats' integer,
            'BAA' float,
            'Whiffs' integer,
            'Swings' integer,
            'Whiff%' float,
            'SO' integer,
            '1B' integer,
            '2B' integer,
            '3B' integer,
            'HR' integer,
            'SLG' float,
            'CK' integer,
            'SK' integer,
            'Fastest Speed' float,
            'Slowest Speed' float,
            '0-0' integer,
            '0-1' integer,
            '0-2' integer,
            '1-0' integer,
            '1-1' integer,
            '1-2' integer,
            '2-0' integer,
            '2-1' integer,
            '2-2' integer,
            '3-0' integer,
            '3-1' integer,
            '3-2' integer,
            'AVG Break Angle' float,
            'AVG Break Length' float,
            'AVG Plate Time' float,
            'AVG Extension' float,
            'Total Bases' integer,
            'Total Speed' float,
            'Total Spin' integer,
            'Total Break Angle' float,
            'Total Break Length' float,
            'Total Plate Time' float,
            'Total Extension' float,
            'SRP' integer,
            'EP' integer
        )""")

    c.execute("CREATE TABLE IF NOT EXISTS 'Check Dates' (Name text, 'Player ID' integer, 'Team' text, 'Last Date' text, 'Game ID' integer)")

    conn.commit()
    conn.close()

    inningsName = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th", 8: "8th", 9: "9th", 10: "10th",
                   11: "11th", 12: "12th", 13: "13th", 14: "14th", 15: "15th", 16: "16th", 17: "17th", 18: "18th"}

    def dateValue(date):
        dhNumber = 0
        if "(" in date:  # This means that the date is a doubleheader date
            dhNumber = int(date[len(date) - 2])
            date = date[0:len(date) - 3]
        dateSplit = date.split("/")
        month = dateSplit[0]
        day = dateSplit[1]
        value = int(month) * 1000 + int(day) * 10 + dhNumber
        return value

    def shouldInsert(pitcherID):
        s.execute('select "Last Date" from "Check Dates" where "Player ID" = ?', (pitcherID,))
        fetch = s.fetchone()
        if fetch == None:
            return True
        else:
            lastDateValue = dateValue(fetch[0])
            gameDateValue = dateValue(gameDate)

            if gameDateValue > lastDateValue:
                return True
            if gameDateValue <= lastDateValue:
                return False

    def accumulateForBatSide(accumulatingDict, tableName, logPitchesDict, pitcherName, pa, pitch):

        def missingData(dataType, pitchType, pitcherName):
            indexOfDataType = None
            if dataType == 'spinRate':
                indexOfDataType = 8
            try:
                pitcherAverageForDataType = allAccumulatePitches[pitcherName]['pitchData'][pitchType][indexOfDataType]
            except KeyError:
                s.execute('select "AVG Spin" from "All Batters" where Name = ? and Pitch = ?', (pitcherName, pitchType))
                f = s.fetchone()
                if f == None:
                    pitcherAverageForDataType = 0
                    input("Can't find an average spin for " + pitcherName)
                else:
                    pitcherAverageForDataType = f[0]

            return pitcherAverageForDataType

        noPitchType = False
        noSpeed = False
        noSpinRate = False
        resultOfPlay = pa['result']['event']
        pitchData = pitch['pitchData']
        try:
            pitchType = pitch['details']['type']['description']
        except KeyError as e:
            pitchType = "Unknown"
            noPitchType = True
            print("Unknown pitch type")
            # input("Press enter to break/leave function")
        try:
            speed = pitchData['startSpeed']
        except KeyError as e:
            if pitchType == "Unknown":
                speed = 0
                noSpeed = True
        spinRateProblemForPitch = 0
        try:
            spinRate = pitchData['breaks']['spinRate']
        except KeyError as e:
            if not noPitchType:
                spinRate = missingData("spinRate", pitchType, pitcherName)
                spinRateProblemForPitch = 1
                noSpinRate = True
            else:
                spinRate = 0
        try:
            breakAngle = pitchData['breaks']['breakAngle']
            breakLength = pitchData['breaks']['breakLength']
        except KeyError:
            if noPitchType:
                breakAngle = 0
                breakLength = 0
            else:
                print(pitchData)
                input("Break problem")
        try:
            plateTime = pitchData['plateTime']
        except KeyError:
            if noPitchType:
                plateTime = 0.00
            else:
                print(pitchData)
                input("plateTime problem")
        extensionProblemForPitch = 0
        try:
            extension = pitchData['extension']
        except KeyError:
            if noPitchType:
                extension = 0.00
            else:
                extension = 6.50
                extensionProblemForPitch = 1

        # if not noPitchType and not noSpeed and not noSpinRate:
        #     print(speed, "MPH /", spinRate, "RPM", pitchType, "by", pitcherName, "on", gameDate, "in the", inning, "to", hitterName, "("+str(logPitchesDict[pitcherName]['pitches'])+")")

        def accumulate(tuple, typeOfPitch):

            balls = tuple[5]
            strikes = tuple[6]
            amount = tuple[7]
            pitchPercentage = tuple[8]
            strikePercentage = tuple[8+1]
            avgSpeed = tuple[9+1]
            avgSpin = tuple[10+1]
            hits = tuple[11+1]
            atBats = tuple[12+1]
            bAA = tuple[13+1]
            whiffs = tuple[14+1]
            swings = tuple[15+1]
            whiffPercentage = tuple[16+1]
            strikeOuts = tuple[17+1]
            singles = tuple[18+1]
            doubles = tuple[19+1]
            triples = tuple[20+1]
            homeRuns = tuple[21+1]
            slg = tuple[22+1]
            calledSO = tuple[23+1]
            swingingSO = tuple[24+1]
            fastestSpeed = tuple[25+1]
            slowestSpeed = tuple[26+1]
            oO = tuple[27+1]
            oOne = tuple[28+1]
            oTwo = tuple[29+1]
            oneO = tuple[30+1]
            oneOne = tuple[31+1]
            oneTwo = tuple[32+1]
            twoO = tuple[33+1]
            twoOne = tuple[34+1]
            twoTwo = tuple[35+1]
            threeO = tuple[36+1]
            threeOne = tuple[37+1]
            threeTwo = tuple[38+1]
            avgBreakAngle = tuple[39+1]
            avgBreakLength = tuple[40+1]
            avgPlateTime = tuple[41+1]
            avgExtension = tuple[42+1]
            totalBases = tuple[43+1]
            totalSpeed = tuple[44+1]
            totalSpin = tuple[45+1]
            totalBreakAngle = tuple[46+1]
            totalBreakLength = tuple[47+1]
            totalPlateTime = tuple[48+1]
            totalExtension = tuple[49+1]
            spinRateProbem = tuple[50+1]
            extensionProblem = 0
            extensionProblem = tuple[51+1]

            amount += 1
            if typeOfPitch == 'All Pitches':
                pitchPercentage = 1.000
            totalSpeed = round(totalSpeed + speed, 1)
            totalSpin += spinRate
            totalBreakAngle = round(totalBreakAngle + breakAngle, 1)
            totalBreakLength = round(totalBreakLength + breakLength, 1)
            totalPlateTime = round(totalPlateTime + plateTime, 2)
            totalExtension += extension
            avgSpeed = round(totalSpeed / amount, 1)
            avgSpin = round(totalSpin / amount, 2)
            avgBreakAngle = round(totalBreakAngle / amount, 1)
            avgBreakLength = round(totalBreakLength / amount, 1)
            avgPlateTime = round(totalPlateTime / amount, 2)
            avgExtension = round(totalExtension / amount, 2)
            spinRateProbem += spinRateProblemForPitch
            extensionProblem += extensionProblemForPitch

            # This if statement is redundant and is just here so the other if statements can be collapsed
            if len(count) > 0:
                ballsInCount = count[0]
                strikesInCount = count[1]
                if ballsInCount == 0 and strikesInCount == 0:
                    oO += 1
                elif ballsInCount == 0 and strikesInCount == 1:
                    oOne += 1
                elif ballsInCount == 0 and strikesInCount == 2:
                    oTwo += 1
                elif ballsInCount == 1 and strikesInCount == 0:
                    oneO += 1
                elif ballsInCount == 1 and strikesInCount == 1:
                    oneOne += 1
                elif ballsInCount == 1 and strikesInCount == 2:
                    oneTwo += 1
                elif ballsInCount == 2 and strikesInCount == 0:
                    twoO += 1
                elif ballsInCount == 2 and strikesInCount == 1:
                    twoOne += 1
                elif ballsInCount == 2 and strikesInCount == 2:
                    twoTwo += 1
                elif ballsInCount == 3 and strikesInCount == 0:
                    threeO += 1
                elif ballsInCount == 3 and strikesInCount == 1:
                    threeOne += 1
                elif ballsInCount == 3 and strikesInCount == 2:
                    threeTwo += 1  #

            if speed > fastestSpeed:
                fastestSpeed = speed
            if slowestSpeed > 0:
                if speed < slowestSpeed:
                    slowestSpeed = speed
            else:
                slowestSpeed = speed

            callDescription = pitch['details']['description']
            isBallInPlay = pitch['details']['isInPlay']
            if pitch['details']['isBall']:
                balls += 1
            if pitch['details'][
                'isStrike']:  # Note that 'isStrike' will not be true if the ball was put in play, so increment strikes when checking for ball in play
                strikes += 1
            if 'Swinging Strike' in callDescription or 'Foul Tip' in callDescription or 'Missed' in callDescription:
                swings += 1
                whiffs += 1
            elif callDescription == 'Foul' or callDescription == 'Foul Bunt' or isBallInPlay:
                swings += 1
                whiffs += 0
                if isBallInPlay:
                    strikes += 1
                    hitData = pitch['hitData']
                    # input(hitData)
                    if resultOfPlay == 'Single' or resultOfPlay == 'Double' or resultOfPlay == 'Triple' or resultOfPlay == 'Home Run':
                        hits += 1
                        atBats += 1
                        if resultOfPlay == 'Single':
                            singles += 1
                            totalBases += 1
                        elif resultOfPlay == 'Double':
                            doubles += 1
                            totalBases += 2
                        elif resultOfPlay == 'Triple':
                            triples += 1
                            totalBases += 3
                        elif resultOfPlay == 'Home Run':
                            homeRuns += 1
                            totalBases += 4
                    elif resultOfPlay == 'Sac Fly' or resultOfPlay == 'Sac Bunt':
                        hits += 0
                        atBats += 0
                    else:  # this includes fielding errors and regular outs
                        hits += 0
                        atBats += 1
            strikePercentage = round(strikes / amount, 3)

            if swings > 0:
                whiffPercentage = round(whiffs / swings, 3)
            else:
                whiffPercentage = 0.000

            if p == len(playEvents) - 1:
                if resultOfPlay == 'Strikeout':
                    hits += 0
                    atBats += 1
                    strikeOuts += 1
                    if 'Called Strike' in callDescription:
                        calledSO += 1
                    if 'Swinging Strike' in callDescription or 'Foul Tip' in callDescription or 'Foul Bunt' in callDescription:
                        swingingSO += 1

            if atBats > 0:
                bAA = round(hits / atBats, 3)
                slg = round(totalBases / atBats, 3)
            else:
                bAA = 0.000
                slg = 0.000

            return (pitcherName, pitcherID, pitcherTeamAbbrev, gameId, typeOfPitch, balls, strikes, amount, pitchPercentage, strikePercentage, avgSpeed, avgSpin, hits, atBats, bAA, whiffs, swings, whiffPercentage, strikeOuts, singles, doubles, triples, homeRuns, slg, calledSO, swingingSO, fastestSpeed, slowestSpeed, oO, oOne, oTwo, oneO, oneOne, oneTwo, twoO, twoOne, twoTwo, threeO, threeOne, threeTwo, avgBreakAngle, avgBreakLength, avgPlateTime, avgExtension, totalBases, totalSpeed, totalSpin, totalBreakAngle, totalBreakLength, totalPlateTime, totalExtension, spinRateProbem, extensionProblem)

        if pitcherName not in accumulatingDict:
            accumulatingDict[pitcherName] = {'pitchData': {}}

        if 'All Pitches' not in accumulatingDict[pitcherName]['pitchData']:
            s.execute('select * from "' + tableName + '" where Name = ? and Pitch = "All Pitches" order by Amount DESC', (pitcherName,))
            previousAllData = s.fetchone()
            if previousAllData == None:
                accumulatingDict[pitcherName]['pitchData']['All Pitches'] = (pitcherName, pitcherID, pitcherTeamAbbrev, gameId, 'All Pitches', 0, 0, 0.00, 0, 0.00, 0.00, 0, 0, 0.00, 0, 0, 0.00, 0, 0.000, 0.000, 0, 0, 0, 0.00, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0)
            else:
                accumulatingDict[pitcherName]['pitchData']['All Pitches'] = previousAllData
        new = accumulate(accumulatingDict[pitcherName]['pitchData']['All Pitches'], 'All Pitches')
        accumulatingDict[pitcherName]['pitchData']['All Pitches'] = new

        if pitchType not in accumulatingDict[pitcherName]['pitchData']:
            s.execute('select * from "' + tableName + '" where Name = ? and Pitch = ? order by Amount DESC', (pitcherName, pitchType))
            previousPitchTypeData = s.fetchone()
            if previousPitchTypeData == None:
                accumulatingDict[pitcherName]['pitchData'][pitchType] = (pitcherName, pitcherID, pitcherTeamAbbrev, gameId, pitchType, 0, 0, 0.00, 0, 0.00, 0.00, 0, 0, 0.00, 0, 0, 0.00, 0, 0.000, 0.000, 0, 0, 0, 0.00, 0, 0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0)
            else:
                accumulatingDict[pitcherName]['pitchData'][pitchType] = previousPitchTypeData
        new = accumulate(accumulatingDict[pitcherName]['pitchData'][pitchType], pitchType)
        accumulatingDict[pitcherName]['pitchData'][pitchType] = new

    def fixData(firstPitcherName, secondPitcherName, firstPitcherActualPitchesPerGame):
        fixLogPitches = {}
        fixAllAccumulatePitches = {}
        fixLeftyAccumulatePitches = {}
        fixRightyAccumulatePitches = {}

        game = statsapi.get('game', {'gamePk': gameId})

        allPlays = game['liveData']['plays']['allPlays']

        if game_status != 'Postponed':

            seasonDB = sqlite3.connect('2021/Season Pitch Data 2021.db')
            s = seasonDB.cursor()

            for pa in allPlays:
                inning = pa['about']['halfInning'] + " of the " + inningsName[pa['about']['inning']]
                pitcherName = pa['matchup']['pitcher']['fullName']
                pitcherID = pa['matchup']['pitcher']['id']
                if pa['about']['halfInning'] == 'top':
                    pitcherTeamAbbrev = game['gameData']['teams']['home']['abbreviation']
                else:
                    pitcherTeamAbbrev = game['gameData']['teams']['away']['abbreviation']
                hitterName = pa['matchup']['batter']['fullName']
                hitterBatSide = pa['matchup']['batSide']['description']
                playEvents = pa['playEvents']

                # Decided not to call shouldInsert() because it should be needed
                if pitcherName == firstPitcherName or pitcherName == secondPitcherName:
                    count = [0, 0]
                    for p in range(len(playEvents)):

                        # If the first pitcher's logged pitches isn't at the actual amount, we set the pitcherName variable as the first pitcher's name (to avoid giving the pitch to the second pitcher)
                        if len(fixLogPitches) > 0:
                            if fixLogPitches[firstPitcherName]['pitches'] < firstPitcherActualPitchesPerGame:
                                pitcherName = firstPitcherName
                            else:
                                pitcherName = secondPitcherName

                        pitch = playEvents[p]
                        if pitch['isPitch'] == True and pitch['details']['description'] != 'Automatic Ball':

                            # Originally thought that the first pitcher's ID would accidentally be given to the second pitcher, but that isn't the case because when the second pitcher's name needs to be added to fixLogPitches, pitcherID will be set to his ID
                            # Important Note: Refer to the comment right above the pitchData() function definition
                            if pitcherName not in fixLogPitches:
                                fixLogPitches[pitcherName] = {'Player ID': pitcherID, 'Team': pitcherTeamAbbrev,
                                                              'pitches': 0}
                            fixLogPitches[pitcherName]['pitches'] += 1

                            accumulateForBatSide(fixAllAccumulatePitches, "All Batters", fixLogPitches, pitcherName, pa, pitch)
                            if hitterBatSide == 'Left':
                                accumulateForBatSide(fixLeftyAccumulatePitches, "LH Batters", fixLogPitches, pitcherName, pa, pitch)
                            if hitterBatSide == 'Right':
                                accumulateForBatSide(fixRightyAccumulatePitches, "RH Batters", fixLogPitches, pitcherName, pa, pitch)
                            count = [pitch['count']['balls'], pitch['count']['strikes']]

        skip = False
        fixListOfPitchers = list(fixLogPitches.keys())
        for p in range(len(fixListOfPitchers)):
            if not skip:
                pitcherName = fixListOfPitchers[p]
                pitcherTeamAbbrev = fixLogPitches[fixListOfPitchers[p]]['Team']
                pitcherID = fixLogPitches[fixListOfPitchers[p]]['Player ID']
                pIDWithID = "ID" + str(fixLogPitches[fixListOfPitchers[p]]['Player ID'])
                loggedNumberOfPitches = fixLogPitches[fixListOfPitchers[p]]['pitches']
                try:
                    actualPitchesPerGame = \
                    game['liveData']['boxscore']['teams']['home']['players'][pIDWithID]['stats']['pitching'][
                        'numberOfPitches']
                except KeyError:
                    actualPitchesPerGame = \
                    game['liveData']['boxscore']['teams']['away']['players'][pIDWithID]['stats']['pitching'][
                        'numberOfPitches']
                if actualPitchesPerGame == loggedNumberOfPitches:
                    if shouldInsert(pitcherID) == True:
                        try:
                            for differentPitch in fixAllAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempFixAllAccumulatePitchesForPitch = list(fixAllAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempFixAllAccumulatePitchesForPitch[8] = round(tempFixAllAccumulatePitchesForPitch[7]/fixAllAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    fixAllAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempFixAllAccumulatePitchesForPitch)
                                s.execute('delete from "All Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "All Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', allAccumulatePitches[pitcherName]['pitchData'][differentPitch])

                            for differentPitch in fixLeftyAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempFixLeftyAccumulatePitchesForPitch = list(fixLeftyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempFixLeftyAccumulatePitchesForPitch[8] = round(tempFixLeftyAccumulatePitchesForPitch[7]/fixLeftyAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    fixLeftyAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempFixLeftyAccumulatePitchesForPitch)
                                s.execute('delete from "LH Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "LH Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', leftyAccumulatePitches[pitcherName]['pitchData'][differentPitch])

                            for differentPitch in fixRightyAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempFixRightyAccumulatePitchesForPitch = list(fixRightyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempFixRightyAccumulatePitchesForPitch[8] = round(tempFixRightyAccumulatePitchesForPitch[7]/fixRightyAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    fixRightyAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempFixRightyAccumulatePitchesForPitch)
                                s.execute('delete from "RH Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "RH Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rightyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                        except KeyError:
                            pass

                        s.execute('delete from "Check Dates" where "Player ID" = ?', (pitcherID,))
                        s.execute('insert into "Check Dates" values (?,?,?,?,?)', (pitcherName, pitcherID, pitcherTeamAbbrev, gameDate, gameId))
                        seasonDB.commit()

                        print("Looks good for " + pitcherName, "(" + pitcherTeamAbbrev + ") with " + str(loggedNumberOfPitches) + " pitches")
                    else:
                        print("Pitch Data on", gameDate, "should already be added for", pitcherName,
                              "(" + pitcherTeamAbbrev + ")")
                else:
                    print("Actual Number of Pitches:", actualPitchesPerGame)
                    print("Logged Number of Pitches:", loggedNumberOfPitches)
                    print("Amount of pitches don't match for " + pitcherName)
                    checkNextPitcher(pitcherName)
                    skip = True
            else:
                skip = False
        print("==============================================")

    def checkNextPitcher(beforePitcherName):
        nextPitcherName = listOfPitchers[p + 1]
        nextPitcherId = logPitches[listOfPitchers[p + 1]]['Player ID']
        npIDWithID = "ID" + str(logPitches[listOfPitchers[p + 1]]['Player ID'])
        nextLoggedNumberOfPitches = logPitches[listOfPitchers[p + 1]]['pitches']
        try:
            nextActualPitchesPerGame = \
            game['liveData']['boxscore']['teams']['home']['players'][npIDWithID]['stats']['pitching']['numberOfPitches']
        except KeyError:
            nextActualPitchesPerGame = \
            game['liveData']['boxscore']['teams']['away']['players'][npIDWithID]['stats']['pitching']['numberOfPitches']

        if nextActualPitchesPerGame != nextLoggedNumberOfPitches:
            print(beforePitcherName, "logged number of pitches is", loggedNumberOfPitches,
                  "but actual number of pitches might be", actualPitchesPerGame)
            print(nextPitcherName, "logged number of pitches is", nextLoggedNumberOfPitches,
                  "but actual number of pitches might be", nextActualPitchesPerGame)
            if (nextLoggedNumberOfPitches - nextActualPitchesPerGame) == (actualPitchesPerGame - loggedNumberOfPitches):
                print("It looks like", nextPitcherName, "has", nextLoggedNumberOfPitches - nextActualPitchesPerGame,
                      beforePitcherName, "pitches")
                print("Attempt to fix issue will happen soon")
                # time.sleep(2.5)
                fixData(beforePitcherName, nextPitcherName, actualPitchesPerGame)
            else:
                input("WE HAVE A CATASTROPHIC PROBLEM")

    # year = '2021'
    # today = datetime.date.today()
    # theDayBefore = today - datetime.timedelta(days=2)
    # yesterday = today - datetime.timedelta(days=1)
    # tomorrow = today + datetime.timedelta(days=1)
    # sched = statsapi.schedule(start_date=theDayBefore, end_date=yesterday)
    # for game in sched:

    logPitches = {}
    allAccumulatePitches = {}
    leftyAccumulatePitches = {}
    rightyAccumulatePitches = {}
    gameId = game["game_id"]
    gameDate = game["game_date"]
    splitDate = gameDate.split("-")
    gameDate = str(int(splitDate[1])) + "/" + splitDate[2] + "/" + splitDate[0][2:4]
    if game['doubleheader'] != 'N':
        gameDate += "(" + str(game["game_num"]) + ")"  # adds number to the back of the game date if the game is a part of a doubleheader

    game_result = game["summary"]
    game_status = game["status"]
    game = statsapi.get('game', {'gamePk': gameId})

    allPlays = game['liveData']['plays']['allPlays']

    seasonDB = sqlite3.connect('2021/Season Pitch Data 2021.db')
    s = seasonDB.cursor()

    if game_status != 'Postponed' and (game_status == "Final" or game_status == "Game Over" or 'Completed' in game_status):
        for pa in allPlays:
            inning = pa['about']['halfInning'] + " of the " + inningsName[pa['about']['inning']]
            pitcherName = pa['matchup']['pitcher']['fullName']
            pitcherID = pa['matchup']['pitcher']['id']
            if pa['about']['halfInning'] == 'top':
                pitcherTeamAbbrev = game['gameData']['teams']['home']['abbreviation']
            else:
                pitcherTeamAbbrev = game['gameData']['teams']['away']['abbreviation']
            hitterName = pa['matchup']['batter']['fullName']
            hitterBatSide = pa['matchup']['batSide']['description']
            playEvents = pa['playEvents']

            if True:
                count = [0, 0]
                for p in range(len(playEvents)):
                    pitch = playEvents[p]
                    # input(pitch)
                    if pitch['isPitch'] == True and pitch['details']['description'] != 'Automatic Ball':

                        if pitcherName not in logPitches:
                            logPitches[pitcherName] = {'Player ID': pitcherID, 'Team': pitcherTeamAbbrev, 'pitches': 0}
                        logPitches[pitcherName]['pitches'] += 1

                        accumulateForBatSide(allAccumulatePitches, "All Batters", logPitches, pitcherName, pa, pitch)
                        if hitterBatSide == 'Left':
                            accumulateForBatSide(leftyAccumulatePitches, "LH Batters", logPitches, pitcherName, pa, pitch)
                        if hitterBatSide == 'Right':
                            accumulateForBatSide(rightyAccumulatePitches, "RH Batters", logPitches, pitcherName, pa, pitch)
                        count = [pitch['count']['balls'], pitch['count']['strikes']]


        skip = False
        listOfPitchers = list(logPitches.keys())
        for p in range(len(listOfPitchers)):
            if not skip:
                pitcherName = listOfPitchers[p]
                pitcherTeamAbbrev = logPitches[listOfPitchers[p]]['Team']
                pitcherID = logPitches[listOfPitchers[p]]['Player ID']
                pIDWithID = "ID" + str(logPitches[listOfPitchers[p]]['Player ID'])
                loggedNumberOfPitches = logPitches[listOfPitchers[p]]['pitches']
                try:
                    actualPitchesPerGame = game['liveData']['boxscore']['teams']['home']['players'][pIDWithID]['stats']['pitching']['numberOfPitches']
                except KeyError:
                    actualPitchesPerGame = game['liveData']['boxscore']['teams']['away']['players'][pIDWithID]['stats']['pitching']['numberOfPitches']
                if actualPitchesPerGame == loggedNumberOfPitches:
                    if shouldInsert(pitcherID) == True:
                        try: # An error will occur if the pitcherName isn't in the dictionaries (it means the pitcher didn't pitch against a lefty or a righty)
                            for differentPitch in allAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempAllAccumulatePitchesForPitch = list(allAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempAllAccumulatePitchesForPitch[8] = round(tempAllAccumulatePitchesForPitch[7]/allAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    allAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempAllAccumulatePitchesForPitch)
                                s.execute('delete from "All Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "All Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', allAccumulatePitches[pitcherName]['pitchData'][differentPitch])

                            for differentPitch in leftyAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempLeftyAccumulatePitchesForPitch = list(leftyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempLeftyAccumulatePitchesForPitch[8] = round(tempLeftyAccumulatePitchesForPitch[7]/leftyAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    leftyAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempLeftyAccumulatePitchesForPitch)
                                s.execute('delete from "LH Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "LH Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', leftyAccumulatePitches[pitcherName]['pitchData'][differentPitch])

                            for differentPitch in rightyAccumulatePitches[pitcherName]['pitchData']:
                                if differentPitch != 'All Pitches':
                                    tempRightyAccumulatePitchesForPitch = list(rightyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                                    tempRightyAccumulatePitchesForPitch[8] = round(tempRightyAccumulatePitchesForPitch[7]/rightyAccumulatePitches[pitcherName]['pitchData']['All Pitches'][7], 3)
                                    rightyAccumulatePitches[pitcherName]['pitchData'][differentPitch] = tuple(tempRightyAccumulatePitchesForPitch)
                                s.execute('delete from "RH Batters" where Name = ? and Pitch = ?', (pitcherName, differentPitch))
                                s.execute('insert into "RH Batters" values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', rightyAccumulatePitches[pitcherName]['pitchData'][differentPitch])
                        except KeyError:
                            pass

                        s.execute('delete from "Check Dates" where "Player ID" = ?', (pitcherID,))
                        s.execute('insert into "Check Dates" values (?,?,?,?,?)', (pitcherName, pitcherID, pitcherTeamAbbrev, gameDate, gameId))
                        seasonDB.commit()

                        print("Looks good for " + pitcherName, "(" + pitcherTeamAbbrev + ") with " + str(loggedNumberOfPitches) + " pitches")
                    else:
                        print("Pitch Data on", gameDate, "should already be added for", pitcherName,
                              "(" + pitcherTeamAbbrev + ")")
                else:
                    print("Actual Number of Pitches:", actualPitchesPerGame)
                    print("Logged Number of Pitches:", loggedNumberOfPitches)
                    print("Amount of pitches don't match for " + pitcherName)
                    checkNextPitcher(pitcherName)
                    skip = True
            else:
                skip = False
        seasonDB.close()

everything()
gl.close()

print(datetime.datetime.now()-start)