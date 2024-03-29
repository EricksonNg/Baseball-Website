import sqlite3, operator, time

hittingCategories = {
    'Season': {'All Categories': 'All Categories', 'Average': 'AVG', 'Hits': 'Hits', 'OBP': 'OBP', 'SLG': 'SLG', 'OPS': 'OPS', 'BABIP': 'BABIP', 'Doubles': '2B', 'Triples': '3B', 'Home Runs': 'HR', 'XBH': 'XBH', 'ISO': 'ISO', 'RBI': 'RBI', 'Runs': 'Runs', 'Strike Outs': 'Strike Outs', 'K%': 'K%', 'Walks': 'Walks', 'BB%': 'BB%', 'HBP': 'HBP', 'SB': 'SB', 'CS': 'CS', 'SB%': 'SB%', 'Total Bases': 'TB', 'Left On Base': 'LOB', 'PA': 'PA', 'ABs': 'AB', 'AB/HR': 'AB/HR', 'IBB': 'IBB', 'Sac Flies': 'Sac Flies', 'Ground Outs': 'Ground Outs', 'Fly Outs': 'Fly Outs', 'Double Plays': 'Double Plays', 'Triple Plays': 'Triple Plays', 'Sac Bunts': 'Sac Bunts', 'Pickoffs': 'Pickoffs', 'Catcher Inteference': 'CI'},
    'Per Game': {'All Categories': 'All Categories', 'Hits': 'Hits', 'Doubles': '2B', 'Triples': '3B', 'Home Runs': 'HR', 'XBH': 'XBH', 'RBI': 'RBI', 'Runs': 'Runs', 'Strike Outs': 'Strike Outs', 'Walks': 'Walks', 'HBP': 'HBP', 'SB': 'SB', 'CS': 'CS', 'SB%': 'SB%', 'Total Bases': 'TB', 'LOB': 'Left On Base', 'PA': 'PA', 'ABs': 'AB', 'IBB': 'IBB', 'Sac Flies': 'Sac Flies', 'Ground Outs': 'Ground Outs', 'Fly Outs': 'Fly Outs', 'Double Plays': 'Double Plays', 'Triple Plays': 'Triple Plays', 'Sac Bunts': 'Sac Bunts', 'Pickoffs': 'Pickoffs', 'Catcher Inteference': 'CI'}
}

