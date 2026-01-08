from espn_api.football import League
import pandas as pd
from ffHistoricalData import *
from ffStandMatchData import *
#from ffMLModel import *
import matplotlib.pyplot as plt
import json

#import dash
#from dash import html, dcc, dash_table
#import plotly.graph_objects as go
#from random import choice  # For coin flip tiebreakers

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2025,
    espn_s2='AECfjwyt%2BaNeo%2BVJXBu5%2BGWDg3KzkvJ%2FmUcffo7x3ZSeeGTuwpdQJ%2B3W%2FNvG0J5J9hvYHZR%2B9NRSKFx4CC9kGKSdSGNKLkUpgSyQ2vxBzAculFDfSBpU%2BlYebExtCZ0ZXNxxZwEiDXy5oIsO4OFHyK%2BzZGJ%2BlEYGjfi%2BZvwUhS30YQN4cuP7qwt3I1jX4Kp3EP%2FFu%2FOywdHlYNF9UrI0YMJPn5hy9r%2F%2FSyoUQrs%2B2rhs0YDb%2Fpooiz2YnNwWFxztH4P1mB2uIlJb8yffDHGU38pk',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

currentWeek = league.current_week #change to league.current_week when in season
        
def exportDF(df, filename='export.csv'):
    df.to_csv(filename, index = False)

def plotTeamPointsVAverage(standings):
    # Calculate the league average points
    leagueAvgPoints = standings['Points For(PF)'].mean()

    # Create the plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(standings['Team Name'], standings['Points For(PF)'], color='blue', label='Team Points')
    plt.axhline(leagueAvgPoints, color='red', linestyle='--', label='League Average')

    # Add labels and title
    plt.xlabel('Team Name')
    plt.ylabel('Points For (PF)')
    plt.title('Team Points vs League Average')
    plt.xticks(rotation=45, ha='right')  # Rotate team names for better readability
    plt.legend()

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}', ha='center', va='bottom')

    # Show the plot
    plt.tight_layout()
    plt.show()


def getExpectedVsActualWins(standingsDf):
    # Extract the 'Record' column to get actual wins
    standingsDf['Actual Wins'] = standingsDf['Record'].apply(lambda x: int(x.split('-')[0]))
    
    # Select the relevant columns
    resultDf = standingsDf[['Team Name', 'Expected Wins', 'Actual Wins']]
    
    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.bar(resultDf['Team Name'], resultDf['Expected Wins'], color='blue', alpha=0.6, label='Expected Wins')
    plt.bar(resultDf['Team Name'], resultDf['Actual Wins'], color='orange', alpha=0.6, label='Actual Wins')
    plt.xlabel('Team Name')
    plt.ylabel('Wins')
    plt.title('Expected Wins vs Actual Wins')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return resultDf


# **make a seperate file just for plots

def exportDFtoJSON(df, filename):
    df.to_json(filename, orient = 'records', index = 4)

# Generate and export matchups data
matchupsDf = getMatchups(currentWeek)
exportDFtoJSON(matchupsDf, 'matchups.json')

# Generate and export standings data
standingsDf = getStandings(league)
exportDFtoJSON(standingsDf, 'standings.json')

# Generate and export historical data
historicalDf = getAllTimeData()
exportDFtoJSON(historicalDf, 'historical.json')

print("JSON files generated successfully!")


#print(getStandings(league))
#print(getMatchups(currentWeek))
#print(getAllTimeData().sort_values(by = 'All-Time Record', ascending= False))
#print(getStandingsForYear(2023))
#plot_team_points_vs_average(getStandings(league))
#get_expected_vs_actual_wins(getStandingsForYear(2023))

#exportDF(getMergedData(),'export.csv')
