from espn_api.football import League
import pandas as pd
import dash
from dash import html, dash_table
from random import choice

# Initialize league connection
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

# Division mapping
division_mapping = {
    'Game of Throws': 'Xavier', 'How I Metcalf Your Mother': 'Xavier',
    'To infinity and Bijan': 'Xavier', 'Hamilton Administration ': 'Xavier',
    'First and Ted': 'Xavier', 'Team Kareem Pie 🥧': 'Ignatius',
    'The  Left Tacklers ': 'Ignatius', 'Amon a Mission': 'Ignatius',
    'Hawaii McLovins VIII': 'Ignatius', "Jared's Pack Attack": 'Ignatius'
}

# Step 1: Calculate Head-to-Head and Divisional Records
def calculate_records():
    head_to_head = {}
    divisional_records = {team: {"Wins": 0, "Losses": 0} for team in division_mapping}

    for week in range(1, 15):  # Regular season weeks
        for matchup in league.scoreboard(week=week):
            home, away = matchup.home_team, matchup.away_team
            home_score, away_score = matchup.home_score, matchup.away_score

            for team in [home.team_name, away.team_name]:
                head_to_head.setdefault(team, {})

            if home_score > away_score:
                winner, loser = home, away
            else:
                winner, loser = away, home

            head_to_head[winner.team_name][loser.team_name] = head_to_head[winner.team_name].get(loser.team_name, 0) + 1

            if division_mapping[winner.team_name] == division_mapping[loser.team_name]:
                divisional_records[winner.team_name]["Wins"] += 1
                divisional_records[loser.team_name]["Losses"] += 1

    return head_to_head, divisional_records

# Step 2: Retrieve Standings
def get_standings():
    teams = league.teams
    standings = [
        {
            'Team Name': team.team_name,
            'Record': f"{team.wins}-{team.losses}",
            'Wins': team.wins,
            'Points For': round(team.points_for),
            'Division': division_mapping.get(team.team_name, 'Unknown'),
            'Divisional Record': f"{divisional_records[team.team_name]['Wins']}-{divisional_records[team.team_name]['Losses']}"
        }
        for team in teams
    ]
    return pd.DataFrame(standings)

# Step 3: Sort with Tiebreakers
def apply_tiebreakers(df):
    def sort_by_criteria(teams):
        def tiebreak_key(team):
            head_to_head_wins = sum(head_to_head_records.get(team['Team Name'], {}).values())
            return (team['Wins'], head_to_head_wins, team['Points For'])

        return sorted(teams, key=tiebreak_key, reverse=True)

    sorted_teams = []
    for division in df['Division'].unique():
        division_teams = df[df['Division'] == division].to_dict('records')
        sorted_teams.extend(sort_by_criteria(division_teams))
    return pd.DataFrame(sorted_teams)

# Step 4: Generate Power Rankings
def generate_power_rankings(df):
    max_points = max(df['Points For'])
    rankings = [
        {
            "Team Name": row['Team Name'],
            "Power Score": round(
                0.4 * (row['Wins'] / (row['Wins'] + row['Losses'])) +
                0.5 * (row['Points For'] / max_points) +
                0.1 * (int(row['Divisional Record'].split('-')[0]) /
                       sum(map(int, row['Divisional Record'].split('-')))), 3
            ),
            "Record": row['Record'],
            "Points For": row['Points For'],
            "Divisional Record": row['Divisional Record']
        }
        for _, row in df.iterrows()
    ]
    return pd.DataFrame(sorted(rankings, key=lambda x: x['Power Score'], reverse=True))

# Prepare data
head_to_head_records, divisional_records = calculate_records()
standings_df = get_standings()
sorted_standings_df = apply_tiebreakers(standings_df)
power_rankings_df = generate_power_rankings(standings_df)

# Step 5: Build Dash App
app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
])

def create_table(df, title):
    return html.Div([
        html.H2(title, style={'text-align': 'center', 'font-family': 'Roboto'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'scroll'},
            style_cell={
                'textAlign': 'center', 'padding': '5px',
                'whiteSpace': 'normal', 'font-family': 'Roboto'
            },
        )
    ])

app.layout = html.Div([
    html.H1("Fantasy Football Dashboard", style={'text-align': 'center', 'font-family': 'Roboto'}),
    create_table(sorted_standings_df[sorted_standings_df['Division'] == 'Xavier'], "Xavier Division Standings"),
    create_table(sorted_standings_df[sorted_standings_df['Division'] == 'Ignatius'], "Ignatius Division Standings"),
    create_table(power_rankings_df, "Power Rankings")
])

if __name__ == '__main__':
    app.run_server(debug=True)