pitchingCategories = {
    'Season': {'All Categories': 'All Categories', 'Air Outs': 'Air Outs', 'At Bats': 'AB', 'Balks': 'Balks', 'Balls': 'Balls', 'Batters Faced': 'Batters Faced', 'BAA': 'BAA', 'Blown Saves': 'Blown Saves', 'Catchers Interferences': 'CI', 'Caught Stealings': 'CS', 'Complete Games': 'CG', 'Doubles': '2B', 'ERA': 'ERA', 'Earned Runs': 'ER', 'Games': 'G', 'Games Finished': 'Games Finished', 'Games Started': 'GS', 'Ground Outs': 'Ground Outs', 'Ground to Air': 'GO/AO', 'Hit By Pitches': 'HBP', 'Hits': 'Hits', 'Hits Per 9': 'Hits Per 9', 'Holds': 'Holds', 'Home Runs': 'HR', 'Home Runs Per 9': 'HR Per 9', 'Inherited Runners': 'IR', 'Inherited Runners Scored': 'IRS', 'Innings': 'IP', 'Intentional Walks': 'IBB', 'Losses': 'Losses', 'OBP': 'OBP', 'Outs': 'Outs', 'Pickoffs': 'Pickoffs', 'Pitches': 'Pitches', 'Pitches/IP': 'Pitches/IP', 'Runs': 'Runs', 'RBI': 'RBI', 'Runs Per 9': 'Runs Per 9', 'Sacrifice Bunts': 'Sac Bunts', 'Sacrifice Flies': 'Sac Flies', 'Save Opportunities': 'Save Opp.', 'Saves': 'Saves', 'Shut Outs': 'Shut Outs', 'SB%': 'SB%', 'Stolen Bases': 'SB', 'S%': 'S%', 'K%': 'K%', 'Strikeout To Walk': 'K/BB', 'Strike Outs': 'Strike Outs', 'Strike Outs Per 9': 'Strike Outs Per 9', 'Strikes': 'Strikes', 'Triples': '3B', 'WHIP': 'WHIP', 'Walks': 'Walks', 'Walks Per 9': 'Walks Per 9', 'Wild Pitches': 'WP', 'W%': 'Win%', 'Wins': 'Wins'},
    'Per Game': {'All Categories': 'All Categories', 'Air Outs': 'Air Outs', 'At Bats': 'AB', 'Balks': 'Balks', 'Balls': 'Balls', 'Batters Faced': 'Batters Faced', 'BAA': 'BAA', 'Blown Saves': 'Blown Saves', 'Catchers Interferences': 'CI', 'Caught Stealings': 'CS', 'Complete Games': 'CG', 'Doubles': '2B', 'Earned Runs': 'ER', 'Games Finished': 'Games Finished', 'Games Started': 'GS', 'Ground Outs': 'Ground Outs', 'Hit By Pitches': 'HBP', 'Hits': 'Hits', 'Hits Per 9': 'Hits Per 9', 'Holds': 'Holds', 'Home Runs': 'HR', 'Home Runs Per 9': 'HR Per 9', 'Inherited Runners': 'IR', 'Inherited Runners Scored': 'IRS', 'Innings': 'IP', 'Intentional Walks': 'IBB', 'Losses': 'Losses', 'Outs': 'Outs', 'Pickoffs': 'Pickoffs', 'Pitches': 'Pitches', 'Pitches/IP': 'Pitches/IP', 'Runs': 'Runs', 'RBI': 'RBI', 'Runs Per 9': 'Runs Per 9', 'Sacrifice Bunts': 'Sac Bunts', 'Sacrifice Flies': 'Sac Flies', 'Save Opportunities': 'Save Opp.', 'Saves': 'Saves', 'Shut Outs': 'Shut Outs', 'SB%': 'SB%', 'Stolen Bases': 'SB', 'S%': 'S%', 'Strike Outs': 'Strike Outs', 'Strike Outs Per 9': 'Strike Outs Per 9', 'Strikes': 'Strikes', 'Triples': '3B', 'WHIP': 'WHIP', 'Walks': 'Walks', 'Walks Per 9': 'Walks Per 9', 'Wild Pitches': 'WP', 'Wins': 'Wins'}
}

fieldingCategories = {
    'Season': {'All Categories': 'All Categories', 'Games Started': 'GS', 'Assists': 'Assists', 'Putouts': 'Putouts', 'Chances': 'Chances', 'Errors': 'Errors', 'Fielding%': 'Fielding%', 'Passed Balls': 'Passed Balls', 'Caught Stealings': 'CS', 'Stolen Bases': 'SB', 'SB%': 'SB%', 'Pickoffs': 'Pickoffs'},
    'Per Game': {'All Categories': 'All Categories', 'Games Started': 'GS', 'Assists': 'Assists', 'Putouts': 'Putouts', 'Chances': 'Chances', 'Errors': 'Errors', 'Passed Balls': 'Passed Balls', 'Caught Stealings': 'CS', 'Stolen Bases': 'SB', 'SB%': 'SB%', 'Pickoffs': 'Pickoffs'}
}

def spghp(year, teamAbbrev, playerName, catType, selectedCategory, page):
    if page == "Hitting":
        categories = hittingCategories[catType]
    elif page == "Pitching":
        categories = pitchingCategories[catType]
    else:
        categories = fieldingCategories[catType]


    conn = sqlite3.connect(year + '/' + page + ' ' + year + '.db')
    c = conn.cursor()

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "' + catType + ' ' + page + '" where Team = ? and Name = ?', (teamAbbrev, playerName))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def seasonHitting(teamAbbrev, playername, selectedCategory):
    categories = hittingCategories['Season']

    conn = sqlite3.connect('2021/Hitting 2021.db')
    c = conn.cursor()

    c.execute('Select Date, "'+ str(categories[selectedCategory]) +'" from "Season Hitting" where Team = ? and Name = ?', (teamAbbrev, playername))
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

    c.execute('Select Date, "' + categories[selectedCategory] + '" from "Per Game Hitting" where Team = ? and Name = ?', (teamAbbrev, playername))
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

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Season Pitching" where Team = ? and Name = ?',(teamAbbrev, playername))
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

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Per Game Pitching" where Team = ? and Name = ?',(teamAbbrev, playername))
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

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Season Fielding" where Team = ? and Name = ?', (teamAbbrev, playername))
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

    c.execute('Select Date, "' + str(categories[selectedCategory]) + '" from "Per Game Fielding" where Team = ? and Name = ?', (teamAbbrev, playername))
    fetch = c.fetchall()
    dates = []
    categoryList = []
    for game in fetch:
        dates.append(game[0])
        categoryList.append(game[1])
    return dates, categoryList

