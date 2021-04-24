import sqlite3

hittingCategories = {
    'Season': {'All Categories': 'All Categories', 'Average': 'AVG', 'Hits': 'Hits', 'OBP': 'OBP', 'SLG': 'SLG', 'OPS': 'OPS', 'BABIP': 'BABIP', 'Doubles': '2B', 'Triples': '3B', 'Home Runs': 'HR', 'XBH': 'XBH', 'ISO': 'ISO', 'RBI': 'RBI', 'Runs': 'Runs', 'Strike Outs': 'Strikeouts', 'K%': 'K%', 'Walks': 'Walks', 'BB%': 'BB%', 'HBP': 'HBP', 'SB': 'SB', 'CS': 'CS', 'SB%': 'SB%', 'Total Bases': 'TB', 'Left On Base': 'LOB', 'PA': 'PA', 'ABs': 'AB', 'AB/HR': 'AB/HR', 'IBB': 'IBB', 'Sac Flies': 'Sac Flies', 'Ground Outs': 'Ground Outs', 'Fly Outs': 'Fly Outs', 'Double Plays': 'Double Plays', 'Triple Plays': 'Triple Plays', 'Sac Bunts': 'Sac Bunts', 'Pickoffs': 'Pickoffs', 'Catcher Inteference': 'CI'},
    'Per Game': {'All Categories': 'All Categories', 'Hits': 'Hits', 'Doubles': '2B', 'Triples': '3B', 'Home Runs': 'HR', 'XBH': 'XBH', 'RBI': 'RBI', 'Runs': 'Runs', 'Strike Outs': 'Strikeouts', 'Walks': 'Walks', 'HBP': 'HBP', 'SB': 'SB', 'CS': 'CS', 'SB%': 'SB%', 'Total Bases': 'TB', 'LOB': 'Left On Base', 'PA': 'PA', 'ABs': 'AB', 'IBB': 'IBB', 'Sac Flies': 'Sac Flies', 'Ground Outs': 'Ground Outs', 'Fly Outs': 'Fly Outs', 'Double Plays': 'Double Plays', 'Triple Plays': 'Triple Plays', 'Sac Bunts': 'Sac Bunts', 'Pickoffs': 'Pickoffs', 'Catcher Inteference': 'CI'}
}

pitchingCategories = {
    'Season': {'Air Outs': 'Air Outs', 'At Bats': 'AB', 'Balks': 'Balks', 'Balls': 'Balls', 'Batters Faced': 'Batters Faced', 'BAA': 'BAA', 'Blown Saves': 'Blown Saves', 'Catchers Interferences': 'CI', 'Caught Stealings': 'CS', 'Complete Games': 'CG', 'Doubles': '2B', 'ERA': 'ERA', 'Earned Runs': 'ER', 'Games': 'G', 'Games Finished': 'Games Finished', 'Games Started': 'GS', 'Ground Outs': 'Ground Outs', 'Ground to Air': 'GO/AO', 'Hit By Pitches': 'HBP', 'Hits': 'Hits', 'Hits Per 9': 'Hits Per 9', 'Holds': 'Holds', 'Home Runs': 'HR', 'Home Runs Per 9': 'HR Per 9', 'Inherited Runners': 'IR', 'Inherited Runners Scored': 'IRS', 'Innings': 'IP', 'Intentional Walks': 'IBB', 'Losses': 'Losses', 'OBP': 'OBP', 'Outs': 'Outs', 'Pickoffs': 'Pickoffs', 'Pitches': 'Pitches', 'Pitches/IP': 'Pitches/IP', 'Runs': 'Runs', 'RBI': 'RBI', 'Runs Per 9': 'Runs Per 9', 'Sacrifice Bunts': 'Sac Bunts', 'Sacrifice Flies': 'Sac Flies', 'Save Opportunities': 'Save Opp.', 'Saves': 'Saves', 'Shut Outs': 'Shut Outs', 'SB%': 'SB%', 'Stolen Bases': 'SB', 'S%': 'S%', 'K%': 'K%', 'Strikeout To Walk': 'K/BB', 'Strikeouts': 'Strikeouts', 'Strikeouts Per 9': 'Strikeouts Per 9', 'Strikes': 'Strikes', 'Triples': '3B', 'WHIP': 'WHIP', 'Walks': 'Walks', 'Walks Per 9': 'Walks Per 9', 'Wild Pitches': 'WP', 'W%': 'Win%', 'Wins': 'Wins'},
    'Per Game': {'Air Outs': 'Air Outs', 'At Bats': 'AB', 'Balks': 'Balks', 'Balls': 'Balls', 'Batters Faced': 'Batters Faced', 'BAA': 'BAA', 'Blown Saves': 'Blown Saves', 'Catchers Interferences': 'CI', 'Caught Stealings': 'CS', 'Complete Games': 'CG', 'Doubles': '2B', 'Earned Runs': 'ER', 'Games Finished': 'Games Finished', 'Games Started': 'GS', 'Ground Outs': 'Ground Outs', 'Hit By Pitches': 'HBP', 'Hits': 'Hits', 'Hits Per 9': 'Hits Per 9', 'Holds': 'Holds', 'Home Runs': 'HR', 'Home Runs Per 9': 'HR Per 9', 'Inherited Runners': 'IR', 'Inherited Runners Scored': 'IRS', 'Innings': 'IP', 'Intentional Walks': 'IBB', 'Losses': 'Losses', 'Outs': 'Outs', 'Pickoffs': 'Pickoffs', 'Pitches': 'Pitches', 'Pitches/IP': 'Pitches/IP', 'Runs': 'Runs', 'RBI': 'RBI', 'Runs Per 9': 'Runs Per 9', 'Sacrifice Bunts': 'Sac Bunts', 'Sacrifice Flies': 'Sac Flies', 'Save Opportunities': 'Save Opp.', 'Saves': 'Saves', 'Shut Outs': 'Shut Outs', 'SB%': 'SB%', 'Stolen Bases': 'SB', 'S%': 'S%', 'Strikeouts': 'Strikeouts', 'Strikeouts Per 9': 'Strikeouts Per 9', 'Strikes': 'Strikes', 'Triples': '3B', 'WHIP': 'WHIP', 'Walks': 'Walks', 'Walks Per 9': 'Walks Per 9', 'Wild Pitches': 'WP', 'Wins': 'Wins'}
}

