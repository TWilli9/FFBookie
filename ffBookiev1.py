from espn_api.football import League
import pandas as pd
from ffProjScore import getProjectedScores
#import dash
#from dash import html, dcc, dash_table
#import plotly.graph_objects as go
#from random import choice  # For coin flip tiebreakers

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

currentWeek = 14 #change to league.current_week when in season

def getStandings():
    #Creates a DataFrame with columns 'Team Name', 'Record', 'Points For', etc. The DataFrame is sorted by best record to worst.

    teams = league.teams
    powerRankings = league.power_rankings()
    luckExp = 2.37 #exponent variable to calcualte expected wins and luck

    # Create a dictionary to map team names to their power rankings
    powerRankingsDict = {team.team_name: rank for rank, team in powerRankings}
    #Call getProjectedScores from ffProjScore
    projectedScores = getProjectedScores(currentWeek)

    standings = [
        {
            'Team Name': team.team_name,
            'Projected Scores': projectedScores.get(team.team_name, 'N/A'),
            'Record': f"{team.wins}-{team.losses}",
            'Points For(PF)': team.points_for,
            'Points Against(PA)': team.points_against,
            'PF/G': round((team.points_for) / currentWeek, 2),
            'PA/G' : round((team.points_against) / currentWeek, 2),
            'DIFF': round((team.points_for / currentWeek) - (team.points_against / currentWeek), 2),
            'Power Ranking': powerRankingsDict.get(team.team_name, 'N/A'),
            'Expected Wins': round((team.points_for ** luckExp) / (team.points_for ** luckExp + team.points_against ** luckExp) * (team.wins + team.losses), 2),
            'Luck': round(team.wins - (team.points_for ** luckExp) / (team.points_for ** luckExp + team.points_against ** luckExp) * (team.wins + team.losses), 2),
            
        }
        for team in teams
    ]

    df = pd.DataFrame(standings)
    
    return df.sort_values(by='Record',ascending=False)


def getMatchups(week):
    #Creates a DataFrame with the matchups and their data for a given week
    matchups = league.scoreboard(week=week)
    projectedScores = getProjectedScores(week)
    matchupDetails = []

    for matchup in matchups:

        homeTeam = matchup.home_team
        homeTeamName = homeTeam.team_name if homeTeam else "N/A"
        homeProj = projectedScores.get(homeTeamName, "N/A")
        homeActual = matchup.home_score if hasattr(matchup, 'home_score') else "N/A"

        awayTeam = matchup.away_team
        awayTeamName = awayTeam.team_name if awayTeam else "N/A"
        awayProj = projectedScores.get(awayTeamName, "N/A")
        awayActual = matchup.away_score if hasattr(matchup, 'away_score') else "N/A"

        if homeProj != "N/A" and awayProj != "N/A":
            if homeProj > awayProj:
                predictedWinner = homeTeamName
                margin = round(homeProj - awayProj, 2)
            else:
                predictedWinner = awayTeamName
                margin = round(awayProj - homeProj, 2)
        else:
            predictedWinner = "N/A"
            margin = "N/A"
        
        def getTopPlayers(team, week):
            if not team:
                return []
            roster = team.roster
            topPlayers = sorted(
                [player for player in roster if player.lineupSlot not in ['BE','IR']],
                key=lambda p: p.stats.get(week,{}).get('projected_points', 0),
                reverse=True
            )[:3]
            return[(player.name, player.stats.get(week, {}).get('projected_points',0)) for player in topPlayers]
        
        homeTopPlayers = getTopPlayers(homeTeam, week)
        awayTopPlayers = getTopPlayers(awayTeam,week)

        matchupDetails.append({
            'Week': week,
            'Home Team': homeTeamName,
            'Away Team': awayTeamName,
            'Home Projected Score': homeProj,
            'Away Projected Score': awayProj,
            'Home Actual Score': homeActual,
            'Away Actual Score': awayActual,
            'Predicted Winner': predictedWinner,
            'Projected Margin': margin,
            'Home Top Players': homeTopPlayers,
            'Away Top Players': awayTopPlayers,
        })

        df = pd.DataFrame(matchupDetails)

    return df
        





print(getStandings())
print(getMatchups(currentWeek))

def exportDF(df, filename='export.csv'):
    df.to_csv(filename, index = False)