def listOfPlayers(year, teamAbbrev, type, needForAllPlayers):

    conn = sqlite3.connect(year + '/' + type + ' ' + year + '.db')
    c = conn.cursor()

    players = []
    if type == 'Hitting':
        c.execute('select Name from "Season ' + type + '" where Team = ? and PA > 0', (teamAbbrev,))
    if type == 'Pitching' or type == 'Fielding':
        c.execute('select Name from "Season ' + type + '" where Team = ?', (teamAbbrev,))
    fetch = c.fetchall()
    fetch.sort()
    for pl in fetch:
        name = pl[0]
        if (name, name) not in players:
            players.append((name, name))
    players.sort()
    if needForAllPlayers:
        players.insert(0, ('All ' + teamAbbrev + ' Players', 'All ' + teamAbbrev + ' Players'))
    return players

def positions(year, teamAbbrev, playername):
    conn = sqlite3.connect(year + '/Fielding ' + year + '.db')
    c = conn.cursor()

    c.execute('Select Positions from "Per Game Fielding" where Team = ? and Name = ?', (teamAbbrev, playername))
    fetch = c.fetchall()
    positions = []
    for game in fetch:
        positions.append(game[0])
    return positions

def grabPitchData(pitcherName, batSide):
    table = 'All Batters' # Only 3 options availible, and All Batters should be the default
    if 'Left' in batSide:
        table = 'LH Batters'
    elif 'Right' in batSide:
        table = 'RH Batters'

    conn = sqlite3.connect('2021/Season Pitch Data 2021.db')
    c = conn.cursor()

    c.execute('select Pitch, Amount, "Pitch%", BAA, "Whiff%", SLG, "PutAway%", "AVG EV", "AVG LA", "S%" from "' + table + '" where Name = ? and Pitch != "All Pitches" order by Amount DESC', (pitcherName,))
    fetch = c.fetchall()
    pitchDataDict = {'pitchTypes': [], 'pitchAmounts': [], 'pitchPercentages': [], 'BAA': [], 'whiffPercentages': [], 'SLG': [], 'putAwayPercentages': [], 'avgEV': [], 'avgLA': [], 'strikePercentages': []}
    for thing in fetch:
        pitchDataDict['pitchTypes'].append(thing[0])
        pitchDataDict['pitchAmounts'].append(thing[1])
        pitchDataDict['pitchPercentages'].append(round(thing[2]*100,1))
        pitchDataDict['BAA'].append(thing[3])
        pitchDataDict['whiffPercentages'].append(round(thing[4]*100,1))
        pitchDataDict['SLG'].append(thing[5])
        pitchDataDict['putAwayPercentages'].append(round(thing[6]*100,1))
        pitchDataDict['avgEV'].append(thing[7])
        pitchDataDict['avgLA'].append(thing[8])
        pitchDataDict['strikePercentages'].append(round(thing[9]*100,1))
    return pitchDataDict

