from espn_api.football import League

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AEAfislB6w%2BkwexCDx2g%2FTi3thxNSwE6%2BzPWVCMqnHPNGAm4DBwg4A9WY4L1euJ0umT%2FbVXUCBkyQHrhOtaWM4RrdWdQPdhNxrKBhH4a8bhO90Apuf7lubbmClqBubEJbyFxYvePyZxyBK57%2FVNUqtESc%2Fe882gjWi%2BNx7SrUxhPNUxEl51VIIVjxJyepn7oQ2Xj8WnEAlcnBjjCspWjUEib6%2FiYzDez1Qe1DEmd3CzdjEDtJuIMYwXs3QgGgZVa6ki7jqBCPQ5taoFSAWkn0FP3YoNz78XTBE%2F4mlgXRLt%2FhTXQB53phgURTeCkbxdKsTg%3D',
    swid='{CDF3A8EC-BC64-49D3-9D3D-58B609C22AA8}'
)

def get_projected_scores(week):
    matchups = league.scoreboard(week=week)
    projected_scores = []

    for matchup in matchups:
        # Get projected scores for home team
        home_team = getattr(matchup, 'home_team', None)
        home_team_name = getattr(home_team, 'team_name', "Unknown") if home_team else "Unknown"
        if home_team:
            home_projected = round(sum(player.stats.get(week, {}).get('projected_points', 0) for player in home_team.roster if player.lineupSlot not in ['BE', 'IR']), 1)
        else:
            home_projected = "N/A"

        # Get projected scores for away team
        away_team = getattr(matchup, 'away_team', None)
        away_team_name = getattr(away_team, 'team_name', "Bye") if away_team else "Bye"
        if away_team:
            away_projected = round(sum(player.stats.get(week, {}).get('projected_points', 0) for player in away_team.roster if player.lineupSlot not in ['BE', 'IR']), 1)
        else:
            away_projected = "N/A"

        projected_scores.append({
            "Team": home_team_name,
            "Projected Score": home_projected
        })
        projected_scores.append({
            "Team": away_team_name,
            "Projected Score": away_projected
        })

    return projected_scores

# Get projected scores for week 15
week_15_projected_scores = get_projected_scores(week=15)

# Display the projected scores
for score in week_15_projected_scores:
    print(f"Team: {score['Team']}, Projected Score: {score['Projected Score']}")