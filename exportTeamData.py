import pandas as pd
import os
from ffLuckModel import calculateLuckScore
from ffStandMatchData import getMatchups, currentWeek
from espn_api.football import League
import json

# Load all weekly matchups
all_weeks = []
for week in range(1, currentWeek + 1):
    df = getMatchups(week)
    all_weeks.append(df)

all_matchups = pd.concat(all_weeks, ignore_index=True)
luck_df = calculateLuckScore(all_matchups)

# Build a per-team dataframe including top players, scores, opponent, and margin
records = []
for _, row in all_matchups.iterrows():
    records.append({
        "Week": row["Week"],
        "Side": "Home Team",
        "Team": row["Home Team"].strip(),
        "Top Scorer": row.get("Home Top Player") or row.get("Home Top Players"),
        "Opponent": row["Away Team"].strip(),
        "Score": row["Home Actual Score"],
        "Opponent Score": row["Away Actual Score"],
        "Margin": row["Home Actual Score"] - row["Away Actual Score"]
    })
    records.append({
        "Week": row["Week"],
        "Side": "Away Team",
        "Team": row["Away Team"].strip(),
        "Top Scorer": row.get("Away Top Player") or row.get("Away Top Players"),
        "Opponent": row["Home Team"].strip(),
        "Score": row["Away Actual Score"],
        "Opponent Score": row["Home Actual Score"],
        "Margin": row["Away Actual Score"] - row["Home Actual Score"]
    })

players_df = pd.DataFrame(records)

# Merge with luck information
merged = pd.merge(players_df, luck_df, on=["Week", "Team"], how="left")

# ✅ Rename merged columns for frontend compatibility
merged = merged.rename(columns={
    "Score_x": "Score",
    "Opponent Score_x": "Opponent Score",
    "Margin_x": "Margin",
    "Opponent_x": "Opponent"
})

# ✅ Drop unnecessary duplicated _y columns
merged = merged.drop(columns=[col for col in merged.columns if col.endswith('_y')])

# Make a folder for team data
os.makedirs("team_data", exist_ok=True)

# Export one JSON per team
for team in merged["Team"].unique():
    team_df = merged[merged["Team"] == team].sort_values(by="Week")
    clean_team = ' '.join(team.split())  # removes extra/multiple spaces
    team_df["Team"] = team_df["Team"].apply(lambda x: ' '.join(x.split()))
    team_df["Opponent"] = team_df["Opponent"].apply(lambda x: ' '.join(x.split()))
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

# Create a roster JSON for all teams using the ESPN API
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)

rosters = {}
for team in league.teams:
    clean_team_name = ' '.join(team.team_name.strip().split())
    roster_list = []
    for player in team.roster:
        roster_list.append({
            "name": player.name,
            "position": player.position,
            "lineupSlot": player.lineupSlot
        })
    rosters[clean_team_name] = roster_list

with open("rosters.json", "w") as f:
    json.dump(rosters, f, indent=2)

print("✅ rosters.json created successfully.")
