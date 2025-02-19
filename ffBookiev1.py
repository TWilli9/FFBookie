from espn_api.football import League
import pandas as pd
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


def getStandings():
    #Creates a DataFrame with columns 'Team Name', 'Record', and 'Points For'. The DataFrame is sorted by best record to worst.
    teams = league.teams

    standings = [
        {
            'Team Name': team.team_name,
            'Record': f"{team.wins}-{team.losses}",
            'Points For': (team.points_for),
        }
        for team in teams
    ]

    df = pd.DataFrame(standings)
    
    return df.sort_values(by='Record',ascending=False)

print(getStandings())