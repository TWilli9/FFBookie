from espn_api.football import League

league = League(
    league_id=42024189,
    year=2025,
    espn_s2='AECfjwyt%2BaNeo%2BVJXBu5%2BGWDg3KzkvJ%2FmUcffo7x3ZSeeGTuwpdQJ%2B3W%2FNvG0J5J9hvYHZR%2B9NRSKFx4CC9kGKSdSGNKLkUpgSyQ2vxBzAculFDfSBpU%2BlYebExtCZ0ZXNxxZwEiDXy5oIsO4OFHyK%2BzZGJ%2BlEYGjfi%2BZvwUhS30YQN4cuP7qwt3I1jX4Kp3EP%2FFu%2FOywdHlYNF9UrI0YMJPn5hy9r%2F%2FSyoUQrs%2B2rhs0YDb%2Fpooiz2YnNwWFxztH4P1mB2uIlJb8yffDHGU38pk',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

#This function returns a dictionary of the projected scores of each team.
def getProjectedScores(week):
    matchups = league.scoreboard(week=week)
    projectedScores = {}

    for matchup in matchups:

        #Home team projected score
        homeTeam = getattr(matchup, 'home_team', None)
        homeTeamName = getattr(homeTeam, 'team_name', "Unknown") if homeTeam else "Unknown"

        if homeTeam:
            homeProjected = round(sum(
                player.stats.get(week, {}).get('projected_points', 0)
                for player in homeTeam.roster
                if player.lineupSlot not in ['BE', 'IR']
            ), 1)
        else:
            homeProjected = 'N/A'
        
        #Away team projected score
        awayTeam = getattr(matchup, 'away_team', None)
        awayTeamName = getattr(awayTeam, 'team_name', "Unknown") if awayTeam else "Unknown"

        if awayTeam:
            awayProjected = round(sum(
                player.stats.get(week, {}).get('projected_points', 0)
                for player in awayTeam.roster
                if player.lineupSlot not in ['BE', 'IR']
            ), 1)
        else:
            awayProjected = 'N/A'

        projectedScores[homeTeamName] = homeProjected
        projectedScores[awayTeamName] = awayProjected
    
    return projectedScores
