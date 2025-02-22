from espn_api.football import League
import pandas as pd
from ffBookiev1 import getStandings


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
    return getStandings()

def getAllTimeData():
    currentLeague = initializeLeague(2024)
    previousSeasons = currentLeague.previousSeasons

    allTimeData = {}

    for year in previousSeasons + [2024]:
        try:
            standings = getStandingsForYear(year)
            for _, row in standings.iterrows():
                teamName = row['Team Name']
                if teamName not in allTimeData:
                    allTimeData[teamName] = {
                        'Total Points For': 0,
                        'Total Points Against': 0,
                        'Total Games': 0,
                        'Total Wins': 0,
                        'Total Losses': 0,
                        'Total Expected Wins': 0,
                        'Total Luck': 0,
                    }

                    # Update all-time metrics
                allTimeData[teamName]['Total Points For'] += row['Points For(PF)']
                allTimeData[teamName]['Total Points Against'] += row['Points Against(PA)']
                allTimeData[teamName]['Total Games'] += (row['Wins'] + row['Losses'])
                allTimeData[teamName]['Total Wins'] += row['Wins']
                allTimeData[teamName]['Total Losses'] += row['Losses']
                allTimeData[teamName]['Total Expected Wins'] += row['Expected Wins']
                allTimeData[teamName]['Total Luck'] += row['Luck']
        except Exception as e:
            print(f"Error retriving data for {year}: {e}")

    #Calculate all-time metrics for each of the teams
    allTimeStandings = []
    for teamName, data in allTimeData.items():
        totalGames = data['Total Games']
        if totalGames == 0:
            continue

        allTimeStandings.append({
           
            'Team Name': teamName,
            'All-Time Record': f"{data['Total Wins']}-{data['Total Losses']}",
            'All-Time PF/G': round(data['Total Points For'] / totalGames, 2),
            'All-Time PA/G': round(data['Total Points Against'] / totalGames, 2),
            'All-Time DIFF': round((data['Total Points For'] - data['Total Points Against']) / totalGames, 2),
            'All-Time Expected Wins': round(data['Total Expected Wins'], 2),
            'All-Time Luck': round(data['Total Luck'], 2),
        })

    return pd.DataFrame(allTimeStandings)

