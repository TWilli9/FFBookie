from espn_api.football import League
import pandas as pd
from ffHistoricalData import *
from ffStandMatchData import *
import matplotlib.pyplot as plt
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
        
def exportDF(df, filename='export.csv'):
    df.to_csv(filename, index = False)

import matplotlib.pyplot as plt

def plot_team_points_vs_average(standings):
    """
    Creates a bar chart comparing each team's total points to the league average.

    Args:
        standings (pd.DataFrame): A DataFrame containing team standings.
    """
    # Calculate the league average points
    league_avg_points = standings['Points For(PF)'].mean()

    # Create the plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(standings['Team Name'], standings['Points For(PF)'], color='blue', label='Team Points')
    plt.axhline(league_avg_points, color='red', linestyle='--', label='League Average')

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


#print(getStandings(league))
#print(getMatchups(currentWeek))
#print(getAllTimeData().sort_values(by = 'All-Time Record', ascending= False))
#print(getStandingsForYear(2021))
#plot_team_points_vs_average(getStandings(league))

