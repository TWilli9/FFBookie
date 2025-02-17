from espn_api.football import League
import pandas as pd
import dash
from dash import html, dcc, dash_table
import plotly.graph_objects as go
from random import choice  # For coin flip tiebreaker
from projectedScorePracv2 import get_projected_scores  # Import from external script

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AEAfislB6w%2BkwexCDx2g%2FTi3thxNSwE6%2BzPWVCMqnHPNGAm4DBwg4A9WY4L1euJ0umT%2FbVXUCBkyQHrhOtaWM4RrdWdQPdhNxrKBhH4a8bhO90Apuf7lubbmClqBubEJbyFxYvePyZxyBK57%2FVNUqtESc%2Fe882gjWi%2BNx7SrUxhPNUxEl51VIIVjxJyepn7oQ2Xj8WnEAlcnBjjCspWjUEib6%2FiYzDez1Qe1DEmd3CzdjEDtJuIMYwXs3QgGgZVa6ki7jqBCPQ5taoFSAWkn0FP3YoNz78XTBE%2F4mlgXRLt%2FhTXQB53phgURTeCkbxdKsTg%3D',
    swid='{CDF3A8EC-BC64-49D3-9D3D-58B609C22AA8}'
)


# Define division mapping for each team
division_mapping = {
    'Game of Throws': 'Xavier',
    'How I Metcalf Your Mother': 'Xavier',
    'To infinity and Bijan': 'Xavier',
    'Hamilton Administration ': 'Xavier',
    'First and Ted': 'Xavier',
    'Team Kareem Pie 🥧': 'Ignatius',
    'The  Left Tacklers ': 'Ignatius',
    'Amon a Mission': 'Ignatius',
    'Hawaii McLovins VIII': 'Ignatius',
    "Jared's Pack Attack": 'Ignatius'
}

# Calculate Head-to-Head and Divisional Records
def calculate_records():
    head_to_head = {}
    divisional_records = {team_name: {"Wins": 0, "Losses": 0} for team_name in division_mapping.keys()}

    # Assume there are 14 weeks in the regular season
    for week in range(1, 15):
        matchups = league.scoreboard(week=week)

        for matchup in matchups:
            team1 = matchup.home_team
            team2 = matchup.away_team
            team1_score = matchup.home_score
            team2_score = matchup.away_score

            if team1.team_name not in head_to_head:
                head_to_head[team1.team_name] = {}
            if team2.team_name not in head_to_head:
                head_to_head[team2.team_name] = {}

            if team1_score > team2_score:
                head_to_head[team1.team_name][team2.team_name] = head_to_head[team1.team_name].get(team2.team_name, 0) + 1
                if division_mapping[team1.team_name] == division_mapping[team2.team_name]:
                    divisional_records[team1.team_name]["Wins"] += 1
                    divisional_records[team2.team_name]["Losses"] += 1
            elif team2_score > team1_score:
                head_to_head[team2.team_name][team1.team_name] = head_to_head[team2.team_name].get(team1.team_name, 0) + 1
                if division_mapping[team1.team_name] == division_mapping[team2.team_name]:
                    divisional_records[team2.team_name]["Wins"] += 1
                    divisional_records[team1.team_name]["Losses"] += 1

    return head_to_head, divisional_records

# Get the head-to-head and divisional records
head_to_head_records, divisional_records = calculate_records()

# Retrieve and Process Standings Data with Divisional Records
def get_standings():
    teams = league.teams
    data = []

    for team in teams:
        team_data = {
            'Team Name': team.team_name,
            'Record': f"{team.wins}-{team.losses}",
            'Wins': team.wins,  # Store separate Wins for sorting
            'Points For': round(team.points_for),
            'Division': division_mapping.get(team.team_name, 'Unknown'),
            'Divisional Record': f"{divisional_records[team.team_name]['Wins']}-{divisional_records[team.team_name]['Losses']}"
        }
        data.append(team_data)

    standings_df = pd.DataFrame(data)
    return standings_df

# Generate standings with divisional records
standings_df = get_standings()

