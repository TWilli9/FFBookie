---

# Fantasy Football League Bookie

Welcome to the **Fantasy Football League Bookie**! This project is designed to provide detailed standings, power rankings, and advanced analytics for your fantasy football league using the `espn_api.football` library. It’s perfect for league commissioners or anyone who loves diving into the numbers behind their league.

---

## **Features**
- **Standings**: View team records, points for, points against, and points per game.
- **Power Rankings**: See how teams stack up based on ESPN's power rankings.
- **Advanced Metrics**:
  - **PF/G**: Points For per Game.
  - **PA/G**: Points Against per Game.
  - **DIFF**: Points Differential per Game.
  - **Luck**: Measures how "lucky" or "unlucky" a team has been based on their points scored and allowed.
- **Customizable**: Easily add or remove metrics to suit your league's needs.

---

## **Setup**

### **1. Prerequisites**
- Python 3.x installed on your machine.
- Required Python libraries: `pandas` and `espn_api`.

### **2. Install Dependencies**
Run the following command to install the required libraries:

```bash
pip install pandas espn-api
```

### **3. Configure League Credentials**
To connect to your ESPN league, you’ll need the following:
- **League ID**: Found in the URL of your ESPN league page.
- **ESPN S2 Cookie**: A secure token for authentication.
- **SWID Cookie**: Another authentication token.

Replace the placeholders in the code with your league's credentials:

```python
league = League(
    league_id=42024189,  # Replace with your league ID
    year=2024,           # Replace with the current year
    espn_s2='YOUR_ESPN_S2_COOKIE',  # Replace with your ESPN S2 cookie
    swid='{YOUR_SWID_COOKIE}'        # Replace with your SWID cookie
)
```

### **4. Run the Script**
Save the script as `ffBookie.py` and run it using Python:

```bash
python ffBookie.py
```

---

## **How It Works**

### **1. Standings**
The script generates a standings table with the following columns:
- **Team Name**: The name of the fantasy team.
- **Record**: The team's win-loss record (e.g., 10-4).
- **Points For (PF)**: Total points scored by the team.
- **Points Against (PA)**: Total points allowed by the team.
- **PF/G**: Points For per Game.
- **PA/G**: Points Against per Game.
- **DIFF**: Points Differential per Game.
- **Power Ranking**: ESPN's power ranking for the team.
- **Expected Wins**: The number of wins the team "should" have based on their points scored and allowed.
- **Luck**: How "lucky" or "unlucky" the team has been (actual wins vs. expected wins).

### **2. Power Rankings**
The script pulls ESPN's power rankings for your league and displays them alongside the standings.

### **3. Advanced Metrics**
- **Luck**: Calculated using the Pythagorean expectation formula, adjusted for a 14-week season.
- **PF/G** and **PA/G**: Points For and Points Against per game, useful for comparing team performance over time.

---

## **Customization**
You can easily add or remove metrics by editing the `standings` list comprehension in the `getStandings()` function. For example:
- Add **Streak**: `'Streak': team.streak`
- Add **Total Moves**: `'Total Moves': team.acquisitions + team.drops`
- Add **Best/Worst Week**: `'Best Week': max(team.scores)`, `'Worst Week': min(team.scores)`

---

## **Example Output**
Here’s an example of what the output might look like:

| Team Name                  | Record | Points For(PF) | Points Against(PA) | PF/G  | PA/G  | DIFF  | Power Ranking | Expected Wins | Luck  |
|----------------------------|--------|----------------|--------------------|-------|-------|-------|---------------|---------------|-------|
| Team 1                     | 10-4   | 1500           | 1400               | 107.14| 100.00| 7.14  | 94.05         | 8.5           | 1.5   |
| Team 2                     | 9-5    | 1450           | 1475               | 103.57| 105.36| -1.79 | 87.00         | 7.8           | 1.2   |
| Team 3                     | 8-6    | 1400           | 1425               | 100.00| 101.79| -1.79 | 86.90         | 7.2           | 0.8   |

---

## **Contributing**
If you’d like to contribute to this project, feel free to fork the repository and submit a pull request. Here are some ideas for improvements:
- Add support for head-to-head records.
- Include playoff probability calculations.
- Add visualizations using `matplotlib` or `plotly`.

---

## **License**
This project is open-source and available under the [MIT License](LICENSE).

---

## **Contact**
If you have any questions or suggestions, feel free to reach out

---

Enjoy using the **Fantasy Football League Bookie**! May your team be lucky and your victories plentiful. 🏈

---
