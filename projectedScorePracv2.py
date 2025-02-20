from espn_api.football import League

# Initialize league connection with your provided credentials
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

def get_projected_scores(week):
    matchups = league.scoreboard(week=week)
    projected_scores = []

    for matchup in matchups:
        # Get projected scores for home team
        home_team = getattr(matchup, 'home_team', None)
        home_team_name = getattr(home_team, 'team_name', "Unknown") if home_team else "Unknown"
        if home_team:
            home_projected = round(sum(
                player.stats.get(week, {}).get('projected_points', 0)
                for player in home_team.roster
                if player.lineupSlot not in ['BE', 'IR']
            ), 1)
        else:
            home_projected = "N/A"

        # Get projected scores for away team
        away_team = getattr(matchup, 'away_team', None)
        away_team_name = getattr(away_team, 'team_name', "Bye") if away_team else "Bye"
        if away_team:
            away_projected = round(sum(
                player.stats.get(week, {}).get('projected_points', 0)
                for player in away_team.roster
                if player.lineupSlot not in ['BE', 'IR']
            ), 1)
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

print(get_projected_scores(16))
