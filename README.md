# Fantasy Football League Bookie

Welcome to the **Fantasy Football League Bookie**! This project is designed to provide detailed standings, power rankings, matchup predictions, and advanced analytics for your fantasy football league using the `espn_api.football` library. It's perfect for league commissioners or anyone who loves diving into the numbers behind their league.

---

## **Features**
- **Standings**: View team records, points for, points against, and points per game.
- **Power Rankings**: See how teams stack up based on ESPN's power rankings.
- **Matchup Predictions**: Get projected scores, predicted winners, and top players for each matchup.
- **Advanced Metrics**:
  - **PF/G**: Points For per Game.
  - **PA/G**: Points Against per Game.
  - **DIFF**: Points Differential per Game.
  - **Luck**: Measures how "lucky" or "unlucky" a team has been based on their points scored and allowed.
- **Historical Data**: Track all-time performance metrics for each team owner.
- **Interactive Dashboard**: A web-based dashboard to visualize standings, matchups, and historical data.
- **JSON Export**: Export standings, matchups, and historical data as JSON files for use in web applications.

---

## **Setup**

### **1. Prerequisites**
- Python 3.x installed on your machine.
- Required Python libraries: `pandas`, `espn_api`, and `matplotlib`.

### **2. Install Dependencies**
Run the following command to install the required libraries:

```bash
pip install pandas espn-api matplotlib
```

### **3. Configure League Credentials**
To connect to your ESPN league, you'll need the following:

- League ID: Found in the URL of your ESPN league page.
- ESPN S2 Cookie: A secure token for authentication.
- SWID Cookie: Another authentication token.

Replace the placeholders in the code with your league's credentials:

```python
league = League(
    league_id=12345678,  # Replace with your league ID
    year=2024,           # Replace with the current year
    espn_s2='YOUR_ESPN_S2_COOKIE',  # Replace with your ESPN S2 cookie
    swid='{YOUR_SWID_COOKIE}'        # Replace with your SWID cookie
)
```

### **4. Run the Script**
Save the script as ffBookie.py and run it using Python:

```bash
python ffBookie.py
```

This will generate the following JSON files:
- matchups.json: Weekly matchup data.
- standings.json: Current standings data.
- historical.json: All-time historical data.

---

## **How It Works**

### **1. Standings**
The script generates a standings table with the following columns:

- Team Name: The name of the fantasy team.
- Record: The team's win-loss record (e.g., 10-4).
- Points For (PF): Total points scored by the team.
- Points Against (PA): Total points allowed by the team.
- PF/G: Points For per Game.
- PA/G: Points Against per Game.
- DIFF: Points Differential per Game.
- Power Ranking: ESPN's power ranking for the team.
- Expected Wins: The number of wins the team "should" have based on their points scored and allowed.
- Luck: How "lucky" or "unlucky" the team has been (actual wins vs. expected wins).
- SOS (Strength of Schedule): Average points scored by the team's opponents.

### **2. Matchup Predictions**
The getMatchups function provides detailed information about each matchup for a given week, including:

- Home Team: The home team in the matchup.
- Away Team: The away team in the matchup.
- Projected Scores: Projected scores for both teams.
- Actual Scores: Actual scores (if the matchup has been played).
- Predicted Winner: The team predicted to win based on projected scores.
- Projected Margin: The difference between projected scores.
- Top Players: The top 3 projected players for each team.

### **3. Historical Data**
The getAllTimeData function calculates all-time performance metrics for each team owner, including:

- All-Time Record: Total wins and losses.
- All-Time PF/G: Average points for per game.
- All-Time PA/G: Average points against per game.
- All-Time DIFF: Average points differential per game.
- All-Time Expected Wins: Total expected wins.
- All-Time Luck: Total luck over all seasons.

### **4. Interactive Dashboard**
The index.html file provides a web-based dashboard to visualize:

- Weekly Matchups: Projected scores, predicted winners, and top players.
- Current Standings: Team records, points for/against, and advanced metrics.
- Historical Data: All-time performance metrics for each team owner.

To use the dashboard:

1. Generate the JSON files by running ffBookie.py.
2. Open index.html in a web browser.

---

## **Example Output**

### **Standings**

| Team Name | Record | Points For(PF) | Points Against(PA) | PF/G | PA/G | DIFF | Power Ranking | Expected Wins | Luck | SOS |
|-----------|--------|----------------|-------------------|------|------|------|---------------|---------------|------|-----|
| Team 1    | 10-4   | 1500           | 1400              | 107.14 | 100.00 | 7.14 | 94.05 | 8.5 | 1.5 | 102.3 |
| Team 2    | 9-5    | 1450           | 1475              | 103.57 | 105.36 | -1.79 | 87.00 | 7.8 | 1.2 | 98.7 |
| Team 3    | 8-6    | 1400           | 1425              | 100.00 | 101.79 | -1.79 | 86.90 | 7.2 | 0.8 | 95.4 |

### **Matchups**

| Week | Home Team | Away Team | Home Projected Score | Away Projected Score | Home Actual Score | Away Actual Score | Predicted Winner | Projected Margin | Home Top Players | Away Top Players |
|------|-----------|-----------|---------------------|---------------------|------------------|------------------|-----------------|-----------------|-----------------|-----------------|
| 1    | Team A    | Team B    | 123.4               | 110.5               | 125.0            | 112.0            | Team A          | 12.9            | [(Player X, 25.3), (Player Y, 22.1)] | [(Player Z, 24.0), (Player W, 21.5)] |
| 1    | Team C    | Team D    | 98.7                | 105.0               | N/A              | N/A              | Team D          | 6.3             | [(Player A, 20.0), (Player B, 18.5)] | [(Player C, 22.0), (Player D, 19.0)] |

### **Historical Data**

| User Name | All-Time Record | All-Time PF/G | All-Time PA/G | All-Time DIFF | All-Time Expected Wins | All-Time Luck |
|-----------|----------------|--------------|--------------|--------------|---------------------|--------------|
| User 1    | 50-30          | 105.5        | 100.0        | 5.5          | 48.2                | 1.8          |
| User 2    | 45-35          | 102.3        | 103.0        | -0.7         | 43.5                | 1.5          |

---

## **Exporting Data**
You can export the standings, matchups, or historical data to a JSON file using the exportDFtoJSON function:

```python
exportDFtoJSON(getStandings(), filename='standings.json')
exportDFtoJSON(getMatchups(currentWeek), filename='matchups.json')
exportDFtoJSON(getAllTimeData(), filename='historical.json')
```

---

## **License**
This project is open-source and available under the MIT License.

## **Contact**
If you have any questions or suggestions, feel free to reach out.

Enjoy using the Fantasy Football League Bookie! May your team be lucky and your victories plentiful. 🏈
