from espn_api.football import League
import pandas as pd
from ffStandMatchData import getStandings
import re

#Initalize league helper function
def initializeLeague(year):
    league = League(
        league_id=42024189,
        year=year,
        espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
        swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
    )
    return league

def getStandingsForYear(year):
    league = initializeLeague(year)
    return getStandings(league)

def cleanTeamName(name):
    """Cleans team name for consistent comparison."""
    name = name.lower().strip()
    name = re.sub(r'[^\w\s]', '', name)  # Remove special characters and emojis
    name = re.sub(r'\s+', ' ', name)  # Collapse multiple spaces
    return name    

def getAllTimeData():
    currentLeague = initializeLeague(2024)          #Change for current year
    previousSeasons = currentLeague.previousSeasons

    members = currentLeague.members
    memberIDs = {member['id']: member for member in members}

    allTimeData = {}

    for year in previousSeasons + [2024]:
        try:
            league = initializeLeague(year)
            standings = getStandings(league)

            teamToUser = {}
            for team in league.teams:
                if team.owners:
                    ownerId = team.owners[0].get('id')
                    cleanedName = cleanTeamName(team.team_name)
                    teamToUser[cleanedName] = ownerId

            for _, row in standings.iterrows():
                rawTeamName = row['Team Name']
                cleanedTeamName1 = cleanTeamName(rawTeamName)
                userID = teamToUser.get(cleanedTeamName1)

                if not userID:
                    continue

                user = memberIDs.get(userID)
                if not user:
                    continue

                firstName = user.get('firstName', 'Unknown')
                lastName = user.get('lastName', '')
                fullName = f"{firstName} {lastName}".strip()

                if fullName not in allTimeData:
                    allTimeData[fullName] = {
                        'Total Points For': 0,
                        'Total Points Against': 0,
                        'Total Games': 0,
                        'Total Wins': 0,
                        'Total Losses': 0,
                        'Total Luck': 0,
                    }

                record = row['Record']
                wins, losses = map(int, record.split('-'))

                    # Update all-time metrics
                allTimeData[fullName]['Total Points For'] += row['Points For(PF)']
                allTimeData[fullName]['Total Points Against'] += row['Points Against(PA)']
                allTimeData[fullName]['Total Games'] += (wins+ losses)
                allTimeData[fullName]['Total Wins'] += wins
                allTimeData[fullName]['Total Losses'] += losses
                allTimeData[fullName]['Total Luck'] += row.get("Total Luck", 0)
        except Exception as e:
            print(f"Error retriving data for {year}: {e}")

    #Calculate all-time metrics for each of the teams
    allTimeStandings = []
    for fullName, data in allTimeData.items():
        totalGames = data['Total Games']
        if totalGames == 0:
            continue

        allTimeStandings.append({
           
            'User Name': fullName,
            'All-Time Record': f"{data['Total Wins']}-{data['Total Losses']}",
            'All-Time PF/G': round(data['Total Points For'] / totalGames, 2),
            'All-Time PA/G': round(data['Total Points Against'] / totalGames, 2),
            'All-Time DIFF': round((data['Total Points For'] - data['Total Points Against']) / totalGames, 2),
            'All-Time Luck': round(data['Total Luck'], 2),
        })

    return pd.DataFrame(allTimeStandings)
