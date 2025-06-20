"""
FFL – Projected Playoff Bracket
--------------------------------
Usage:
    python ffProjectedBracket.py        # regenerates projected_bracket.png
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from ffStandMatchData import getStandings            # existing helper :contentReference[oaicite:0]{index=0}
from espn_api.football import League

# ---------- CONFIG ---------------------------------------------------------
league = League(
    league_id=42024189,
    year=2024,
    espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14',
    swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}'
)                         # swap to league.current_week in-season

# Hard-code each team’s division for quick lookup.
DIVISION_MAP = {
    "Game of Throws": "Ignatius",
    "Hamilton Administration": "Ignatius",
    "Team Kareem Pie 🥧": "Ignatius",
    "The  Left Tacklers": "Ignatius",
    "Hawaii McLovins VIII": "Ignatius",
    "To infinity and Bijan": "Xavier",
    "First and Ted": "Xavier",
    "Amon a Mission": "Xavier",
    "How I Metcalf Your Mother": "Xavier",
    "Jared's Pack Attack": "Xavier",
}

# ---------------------------------------------------------------------------

def labelWinner(value, teamA, teamB):
    if value > 0:
        return teamA
    elif value < 0:
        return teamB
    else:
        return ""

def head_to_head_matrix(league):
    """Return a DataFrame of head-to-head wins (rows beaten columns)."""
    matrix = pd.DataFrame(0, index=[t.team_name for t in league.teams],
                             columns=[t.team_name for t in league.teams])
    for wk in range(1, 14 + 1):
        for m in league.scoreboard(week=wk):
            if m.home_score > m.away_score:
                matrix.loc[m.home_team.team_name, m.away_team.team_name] += 1
                matrix.loc[m.away_team.team_name, m.home_team.team_name] -= 1
            else:
                matrix.loc[m.away_team.team_name, m.home_team.team_name] += 1
                matrix.loc[m.home_team.team_name, m.away_team.team_name] -= 1
    
    labeledDf = pd.DataFrame(index=matrix.index, columns=matrix.columns)
    for teamA in matrix.index:
        for teamB in matrix.columns:
            value = matrix.loc[teamA, teamB]
            labeledDf.loc[teamA, teamB] = labelWinner(value, teamA, teamB)

    return labeledDf


def break_ties(df, h2h_matrix):
    """Resolve ties inside a single division (record first already equal)."""
    resolved = []
    for _, group in df.groupby('division'):
        while not group.empty:
            best_wins = group.wins.max()
            tier = group[group.wins == best_wins]
            if len(tier) == 1:
                resolved.append(tier.iloc[0])
                group = group.drop(tier.index)
                continue
            # Head-to-head wins among tied teams
            h2h_wins = tier.apply(lambda row:
                                  h2h_matrix.loc[row.team, tier.team].sum(),
                                  axis=1)
            tier['h2h'] = h2h_wins
            best_h2h = tier.h2h.max()
            tier = tier[tier.h2h == best_h2h]
            if len(tier) == 1:
                resolved.append(tier.iloc[0])
                group = group.drop(tier.index)
                continue
            # Points-for as final tie-breaker
            tier = tier.sort_values('pf', ascending=False)
            resolved.append(tier.iloc[0])
            group = group.drop(tier.index[0])
    return pd.DataFrame(resolved)

def project_seeds(stand_df, league):
    """Return DataFrame of six seeded teams with columns [seed, team]."""
    stand_df = stand_df.copy()
    stand_df['division'] = stand_df['Team Name'].map(DIVISION_MAP)
    stand_df['wins']  = stand_df['Record'].str.split('-').str[0].astype(int)
    stand_df['pf']    = stand_df['Points For(PF)']

    h2h = head_to_head_matrix(league)

    # 1) pick top-2 per division with tiebreaks
    div_ranked = break_ties(stand_df, h2h)

    # if any division still missing a 2nd team (rare after drops)
    div_full = (stand_df[~stand_df.index.isin(div_ranked.index)]
                .sort_values(['division', 'wins', 'pf'], ascending=[True, False, False])
                .groupby('division').head(2 - div_ranked.groupby('division').size()))
    div_ranked = pd.concat([div_ranked, div_full])

    # 2) two wildcard spots by highest PF
    remaining = stand_df[~stand_df['Team Name'].isin(div_ranked['Team Name'])]
    wildcards = remaining.nlargest(2, 'pf')

    six = pd.concat([div_ranked, wildcards])
    six = six.sort_values(['wins', 'pf'], ascending=[False, False]).reset_index(drop=True)
    six.insert(0, 'seed', six.index + 1)
    return six[['seed', 'Team Name', 'division', 'wins', 'pf']]

def draw_bracket(seed_df, outfile="projected_bracket.png"):
    plt.figure(figsize=(10, 6))
    # Seed positions
    y = {1:4, 2:1, 3:3, 4:2, 5:2.5, 6:3.5}
    for _, row in seed_df.iterrows():
        plt.text(0, y[row.seed], f"{row.seed}. {row['Team Name']}", va='center')
    # Connecting lines
    plt.plot([0.6, 1.2], [y[3], y[6]], lw=2)
    plt.plot([0.6, 1.2], [y[4], y[5]], lw=2)
    plt.plot([1.2, 2.0], [y[3], 3.25], lw=2)
    plt.plot([1.2, 2.0], [y[4], 2.25], lw=2)
    plt.plot([2.0, 2.8], [3.25, 2.75], lw=2)
    plt.axis('off')
    plt.title("Projected Playoff Bracket (Seeds 1-6)")
    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    print(f"✅  Bracket saved ➜ {outfile}")

if __name__ == "__main__":
    league = League(league_id=42024189, year=2024, espn_s2='AECycM1RSKC9H6KO4Qw7b0ZKIaa417A48498axeqW12XB0VFyWXroqy%2BFzAdJFMJUqxu4t05etxquUZYQ92C7V8N%2BzGT48zFtm4IJM04CG%2FG7zrSRXMBsqrw219pF4k7L0BYwwHr1om5AQNTKViQ5YJhH9SFEmGo03L1NTeuQSPy3Ws6HpQs2pfnZKuddHWxNUwH9HVOxVkOc4nSbCn8LPm2c1lsCAuuH26Z4laiqV2e0MCjMNizTi%2FS8VFHmVCXcPVejE3reh1JRyiHuKp1gE14', swid='{CDA2BA80-43BE-41FB-9AB1-C8BE52DD4C45}')
    standings = getStandings(league)                       # your existing routine :contentReference[oaicite:1]{index=1}
    #seeds = project_seeds(standings, league)
    # Optional: also dump seeds to JSON for SPA use
    #seeds.to_json("projected_bracket.json", orient="records", indent=2)
    #draw_bracket(seeds)

    head_to_head_matrix(league).to_csv("head_to_head_matrix.csv", index=True)
    print(head_to_head_matrix(league).head(10))
