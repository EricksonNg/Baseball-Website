from flask import Flask, render_template, request, jsonify
from forms import HittingForm, SelectForm, PitchChartForm
from dataGrab import listOfPlayers, seasonHitting, perGameHitting, hittingCategories, grabPitchData, pitchingCategories, seasonPitching, perGamePitching

app = Flask('app')
app.config["SECRET_KEY"] = "1234"


#first team form
@app.route("/getdata3/<types>")
def resend_selectionForm_data3(types):
    global team
    page = "Hitting"
    # print("The team from form:", types)

    if page == "Hitting":
        team = types
        # print("This means that team now is:", team)

        # the jsonify function is part of the Flask library and it needs to be imported
        return (jsonify({"data": listOfPlayers(team, "Hitting", False)}))

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
    fo.name.choices = listOfPlayers(team, "Hitting", False)
    fo.category.choices = [(c,c) for c in hittingCategories[type]]

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
                    dates, player_category = seasonHitting(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = perGameHitting(playerTeam, playerName, chosenCategory)

                return render_template("hit.html", hittingForm = fo, player_date= dates, player_category=player_category, category= playerName + "'s " + catType + ' ' + chosenCategory)
            else:
                allCategories = {}
                for cate in fo.category.choices:
                    c = cate[0]
                    if 'All ' not in c:
                        if catType == 'Season':
                            dates, player_category = seasonHitting(playerTeam, playerName, c)
                            allCategories[c] = player_category
                        else:
                            dates, player_category = perGameHitting(playerTeam, playerName, c)
                            allCategories[c] = player_category
                return render_template("hit.html", hittingForm = fo, player_date= dates, allCategories= allCategories, player = playerName, type = catType)
        else:
            allPlayers = {}
            for pt in fo.name.choices:
                pn = pt[0]
                if 'All ' not in pn:
                    if catType == 'Season':
                        dates, player_category = seasonHitting(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
                    if catType == 'Per Game':
                        dates, player_category = perGameHitting(playerTeam, pn, chosenCategory)
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
    fo.name.choices = listOfPlayers(team, "Pitching", True)
    fo.category.choices = [(c, c) for c in pitchingCategories[type]]

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
                    dates, player_category = seasonPitching(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = perGamePitching(playerTeam, playerName, chosenCategory)

                return render_template("pitch.html", pitchForm=fo, player_date=dates, player_category=player_category, category=playerName + "'s " + catType + ' ' + chosenCategory)
            else:
                allCategories = {}
                for cate in fo.category.choices:
                    c = cate[0]
                    if 'All ' not in c:
                        if catType == 'Season':
                            dates, player_category = seasonPitching(playerTeam, playerName, c)
                            allCategories[c] = player_category
                        else:
                            dates, player_category = perGamePitching(playerTeam, playerName, c)
                            allCategories[c] = player_category
                return render_template("pitch.html", pitchForm=fo, player_date=dates, allCategories=allCategories, player=playerName, type=catType)
        else:
            allPlayers = {}
            for pt in fo.name.choices:
                pn = pt[0]
                if 'All ' not in pn:
                    if catType == 'Season':
                        dates, player_category = seasonPitching(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
                    if catType == 'Per Game':
                        dates, player_category = perGamePitching(playerTeam, pn, chosenCategory)
                        allPlayers[pn] = {'stats': player_category, 'dates': dates}
            return render_template("pitch.html", pitchForm=fo, allPlayers=allPlayers, category=chosenCategory, type=catType)

    return render_template('pitch.html', pitchForm=fo)

@app.route('/pitchCharts', methods = ['GET', 'POST'])
def pitchCharts():
    team = 'SF'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
    except Exception as e:
        pass
    pitchChartForm = PitchChartForm()
    pitchChartForm.name.choices = listOfPlayers(team, "Pitching", False)

    if pitchChartForm.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        batSide = request.form.to_dict(flat=False)["batSide"][0]

        pitchDataDict = grabPitchData(playerName, batSide)
        return render_template('pitchingCharts.html', pitchDataDict = pitchDataDict, range = range, len = len, pitchChartForm = pitchChartForm)

    return render_template('pitchingCharts.html', pitchChartForm = pitchChartForm)

@app.route('/hitter/<team>')
def hitter(team):
    return (jsonify({"data": listOfPlayers(team, "Hitting", False)}))

@app.route('/pitcher/<team>')
def pitcher(team):
    return(jsonify({"data": listOfPlayers(team, "Pitching", True)}))

@app.route('/pcPitcher/<team>')
def pcPitcher(team):
    return(jsonify({"data": listOfPlayers(team, "Pitching", False)}))

@app.route('/category/<sOrPg>')
def category(sOrPg):
    # It seems like javascript can only traverse through lists (hittingCategory is a dictionary of two dictionaries)
    return(jsonify({"data": list(hittingCategories[sOrPg].keys())}))

@app.route('/pitchCategory/<sOrPg>')
def pitchCategory(sOrPg):
    return(jsonify({"data": list(pitchingCategories[sOrPg].keys())}))

try:
    app.run(debug=True, use_reloader=False, port= 5001)
except Exception as e:
    print(e)