fieldingCategories = {
    'Season': {'Games Started': 'GS', 'Assists': 'Assists', 'Putouts': 'Putouts', 'Chances': 'Chances', 'Errors': 'Errors', 'Fielding%': 'Fielding%', 'Passed Balls': 'Passed Balls', 'Caught Stealings': 'CS', 'Stolen Bases': 'SB', 'SB%': 'SB%', 'Pickoffs': 'Pickoffs'},
    'Per Game': {'Games Started': 'GS', 'Assists': 'Assists', 'Putouts': 'Putouts', 'Chances': 'Chances', 'Errors': 'Errors', 'Passed Balls': 'Passed Balls', 'Caught Stealings': 'CS', 'Stolen Bases': 'SB', 'SB%': 'SB%', 'Pickoffs': 'Pickoffs'}
}

def seasonHitting(teamAbbrev, playername, selectedCategory):
    categories = hittingCategories['Season']

    conn = sqlite3.connect('2021/Hitting 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "'+ str(categories[selectedCategory]) +'" from "Season Hitting" where Team = ? and Name = ? order by date ASC', (teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def perGameHitting(teamAbbrev, playername, selectedCategory):
    categories = hittingCategories['Per Game']

    conn = sqlite3.connect('2021/Hitting 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "' + categories[selectedCategory] + '" from "Per Game Hitting" where Team = ? and Name = ? order by date ASC', (teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def seasonPitching(teamAbbrev, playername, selectedCategory):
    categories = pitchingCategories['Season']

    conn = sqlite3.connect('2021/Pitching 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Season Pitching" where Team = ? and Name = ? order by date ASC',(teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def perGamePitching(teamAbbrev, playername, selectedCategory):
    categories = pitchingCategories['Per Game']

    conn = sqlite3.connect('2021/Pitching 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Per Game Pitching" where Team = ? and Name = ? order by date ASC',(teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def seasonFielding(teamAbbrev, playername, selectedCategory):
    categories = fieldingCategories['Season']

    conn = sqlite3.connect('2021/Fielding 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Season Fielding" where Team = ? and Name = ? order by date ASC', (teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def perGameFielding(teamAbbrev, playername, selectedCategory):
    categories = fieldingCategories['Per Game']

    conn = sqlite3.connect('2021/Fielding 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Per Game Fielding" where Team = ? and Name = ? order by date ASC', (teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def listOfPlayers(teamAbbrev, type):

    conn = sqlite3.connect('2021/' + type + ' 2021.db')
    c = conn.cursor()

    c.execute('select Name from "Season ' + type + '" where Team = ? and PA > 0', (teamAbbrev,))
    fetch = c.fetchall()
    fetch.sort()
    players = []
    for pl in fetch:
        name = pl[0]
        if (name, name) not in players:
            players.append((name, name))
    players.sort()
    players.insert(0, ('All ' + teamAbbrev + ' Players', 'All ' + teamAbbrev + ' Players'))
    return players

def positions(teamAbbrev, playername):
    conn = sqlite3.connect('2021/Fielding 2021.db')
    c = conn.cursor()

    c.execute('Select Positions from "Per Game Fielding" where Team = ? and Name = ? order by date ASC', (teamAbbrev, playername))
    fetch = c.fetchall()
    positions = []
    for game in fetch:
        positions.append(game[0])
    return positions

def grabPitchData(pitcherName):
    batSide = 'All Batters'

    conn = sqlite3.connect('2021/Season Pitch Data 2021.db')
    c = conn.cursor()

    c.execute('select * from "' + batSide + '" where Name = ? and Pitch != "All Pitches"', (pitcherName,))
    fetch = c.fetchall()
    for thing in fetch:
        print(thing)

grabPitchData('Kevin Gausman')