#Apply Custom Tiebreakers Using Head-to-Head and Points For
def apply_tiebreakers(standings_df):
    def sort_teams(teams):
        sorted_teams = []
        teams_by_record = {}

        for team in teams:
            record = team['Wins']  # Using Wins for sorting
            teams_by_record.setdefault(record, []).append(team)

        for record, tied_teams in sorted(teams_by_record.items(), reverse=True):
            if len(tied_teams) == 1:
                sorted_teams.extend(tied_teams)
            elif len(tied_teams) == 2:
                team1, team2 = tied_teams
                team1_wins_vs_team2 = head_to_head_records.get(team1['Team Name'], {}).get(team2['Team Name'], 0)
                team2_wins_vs_team1 = head_to_head_records.get(team2['Team Name'], {}).get(team1['Team Name'], 0)
                if team1_wins_vs_team2 > team2_wins_vs_team1:
                    sorted_teams.extend([team1, team2])
                elif team2_wins_vs_team1 > team1_wins_vs_team2:
                    sorted_teams.extend([team2, team1])
                elif team1['Points For'] > team2['Points For']:
                    sorted_teams.extend([team1, team2])
                elif team2['Points For'] > team1['Points For']:
                    sorted_teams.extend([team2, team1])
                else:
                    sorted_teams.extend([team1, team2] if choice([True, False]) else [team2, team1])
            else:
                tied_teams.sort(
                    key=lambda x: (
                        sum(head_to_head_records.get(x['Team Name'], {}).values()),
                        x['Points For']
                    ),
                    reverse=True
                )
                sorted_teams.extend(tied_teams)

        return sorted_teams

    xavier_teams = standings_df[standings_df['Division'] == 'Xavier'].to_dict('records')
    ignatius_teams = standings_df[standings_df['Division'] == 'Ignatius'].to_dict('records')

    sorted_xavier = sort_teams(xavier_teams)
    sorted_ignatius = sort_teams(ignatius_teams)

    return pd.DataFrame(sorted_xavier + sorted_ignatius)

# Apply tiebreakers and get sorted standings
sorted_standings_df = apply_tiebreakers(standings_df)


# Step 6: Build the Dash App
app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
])


# Step 7: Generate Power Rankings

# Add the "FP Rankings" data to standings_df
fp_rankings_data = {
    'Team Name': [
        'Team Kareem Pie 🥧', 'The  Left Tacklers ', 'First and Ted',
        "Jared's Pack Attack", 'Hawaii McLovins VIII', 'Amon a Mission',
        'Hamilton Administration ', 'Game of Throws', 'To infinity and Bijan',
        'How I Metcalf Your Mother'
    ],
    'FP Score': [100, 94, 92, 89, 88, 84, 82, 82, 81, 79]
}

fp_rankings_df = pd.DataFrame(fp_rankings_data)
standings_df = standings_df.merge(fp_rankings_df, on="Team Name", how="left")

# Include all-time win percentage data
all_time_data = {
    "Team Name": [
        'The  Left Tacklers ', 'First and Ted', 'Hamilton Administration ', 'Hawaii McLovins VIII',
        'How I Metcalf Your Mother', "Jared's Pack Attack", 'Team Kareem Pie 🥧',
        'Game of Throws', 'To infinity and Bijan', 'Amon a Mission'
    ],
    "All-Time Playoff Win %": [0.5556, 0.4, 1.0, 0.6, 0.25, 0.25, 0.5, 0.8, 0.0, 0.0],
    "All-Time Regular Season Win %": [0.6087, 0.5797, 0.5652, 0.5362, 0.5362, 0.5072, 0.4493, 0.4928, 0.4638, 0.3913]
}

# Convert to DataFrame
all_time_df = pd.DataFrame(all_time_data)

# Include poll data
poll_data = {
    "Team Name": [
        "Game of Throws", "The  Left Tacklers ", "To infinity and Bijan", 
        "Amon a Mission", "First and Ted", "Jared's Pack Attack", 
        "Hamilton Administration ", "Team Kareem Pie 🥧", 
        "How I Metcalf Your Mother", "Hawaii McLovins VIII"
    ],
    "Average Ranking": [2.375, 3.125, 4, 5.375, 2.125, 5.75, 6, 5.5, 8.5, 8]
}

# Merge all-time data with standings_df
standings_df = standings_df.merge(all_time_df, on="Team Name", how="left")

# Update the power rankings calculation
def generate_power_rankings(standings_df):
    # Assign weights to the metrics
    weights = {
        "record": 0.2,       # 20% weight for current season record
        "points_for": 0.3,  # 25% weight for points for
        "divisional_record": 0.05,  # 10% weight for divisional record
        "fp_score": 0.35,    # 25% weight for FP Score
        "playoff_win_pct": 0.05,  # 10% weight for playoff win percentage
        "regular_season_win_pct": 0.05  # 10% weight for regular season win percentage
    }

    # Calculate power score for each team
    power_rankings = []
    for _, row in standings_df.iterrows():
        # Extract record as a win percentage
        wins, losses = map(int, row['Record'].split('-'))
        win_percentage = wins / (wins + losses) if (wins + losses) > 0 else 0

        # Extract divisional record as a win percentage
        div_wins, div_losses = map(int, row['Divisional Record'].split('-'))
        div_win_percentage = div_wins / (div_wins + div_losses) if (div_wins + div_losses) > 0 else 0

        # Compute the power score
        power_score = (
            weights["record"] * win_percentage +
            weights["points_for"] * (row['Points For'] / max(standings_df['Points For'])) +
            weights["divisional_record"] * div_win_percentage +
            weights["fp_score"] * (row['FP Score'] / max(standings_df['FP Score'])) +
            weights["playoff_win_pct"] * row['All-Time Playoff Win %'] +
            weights["regular_season_win_pct"] * row['All-Time Regular Season Win %']
        )

        power_rankings.append({
            "Team Name": row['Team Name'],
            "Power Score": round(power_score, 3),
            "FP Score": row['FP Score'],
            "Record": row['Record'],
            "Points For": row['Points For'],
            "Divisional Record": row['Divisional Record'],
            "All-Time Playoff Win %": row['All-Time Playoff Win %'],
            "All-Time Regular Season Win %": row['All-Time Regular Season Win %']
        })

    # Sort teams by power score in descending order
    power_rankings = sorted(power_rankings, key=lambda x: x['Power Score'], reverse=True)

    return pd.DataFrame(power_rankings)