def linePG(year, teamAbbrev, playername):
    labelsInDB = ['Hits', 'AB', 'PA', 'RBI', 'Runs', 'TB', '"2B"', '"3B"', 'HR', 'XBH', 'Strike Outs', 'Walks', 'IBB', 'HBP', 'SB', 'CS', 'LOB', '"Sac Bunts"', '"Sac Flies"', '"Ground Outs"', '"Fly Outs"', '"Double Plays"', '"Triple Plays"']
    # cString = ""
    # for i in range(len(labelsInDB)):
    #     cString += labelsInDB[i]
    #     if i != len(labelsInDB)-1:
    #         cString += ", "
    # print(cString)

    conn = sqlite3.connect(year + '/Hitting ' + year + '.db')
    c = conn.cursor()

    c.execute('Select Date, Hits, AB, PA, RBI, Runs, TB, "2B", "3B", HR, XBH, "Strike Outs", Walks, IBB, HBP, SB, CS, LOB, "Sac Bunts", "Sac Flies", "Ground Outs", "Fly Outs", "Double Plays", "Triple Plays" from "Per Game Hitting" where Name = ? and Team = ?', (playername, teamAbbrev))
    stats = c.fetchall()

    field = sqlite3.connect(year + '/Fielding ' + year + '.db')
    f = field.cursor()

    f.execute('Select Date, Positions from "Per Game Fielding" where Name = ? and Team = ?', (playername, teamAbbrev))
    positions = f.fetchall()

    lines = []
    for i in range(len(stats)):
        tTol = list(stats[i])
        positionsOnDate = positions[i][1]
        tTol.insert(1, positionsOnDate)
        lines.append(tTol)
    # print(lines)

    return lines

def seasonLine(year, teamAbbrev, playername):
    labelsInDB = ['AVG', 'OBP', 'SLG', 'OPS', 'BABIP', 'Hits', 'AB', 'PA', 'RBI', 'Runs', 'TB', '"2B"', '"3B"', 'HR', 'XBH', 'ISO', 'Strike Outs', '"K%"', 'BB', '"BB%"', 'IBB', 'HBP', 'SB', 'CS', '"SB%"', 'LOB', '"Sac Bunts"', '"Sac Flies"', '"Ground Outs"', '"Fly Outs"', '"Double Plays"', '"Triple Plays"']
    # cString = ""
    # for i in range(len(labelsInDB)):
    #     cString += labelsInDB[i]
    #     if i != len(labelsInDB)-1:
    #         cString += ", "
    # print(cString)

    conn = sqlite3.connect(year + '/Hitting ' + year + '.db')
    c = conn.cursor()

    c.execute('Select AVG, OBP, SLG, OPS, BABIP, Hits, AB, PA, RBI, Runs, TB, "2B", "3B", HR, XBH, ISO, "Strike Outs", "K%", Walks, "BB%", IBB, HBP, SB, CS, "SB%", LOB, "Sac Bunts", "Sac Flies", "Ground Outs", "Fly Outs", "Double Plays", "Triple Plays" from "Season Hitting" where Name = ? and Team = ? order by Date DESC', (playername, teamAbbrev))
    stats = list(c.fetchone())

    return stats

def teamLeaders(year, teamAbbrev, hittingOrPitching):
    if hittingOrPitching == "Hitting":
        categories = hittingCategories['Season']
    else:
        categories = pitchingCategories['Season']

    conn = sqlite3.connect(year + '/' + hittingOrPitching + ' ' + year + '.db')
    c = conn.cursor()

    selectedCategory = "Average"
    all = {}

    for ca in categories:
        if 'All ' not in ca:
            found = {}
            if hittingOrPitching == 'Hitting':
                c.execute('Select Date, PA, Name, "' + str(categories[ca]) + '" from "Season Hitting" where Team = ? order by date DESC', (teamAbbrev,))
                for game in c.fetchall():
                    plateAppearances = game[1]
                    name = game[2]
                    stat = game[3]
                    if name not in found:
                        found[name] = [stat, plateAppearances]
            if hittingOrPitching == 'Pitching':
                c.execute('Select Date, IP, Name, "' + str(categories[ca]) + '" from "Season Pitching" where Team = ? order by date DESC', (teamAbbrev,))
                for game in c.fetchall():
                    innings = game[1]
                    name = game[2]
                    stat = game[3]
                    if name not in found:
                        found[name] = [stat, innings]
            sorted_found = sorted(found.items(), key=operator.itemgetter(1), reverse=True)
            all[ca] = sorted_found

    return all

# print(teamLeaders("SF", "Pitching"))