from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class HittingForm(FlaskForm):
    team = StringField("Team: ", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    category = StringField("Category: ", validators=[DataRequired()])
    submit = SubmitField("Find")  # the parameter is the label on the button

class SelectForm(FlaskForm):
    team = SelectField("Team: ", choices = [('ARI', 'ARI'), ('ATL', 'ATL'), ('BAL', 'BAL'), ('BOS', 'BOS'), ('CHC', 'CHC'), ('CIN', 'CIN'), ('CLE', 'CLE'), ('COL', 'COL'), ('CWS', 'CWS'), ('DET', 'DET'), ('HOU', 'HOU'), ('KC', 'KC'), ('LAA', 'LAA'), ('LAD', 'LAD'), ('MIA', 'MIA'), ('MIL', 'MIL'), ('MIN', 'MIN'), ('NYM', 'NYM'), ('NYY', 'NYY'), ('OAK', 'OAK'), ('PHI', 'PHI'), ('PIT', 'PIT'), ('SD', 'SD'), ('SEA', 'SEA'), ('SF', 'SF'), ('STL', 'STL'), ('TB', 'TB'), ('TEX', 'TEX'), ('TOR', 'TOR'), ('WSH', 'WSH')], validators=[DataRequired()], default= 'SF')
    name = SelectField("Player: ", choices= [], validators=[DataRequired()])
    cType = SelectField("Type: ", choices = [('Season', 'Season'), ('Per Game', 'Per Game')])
    category = SelectField("Category: ", choices = [], validators=[DataRequired()])
    submit = SubmitField("Find")

class PitchChartForm(FlaskForm):
    team = SelectField("Team: ", choices = [('ARI', 'ARI'), ('ATL', 'ATL'), ('BAL', 'BAL'), ('BOS', 'BOS'), ('CHC', 'CHC'), ('CIN', 'CIN'), ('CLE', 'CLE'), ('COL', 'COL'), ('CWS', 'CWS'), ('DET', 'DET'), ('HOU', 'HOU'), ('KC', 'KC'), ('LAA', 'LAA'), ('LAD', 'LAD'), ('MIA', 'MIA'), ('MIL', 'MIL'), ('MIN', 'MIN'), ('NYM', 'NYM'), ('NYY', 'NYY'), ('OAK', 'OAK'), ('PHI', 'PHI'), ('PIT', 'PIT'), ('SD', 'SD'), ('SEA', 'SEA'), ('SF', 'SF'), ('STL', 'STL'), ('TB', 'TB'), ('TEX', 'TEX'), ('TOR', 'TOR'), ('WSH', 'WSH')], validators=[DataRequired()], default= 'SF')
    name = SelectField("Player: ", choices= [], validators=[DataRequired()])
    batSide = SelectField("Bat Side: ", choices = [('All Batters','All Batters'),('Left-Handed','Left-Handed'),('Right-Handed','Right-Handed')])
    submit = SubmitField("Find")

class LineScoreForm(FlaskForm):
    team = SelectField("Team: ", choices=[('ARI', 'ARI'), ('ATL', 'ATL'), ('BAL', 'BAL'), ('BOS', 'BOS'), ('CHC', 'CHC'), ('CIN', 'CIN'), ('CLE', 'CLE'), ('COL', 'COL'), ('CWS', 'CWS'), ('DET', 'DET'), ('HOU', 'HOU'), ('KC', 'KC'), ('LAA', 'LAA'), ('LAD', 'LAD'), ('MIA', 'MIA'), ('MIL', 'MIL'), ('MIN', 'MIN'), ('NYM', 'NYM'), ('NYY', 'NYY'), ('OAK', 'OAK'), ('PHI', 'PHI'), ('PIT', 'PIT'), ('SD', 'SD'), ('SEA', 'SEA'), ('SF', 'SF'), ('STL', 'STL'), ('TB', 'TB'), ('TEX', 'TEX'), ('TOR', 'TOR'), ('WSH', 'WSH')], validators=[DataRequired()], default='SF')
    name = SelectField("Player: ", choices=[], validators=[DataRequired()])
    submit = SubmitField("Find")