# Generate and display updated power rankings
power_rankings_df = generate_power_rankings(standings_df)

# Function to fetch projected scores
def fetch_weekly_projected_scores(week):
    return pd.DataFrame(get_projected_scores(week=week))

# Generate Week 15 matchups data
week_15_projected_scores_df = fetch_weekly_projected_scores(week=15)

def calculate_odds_from_probability(probability):
    """
    Convert probability (0-100 scale) into American odds (-110, +200, etc.).
    """
    if probability <= 0:
        return "+Infinity"  # Impossible event
    if probability >= 100:
        return "-Infinity"  # Certain event

    if probability > 50:
        odds = -100 * (probability / (100 - probability))
    else:
        odds = 100 * ((100 - probability) / probability)

    odds = round(odds)
    return f"+{odds}" if odds > 0 else str(odds)


current_week = 15
weekly_projected_scores = get_projected_scores(week=current_week)

max_poll_rank = 10  # Assuming rankings are from 1 to 10

weights = {
    'power': 1,        # Default weight for power score
    'poll': 0.5,       # Lower weight for poll rankings
    'projected': 1.5   # Higher weight for projected scores
}


# Calculate Odds from probabilities
def calculate_odds(home_power_score, away_power_score, home_poll, away_poll, max_poll_rank, home_projected_score, away_projected_score, weights):
    """
    Calculate odds and probabilities considering power scores, poll rankings, and projected scores.
    """
    # Ensure poll rankings are integers or default to a high value (e.g., max_poll_rank + 1) if not valid
    try:
        home_poll_rank = int(home_poll)
    except (ValueError, TypeError):
        home_poll_rank = max_poll_rank  # Default to a rank lower than the worst possible rank

    try:
        away_poll_rank = int(away_poll)
    except (ValueError, TypeError):
        away_poll_rank = max_poll_rank  # Default to a rank lower than the worst possible rank

    # Calculate poll influences
    home_poll_influence = (max_poll_rank - home_poll_rank) / max_poll_rank if max_poll_rank > 0 else 0
    away_poll_influence = (max_poll_rank - away_poll_rank) / max_poll_rank if max_poll_rank > 0 else 0

    # Adjust power scores with weights
    power_weight = weights.get('power', 1)  # Default to 1 if not specified
    poll_weight = weights.get('poll', 1)   # Default to 1 if not specified
    projected_weight = weights.get('projected', 1)  # Weight for projected scores

    home_adjusted_score = (
        (home_power_score * power_weight) + 
        (home_poll_influence * poll_weight) + 
        (home_projected_score * projected_weight)
    )

    away_adjusted_score = (
        (away_power_score * power_weight) + 
        (away_poll_influence * poll_weight) + 
        (away_projected_score * projected_weight)
    )

    # Calculate probabilities
    total_score = home_adjusted_score + away_adjusted_score
    home_prob = home_adjusted_score / total_score if total_score > 0 else 0.5
    away_prob = away_adjusted_score / total_score if total_score > 0 else 0.5

    # Normalize probabilities
    prob_sum = home_prob + away_prob
    home_prob /= prob_sum
    away_prob /= prob_sum

    home_prob = round(home_prob * 100, 2)  # Convert to percentage and round to 2 decimal places
    away_prob = round(away_prob * 100, 2)  # Convert to percentage and round to 2 decimal places

    # Calculate odds
    home_odds = calculate_odds_from_probability(home_prob)
    away_odds = calculate_odds_from_probability(away_prob)

    return home_prob, away_prob, home_odds, away_odds




