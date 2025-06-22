from espn_api.football import League
import pandas as pd
from ffHistoricalData import *
from ffStandMatchData import *
#from ffMLModel import *
import matplotlib.pyplot as plt
import json
#from ffBookiev1 import *

league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)


#test_df = getLuckScoresAcrossWeeks(1, 14)

#print(getStandings(league))
#exportDF(test_df, 'testLuckScores.csv')
#print(test_df.sort_values("Luck Score", ascending=False).head(10))
#print(test_df.sort_values("Luck Score", ascending=False).tail(10))

#standings_df = getStandings(league)

# Preview the key luck columns
#print(standings_df[[  'Team Name',    'Record',    'Points For(PF)',    'Points Against(PA)',    'Total Luck',    'Luck Rank']].sort_values("Luck Rank"))

exportMatchupsToFolder(currentWeek=14)
