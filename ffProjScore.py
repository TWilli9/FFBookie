from espn_api.football import League

league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
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