# Process the matchups to include pairings and projected scores
matchups_with_projections = []
for i in range(0, len(weekly_projected_scores), 2):
    home_team = weekly_projected_scores[i]
    away_team = weekly_projected_scores[i + 1]

    # Fetch poll rankings and power scores
    home_power_score = power_rankings_df.loc[power_rankings_df['Team Name'] == home_team['Team'], 'Power Score']
    home_power_score = home_power_score.values[0] if not home_power_score.empty else 0  # Default to 0 if no match found

    away_power_score = power_rankings_df.loc[power_rankings_df['Team Name'] == away_team['Team'], 'Power Score']
    away_power_score = away_power_score.values[0] if not away_power_score.empty else 0  # Default to 0 if no match found

    home_poll_rank = poll_data.get(home_team['Team'], 'N/A')
    away_poll_rank = poll_data.get(away_team['Team'], 'N/A')


    # Calculate probabilities and odds
    home_prob, away_prob, home_odds, away_odds = calculate_odds(
    home_power_score,
    away_power_score,
    home_poll_rank,
    away_poll_rank,
    max_poll_rank,
    home_projected,
    away_projected_score,
    weights  # Ensure weights is a dictionary
    )



    matchups_with_projections.append({
        "Matchup": f"{home_team['Team']} vs {away_team['Team']}",
        "Home Team": home_team['Team'],
        "Home Projected": home_team['Projected Score'],
        "Away Team": away_team['Team'],
        "Away Projected": away_team['Projected Score'],
        "Home Win %": f"{home_prob}%",
        "Away Win %": f"{away_prob}%",
        "Home Odds": home_odds,
        "Away Odds": away_odds
    })

# Convert the result into a DataFrame for Dash display
matchups_df = pd.DataFrame(matchups_with_projections)


# Update the Dash table to include new columns
app.layout = html.Div([
    html.H1("Fantasy Football Dashboard", style={'text-align': 'center', 'font-family': 'Roboto'}),

    html.Div([
        html.H2("Power Rankings", style={'text-align': 'center', 'font-family': 'Roboto'}),
        dash_table.DataTable(
            data=power_rankings_df.to_dict('records'),
            columns=[
                {"name": i, "id": i} for i in [
                    'Team Name', 'Power Score', 'FP Score', 'Record', 'Points For', 'Divisional Record',
                    'All-Time Playoff Win %', 'All-Time Regular Season Win %'
                ]
            ],
            style_table={'overflowX': 'scroll'},
            style_cell={
                'textAlign': 'center',
                'padding': '5px',
                'whiteSpace': 'normal',
                'font-family': 'Roboto'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Team Name'}, 'width': '20%'},
                {'if': {'column_id': 'Power Score'}, 'width': '15%'},
                {'if': {'column_id': 'FP Score'}, 'width': '10%'},
                {'if': {'column_id': 'Record'}, 'width': '10%'},
                {'if': {'column_id': 'Points For'}, 'width': '10%'},
                {'if': {'column_id': 'Divisional Record'}, 'width': '10%'},
                {'if': {'column_id': 'All-Time Playoff Win %'}, 'width': '10%'},
                {'if': {'column_id': 'Regular Season Win %'}, 'width': '10%'},
            ]
        ),
    ]),

    html.Div([
    html.H2(f"Week {current_week} Matchups and Projected Scores", style={'text-align': 'center', 'font-family': 'Roboto'}),
    dash_table.DataTable(
        data=matchups_df.to_dict('records'),
        columns=[
            {"name": "Matchup", "id": "Matchup"},
            {"name": "Home Team", "id": "Home Team"},
            {"name": "Home Projected", "id": "Home Projected"},
            {"name": "Away Team", "id": "Away Team"},
            {"name": "Away Projected", "id": "Away Projected"},
            {"name": "Home Win %", "id": "Home Win %"},
            {"name": "Away Win %", "id": "Away Win %"},
            {"name": "Home Odds", "id": "Home Odds"},
            {"name": "Away Odds", "id": "Away Odds"},
        ],
        style_table={'overflowX': 'scroll'},
        style_cell={
            'textAlign': 'center',
            'padding': '5px',
            'whiteSpace': 'normal',
            'font-family': 'Roboto'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Matchup'}, 'width': '20%'},
            {'if': {'column_id': 'Home Team'}, 'width': '15%'},
            {'if': {'column_id': 'Home Projected'}, 'width': '10%'},
            {'if': {'column_id': 'Away Team'}, 'width': '15%'},
            {'if': {'column_id': 'Away Projected'}, 'width': '10%'},
            {'if': {'column_id': 'Home Win %'}, 'width': '10%'},
            {'if': {'column_id': 'Away Win %'}, 'width': '10%'},
            {'if': {'column_id': 'Home Odds'}, 'width': '10%'},
            {'if': {'column_id': 'Away Odds'}, 'width': '10%'},
        ]
    ),
]),

])

if __name__ == '__main__':
    app.run_server(debug=True)


