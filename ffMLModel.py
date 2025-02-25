from espn_api.football import League
import pandas as pd
from ffHistoricalData import *
from ffStandMatchData import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

currentData = getStandings(league)
historicalData = getAllTimeData()

teamOwners = getTeamOwners(league)

currentData['Owner Name'] = currentData['Team Name'].map(teamOwners)

mergedData = pd.merge(currentData,historicalData, left_on = 'Owner Name', right_on= 'User Name', how='left')

print(mergedData)
