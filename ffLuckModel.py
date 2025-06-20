import pandas as pd
import numpy as np
from scipy.stats import norm


matchups = pd.read_json("matchups.json")
standings = pd.read_json("standings.json")


allScores = []

for _, row in matchups.iterrows():
    week = row['Week']

    for side in ['Home', 'Away']:
        allScores.append({
            'Week': week,
            'Team': row[f'{side} Team'].strip(),
            "Opponent": row[f"{'Away' if side == 'Home' else 'Home'} Team"].strip(),
            "Score": row[f'{side} Actual Score'],
            "Opponent Score": row[f"{'Away' if side == 'Home' else 'Home'} Actual Score"],
            "Margin": row[f"{side} Actual Score"] - row[f"{'Away' if side == 'Home' else 'Home'} Actual Score"],
        })

#scoreDf = pd.DataFrame(allScores)


def calcCompositeLuck(df):
    df = df.copy()
    df["Luck Score"] = 0.0

    for week in df['Week'].unique():
        weekDf = df[df['Week'] == week].copy()

        scorePct = weekDf["Score"].rank(pct=True)
        oppScorePct = weekDf["Opponent Score"].rank(pct=True)
        #avgScore = weekDf["Score"].mean()
        #avgRelativeScore = (weekDf["Score"] / avgScore) -1

        margin = weekDf["Margin"]
        maxMargin = margin.abs().max() or 1  # Prevent divide-by-zero
        marginCloseness = 1 - (margin.abs() / maxMargin)  # 1 for close, 0 for blowout

        luckScores = []

        for i in weekDf.index:
            
            if margin[i] > 0:  # WIN
                # Lucky win = low score, weak opponent, close game
                luck = (
                    (1 - scorePct[i]) * 2 +            # low score = lucky
                    (1 - oppScorePct[i]) * 1 +         # weak opponent = lucky
                    marginCloseness[i] * 3             # closer win = more lucky
                    #(-avgRelativeScore[i] * 1)           #scored less than average = lucky
                ) / 6
                luckScores.append(round(luck, 3))

            else:  # LOSS
                # Unlucky loss = high score, strong opponent, close game
                luck = (
                    scorePct[i] * 2 +                  # high score = unlucky
                    oppScorePct[i] * 1 +               # strong opponent = unlucky
                    marginCloseness[i] * 3            # closer loss = more unlucky
                    #avgRelativeScore[i] * 1            #scored more than average = unlucky
                ) / 6
                luckScores.append(round(-luck, 3))     # NEGATIVE score for unlucky

        df.loc[weekDf.index, "Luck Score"] = pd.Series(luckScores, index=weekDf.index).clip(-1, 1)

    return df




# Combines all three luck components into a single 'Luck Score' for each team per week.
# This function expects a matchups-style DataFrame and flattens it internally.
def calculateLuckScore(matchups_df):

    allScores = []
    for _, row in matchups_df.iterrows():
        week = row['Week']
        for side in ['Home', 'Away']:
            allScores.append({
                'Week': week,
                'Team': row[f'{side} Team'].strip(),
                'Opponent': row[f"{'Away' if side == 'Home' else 'Home'} Team"].strip(),
                'Score': row[f'{side} Actual Score'],
                'Opponent Score': row[f"{'Away' if side == 'Home' else 'Home'} Actual Score"],
                'Margin': row[f'{side} Actual Score'] - row[f"{'Away' if side == 'Home' else 'Home'} Actual Score"],
            })

    df = pd.DataFrame(allScores)
    df = calcCompositeLuck(df)
    return df


