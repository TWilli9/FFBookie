from flask import Flask, render_template
from espn_api.football import League
import pandas as pd
from ffBookiev1 import getStandings, getMatchups, getAllTimeData
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

currentWeek = 14 # change to league.current_week when season is active


#Home page
@app.route('/')
def home():
    return render_template('index.html')

#Current Season Standings
@app.route('/standings')
def standings():
    standingsDf = getStandings(league)
    fig = px.bar(standingsDf, x = 'Team Name', y = 'Points For(PF)', title = 'Team Points vs League Average')
    fig.add_hline(y=standingsDf['Points For(PF)'].mean(), line_dash="dash", line_color="red")
    graphJSON = fig.to_json()
    return render_template('standings.html', graphJSON=graphJSON)


# All-Time Data
@app.route('/alltime')
def alltime():
    allTimeDf = getAllTimeData()
    fig = px.bar(allTimeDf, x='User Name', y='All-Time PF/G', title='All-Time Points For per Game')
    graphJSON = fig.to_json()
    return render_template('alltime.html', graphJSON=graphJSON)

# Weekly Matchups
@app.route('/matchups')
def matchups():
    matchupDf = getMatchups(currentWeek)
    fig = go.Figure(data=[
        go.Bar(name='Home Projected', x=matchupDf['Home Team'], y=matchupDf['Home Projected Score']),
        go.Bar(name='Away Projected', x=matchupDf['Away Team'], y=matchupDf['Away Projected Score'])
    ])
    fig.update_layout(barmode='group', title='Weekly Matchups - Projected Scores')
    graphJSON = fig.to_json()
    return render_template('matchups.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)