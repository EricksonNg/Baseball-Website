from flask import Flask, render_template, request, jsonify
from forms import HittingForm, SelectForm, PitchChartForm, LineScoreForm
import dataGrab

app = Flask('app')
app.config["SECRET_KEY"] = "1234"

@app.route('/', methods=["GET", "POST"])
@app.route("/hitting", methods = ['GET', 'POST'])
def hitting():
    team = 'SF'
    type = 'Season'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
        type = request.form.to_dict(flat=False)["cType"][0]
    except Exception as e:
        pass
    fo = SelectForm()
    fo.name.choices = dataGrab.listOfPlayers(team, "Hitting", True)
    fo.category.choices = [(c,c) for c in dataGrab.hittingCategories[type]]

    if fo.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        catType = request.form.to_dict(flat=False)["cType"][0]
        chosenCategory = request.form.to_dict(flat=False)["category"][0]
        if 'All ' in playerName and 'All ' in chosenCategory:
            return render_template("hit.html", hittingForm = fo, bothAreAll = "No charts are displayed when looking for both All Players and All Categories...yet. Any other combination would work though")
        if 'All ' not in playerName:
            if 'All Categories' not in chosenCategory:
                if catType == 'Season':
                    dates, player_category = dataGrab.seasonHitting(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = dataGrab.perGameHitting(playerTeam, playerName, chosenCategory)

                return render_template("hit.html", hittingForm = fo, player_date= dates, player_category=player_category, category= playerName + "'s " + catType + ' ' + chosenCategory)
            else:
                allCategories = {}
                for cate in fo.category.choices:
                    c = cate[0]
                    if 'All ' not in c:
                        if catType == 'Season':
                            dates, player_category = dataGrab.seasonHitting(playerTeam, playerName, c)
                            allCategories[c] = player_category
                        else:
                            dates, player_category = dataGrab.perGameHitting(playerTeam, playerName, c)
                            allCategories[c] = player_category
                return render_template("hit.html", hittingForm = fo, player_date= dates, allCategories= allCategories, player = playerName, type = catType)
        else:
            allPlayers = {}
            for pt in fo.name.choices:
                pn = pt[0]
                if 'All ' not in pn:
                    if catType == 'Season':
                        dates, player_category = dataGrab.seasonHitting(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
                    if catType == 'Per Game':
                        dates, player_category = dataGrab.perGameHitting(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
            return render_template("hit.html", hittingForm = fo, allPlayers = allPlayers, category = chosenCategory, type = catType)

    return render_template('hit.html', hittingForm= fo)

@app.route('/pitching', methods = ['GET', 'POST'])
def pitching():
    team = 'SF'
    type = 'Season'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
        type = request.form.to_dict(flat=False)["cType"][0]
    except Exception as e:
        pass
    fo = SelectForm()
    fo.name.choices = dataGrab.listOfPlayers(team, "Pitching", True)
    fo.category.choices = [(c, c) for c in dataGrab.pitchingCategories[type]]

    if fo.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        catType = request.form.to_dict(flat=False)["cType"][0]
        chosenCategory = request.form.to_dict(flat=False)["category"][0]
        if 'All ' in playerName and 'All ' in chosenCategory:
            return render_template("pitch.html", pitchForm=fo, bothAreAll="No charts are displayed when looking for both All Players and All Categories...yet. Any other combination would work though")
        if 'All ' not in playerName:
            if 'All Categories' not in chosenCategory:
                if catType == 'Season':
                    dates, player_category = dataGrab.seasonPitching(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = dataGrab.perGamePitching(playerTeam, playerName, chosenCategory)

                return render_template("pitch.html", pitchForm=fo, player_date=dates, player_category=player_category, category=playerName + "'s " + catType + ' ' + chosenCategory)
            else:
                allCategories = {}
                for cate in fo.category.choices:
                    c = cate[0]
                    if 'All ' not in c:
                        if catType == 'Season':
                            dates, player_category = dataGrab.seasonPitching(playerTeam, playerName, c)
                            allCategories[c] = player_category
                        else:
                            dates, player_category = dataGrab.perGamePitching(playerTeam, playerName, c)
                            allCategories[c] = player_category
                return render_template("pitch.html", pitchForm=fo, player_date=dates, allCategories=allCategories, player=playerName, type=catType)
        else:
            allPlayers = {}
            for pt in fo.name.choices:
                pn = pt[0]
                if 'All ' not in pn:
                    if catType == 'Season':
                        dates, player_category = dataGrab.seasonPitching(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
                    if catType == 'Per Game':
                        dates, player_category = dataGrab.perGamePitching(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
            return render_template("pitch.html", pitchForm=fo, allPlayers=allPlayers, category=chosenCategory, type=catType)

    return render_template('pitch.html', pitchForm=fo)

@app.route('/fielding', methods = ['GET', 'POST'])
def fielding():
    team = 'SF'
    type = 'Season'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
        type = request.form.to_dict(flat=False)["cType"][0]
    except Exception as e:
        pass
    fo = SelectForm()
    fo.name.choices = dataGrab.listOfPlayers(team, "Fielding", True)
    fo.category.choices = [(c, c) for c in dataGrab.fieldingCategories[type]]

    if fo.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        catType = request.form.to_dict(flat=False)["cType"][0]
        chosenCategory = request.form.to_dict(flat=False)["category"][0]
        if 'All ' in playerName and 'All ' in chosenCategory:
            return render_template("field.html", fieldForm=fo, bothAreAll="No charts are displayed when looking for both All Players and All Categories...yet. Any other combination would work though")
        if 'All ' not in playerName:
            if 'All Categories' not in chosenCategory:
                if catType == 'Season':
                    dates, player_category = dataGrab.seasonFielding(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = dataGrab.perGameFielding(playerTeam, playerName, chosenCategory)

                return render_template("field.html", fieldForm=fo, player_date=dates, player_category=player_category, category=playerName + "'s " + catType + ' ' + chosenCategory)
            else:
                allCategories = {}
                for cate in fo.category.choices:
                    c = cate[0]
                    if 'All ' not in c:
                        if catType == 'Season':
                            dates, player_category = dataGrab.seasonFielding(playerTeam, playerName, c)
                            allCategories[c] = player_category
                        else:
                            dates, player_category = dataGrab.perGameFielding(playerTeam, playerName, c)
                            allCategories[c] = player_category
                return render_template("field.html", fieldForm=fo, player_date=dates, allCategories=allCategories, player=playerName, type=catType)
        else:
            allPlayers = {}
            for pt in fo.name.choices:
                pn = pt[0]
                if 'All ' not in pn:
                    if catType == 'Season':
                        dates, player_category = dataGrab.seasonFielding(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
                    if catType == 'Per Game':
                        dates, player_category = dataGrab.perGameFielding(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
            return render_template("field.html", fieldForm=fo, allPlayers=allPlayers, category=chosenCategory, type=catType)

    return render_template('field.html', fieldForm=fo)

@app.route('/pitchCharts', methods = ['GET', 'POST'])
def pitchCharts():
    team = 'SF'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
    except Exception as e:
        pass
    pitchChartForm = PitchChartForm()
    pitchChartForm.name.choices = dataGrab.listOfPlayers(team, "Pitching", False)

    if pitchChartForm.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        batSide = request.form.to_dict(flat=False)["batSide"][0]

        pitchDataDict = dataGrab.grabPitchData(playerName, batSide)
        return render_template('pitchingCharts.html', pitchDataDict = pitchDataDict, range = range, len = len, pitchChartForm = pitchChartForm)

    return render_template('pitchingCharts.html', pitchChartForm = pitchChartForm)

@app.route('/linescores', methods = ['GET', 'POST'])
def linescores():
    from dataGrab import linePG

    team = 'SF'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
    except Exception as e:
        pass
    fo = LineScoreForm()
    fo.name.choices = dataGrab.listOfPlayers(team, "Hitting", False)

    if fo.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        lineScoreData = linePG(playerTeam, playerName)
        seasonLineData = dataGrab.seasonLine(playerTeam, playerName)
        lineScoreOrder = ['H', 'AB', 'PA', 'RBI', 'R', 'TB', '2B', '3B', 'HR', 'XBH', 'SO', 'BB', 'IBB', 'HBP', 'SB', 'CS', 'LOB', 'Sac Bunts', 'Sac Flies', 'GO', 'FO', 'GIDP', 'GITP']
        seasonLineOrder = ['AVG', 'OBP', 'SLG', 'OPS', 'BABIP', 'H', 'AB', 'PA', 'RBI', 'R', 'TB', '2B', '3B', 'HR', 'XBH', 'ISO', 'SO', 'SO%', 'BB', 'BB%', 'IBB', 'HBP', 'SB', 'CS', 'SB%', 'LOB', 'Sac Bunts', 'Sac Flies', 'GO', 'FO', 'GIDP', 'GITP']

        return render_template("linescore.html", lineScoreForm = fo, lineScoreData = lineScoreData, seasonLineData = seasonLineData, lineScoreOrder = lineScoreOrder, seasonLineOrder = seasonLineOrder, range = range, len = len)

    return render_template("linescore.html", lineScoreForm = fo)

@app.route('/hitter/<team>')
def hitter(team):
    return (jsonify({"data": dataGrab.listOfPlayers(team, "Hitting", True)}))

@app.route('/pitcher/<team>')
def pitcher(team):
    return(jsonify({"data": dataGrab.listOfPlayers(team, "Pitching", True)}))

@app.route('/fielder/<team>')
def fielder(team):
    return(jsonify({"data": dataGrab.listOfPlayers(team, "Fielding", True)}))

@app.route('/pcPitcher/<team>')
def pcPitcher(team):
    return(jsonify({"data": dataGrab.listOfPlayers(team, "Pitching", False)}))

@app.route('/lsHitter/<team>')
def lsHitter(team):
    return(jsonify({"data": dataGrab.listOfPlayers(team, "Hitting", False)}))

@app.route('/category/<sOrPg>')
def category(sOrPg):
    # It seems like javascript can only traverse through lists (hittingCategory is a dictionary of two dictionaries)
    return(jsonify({"data": list(dataGrab.hittingCategories[sOrPg].keys())}))

@app.route('/pitchCategory/<sOrPg>')
def pitchCategory(sOrPg):
    return(jsonify({"data": list(dataGrab.pitchingCategories[sOrPg].keys())}))

@app.route('/fieldCategory/<sOrPg>')
def fieldCategory(sOrPg):
    return(jsonify({"data": list(dataGrab.fieldingCategories[sOrPg].keys())}))

try:
    app.run(debug=True, use_reloader=False, port= 5001)
except Exception as e:
    print(e)