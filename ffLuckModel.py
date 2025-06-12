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


# Calculates how lucky a team was based on the strength of the opponent they faced (lower opponent score = luckier).
def calcOpponentLuck(df):
    df["Opponent Luck"] = 0.0

    for week in df['Week'].unique():
        weekData = df[df['Week'] == week]
        scores = weekData["Opponent Score"].rank(pct=True)

        df.loc[weekData.index, "Opponent Luck"] = 1 - scores

    return df

#scoreDf = calcOpponentLuck(scoreDf)


# Calculates luck based on how close the game was; narrow wins/losses are considered luckier.
def calcMarginLuck(df):
    df["Margin Luck"] = 0.0

    for week in df['Week'].unique():
        weekData = df[df['Week'] == week]
        maxMargin = weekData["Margin"].abs().max()

        if maxMargin == 0:
            df.loc[weekData.index, "Margin Luck"] = 1.0

        else:
            df.loc[weekData.index, "Margin Luck"] = 1 - (weekData["Margin"].abs() / maxMargin)

    return df

#scoreDf = calcMarginLuck(scoreDf)


# Calculates luck based on how a team's score compared to the league average that week.
def calcAvgLuck(df):
    df["Average Luck"] = 0.0

    for week in df['Week'].unique():
        weekDf = df[df['Week'] == week]
        weekMean = weekDf["Score"].mean()
        weekStd = weekDf["Score"].std()

        if weekStd == 0:
            df.loc[weekDf.index, "Average Luck"] = 0.5

        else:
            
            zScores = (weekDf["Score"] - weekMean) / weekStd
            df.loc[weekDf.index, "Average Luck"] = norm.cdf(zScores) 

    return df

#scoreDf = calcAvgLuck(scoreDf)

'''
scoreDf["Luck Score"] = (round(
    0.4 * scoreDf["Opponent Luck"] + 
    0.3 * scoreDf["Margin Luck"] + 
    0.3 * scoreDf["Average Luck"],
    2) * 100)
'''

#print(scoreDf.sort_values("Luck Score", ascending=False).head(10))


def calcCompositeLuck(df):
    df = df.copy()
    df["Luck Score"] = 0.0

    for week in df['Week'].unique():
        weekDf = df[df['Week'] == week].copy()

        scorePct = weekDf["Score"].rank(pct=True)
        oppScorePct = weekDf["Opponent Score"].rank(pct=True)

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
                ) / 6
                luckScores.append(round(luck, 3))

            else:  # LOSS
                # Unlucky loss = high score, strong opponent, close game
                luck = (
                    scorePct[i] * 2 +                  # high score = unlucky
                    oppScorePct[i] * 1 +               # strong opponent = unlucky
                    marginCloseness[i] * 3             # closer loss = more unlucky
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


