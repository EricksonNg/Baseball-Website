from flask import Flask, render_template, request, jsonify
from forms import HittingForm, SelectForm
from dataGrab import listOfPlayers, seasonHitting, perGameHitting, hittingCategories

app = Flask('app')
app.config["SECRET_KEY"] = "1234"

team = 'SF'

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
        return (jsonify({"data": listOfPlayers(team, "Hitting")}))

@app.route('/', methods=["GET", "POST"])
@app.route("/testing", methods = ['GET', 'POST'])
def testing():
    team = 'SF'
    type = 'Season'
    try:
        team = request.form.to_dict(flat=False)["team"][0]
        type = request.form.to_dict(flat=False)["cType"][0]
    except Exception as e:
        pass
    fo = SelectForm()
    fo.name.choices = listOfPlayers(team, "Hitting")
    fo.category.choices = [(c,c) for c in hittingCategories[type]]

    if fo.validate_on_submit():
        playerTeam = request.form.to_dict(flat=False)["team"][0]
        playerName = request.form.to_dict(flat=False)["name"][0]
        catType = request.form.to_dict(flat=False)["cType"][0]
        chosenCategory = request.form.to_dict(flat=False)["category"][0]
        if 'All ' not in playerName:
            if 'All Categories' not in chosenCategory:
                if catType == 'Season':
                    dates, player_category = seasonHitting(playerTeam, playerName, chosenCategory)
                else:
                    dates, player_category = perGameHitting(playerTeam, playerName, chosenCategory)

                return render_template("test.html", testForm = fo, player_date= dates, player_category=player_category, category= playerName + "'s " + catType + ' ' + chosenCategory)
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
                return render_template("test.html", testForm = fo, player_date= dates, allCategories= allCategories, player = playerName, type = catType)
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
            return render_template("test.html", testForm = fo, allPlayers = allPlayers, category = chosenCategory, type = catType)


    return render_template('test.html', testForm= fo)

@app.route('/player/<team>')
def player(team):
    return (jsonify({"data": listOfPlayers(team, "Hitting")}))

@app.route('/category/<sOrPg>')
def category(sOrPg):
    # It seems like javascript can only traverse through lists (hittingCategory is a dictionary of two dictionaries)
    return(jsonify({"data": list(hittingCategories[sOrPg].keys())}))

try:
    app.run(debug=True, use_reloader=False, port= 5001)
except Exception as e:
    print(e)