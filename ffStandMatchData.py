from espn_api.football import League
import pandas as pd
from ffProjScore import getProjectedScores
from ffLuckModel import calculateLuckScore

league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

currentWeek = 14 # change to league.current_week when season is active

def calculateSOS(league,currentWeek):
    #Calculates the Strength of Schedule (SOS) for each team
    teams = league.teams
    sosData = []

    for team in teams:
        matchups = []
        for week in range(1, currentWeek + 1):
            for matchup in league.scoreboard(week=week):
                if matchup.home_team == team:
                    matchups.append(matchup.away_team)
                elif matchup.away_team == team:
                    matchups.append(matchup.home_team)

        totalOppPoints = sum(opponent.points_for for opponent in matchups)
        avgOppPoints = totalOppPoints / len(matchups) if matchups else 0

        sosData.append({

            'Team Name' : team.team_name,
            'SOS' : round(avgOppPoints, 2),

        })
    return pd.DataFrame(sosData)


def getLuckScoresAcrossWeeks(startweek = 1, endweek = 14): #change endweek to league.current_week when season is active
    #Calculates the luck scores for each team across multiple weeks
    allWeeks = []

    for week in range(startweek, endweek + 1):
        try:
            matchups_df = getMatchups(week)
            weekScores = calculateLuckScore(matchups_df)
            allWeeks.append(weekScores)
        except Exception as e:
            print(f"Error processing week {week}: {e}")
            
    if allWeeks:
        return pd.concat(allWeeks, ignore_index=True)
    else:
        return pd.DataFrame()



def getStandings(league):
    #Creates a DataFrame with columns 'Team Name', 'Record', 'Points For', etc. The DataFrame is sorted by best record to worst.

    teams = league.teams
    powerRankings = league.power_rankings()

    # Create a dictionary to map team names to their power rankings
    powerRankingsDict = {team.team_name: rank for rank, team in powerRankings}
    #Call getProjectedScores from ffProjScore
    projectedScores = getProjectedScores(currentWeek)

    sosDf = calculateSOS(league, currentWeek)
    sosDict = sosDf.set_index('Team Name')['SOS'].to_dict()

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
            'SOS' : sosDict.get(team.team_name, 'N/A'),

        }
        for team in teams
    ]

    df = pd.DataFrame(standings)

    try:
        luckdf = getLuckScoresAcrossWeeks(startweek=1, endweek=currentWeek)
        
        df["Team Name"] = df["Team Name"].str.strip()
        luckdf["Team"] = luckdf["Team"].str.strip()

        # Aggregate luck scores
        total_luck_df = luckdf.groupby("Team")["Luck Score"].sum().reset_index()
        total_luck_df.columns = ["Team Name", "Total Luck"]
        total_luck_df["Luck Rank"] = total_luck_df["Total Luck"].rank(ascending=False).astype(int)

        # Merge with main standings
        df = df.merge(total_luck_df, on="Team Name", how="left")

    except Exception as e:
        print("Could not calculate luck metrics:", e)
        df["Total Luck"] = None
        df["Luck Rank"] = None
    
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

def getTeamOwners(league):
    # Creates a dictionary with team names as keys and owner names as values
    teams = league.teams
    teamOwners = {}

    for team in teams:
        if hasattr(team, 'owners') and team.owners:
            owner = team.owners[0]
            firstName = owner.get('firstName', 'Unknown')
            lastName = owner.get('lastName', '')
            fullName = f"{firstName} {lastName}".strip()
            teamOwners[team.team_name] = fullName
        else:
            teamOwners[team.team_name] = 'Unknown'
            
    return teamOwners