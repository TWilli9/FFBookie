import pandas as pd
import os
from ffLuckModel import calculateLuckScore
from ffStandMatchData import getMatchups, currentWeek
import json


# Load all weekly matchups + calculate luck
all_weeks = []
for week in range(1, currentWeek + 1):
    df = getMatchups(week)
    all_weeks.append(df)
all_matchups = pd.concat(all_weeks, ignore_index=True)
luck_df = calculateLuckScore(all_matchups)

# Merge scores + luck
merged = pd.merge(
    all_matchups.melt(id_vars=["Week"], value_vars=["Home Team", "Away Team"], var_name="Side", value_name="Team"),
    luck_df,
    on=["Week", "Team"],
    how="left"
)

# Make a folder for team data
os.makedirs("team_data", exist_ok=True)

# Export one JSON per team
for team in merged["Team"].unique():
    team_df = merged[merged["Team"] == team].sort_values(by="Week")
    clean_team = ' '.join(team.strip().split())  # Removes extra/multiple spaces
    filename = f"team_data/{clean_team.replace(' ', '_')}.json"
    team_df.to_json(filename, orient="records", indent=2)
    print(f"Exported {filename}")


# Collect all clean team names from filenames
team_names = sorted([
    ' '.join(filename.replace('.json', '').replace('_', ' ').strip().split())
    for filename in os.listdir("team_data")
    if filename.endswith(".json")
])


# Save to teams.json
with open("teams.json", "w") as f:
    json.dump(team_names, f, indent=2)

print("✅ teams.json created successfully.")
