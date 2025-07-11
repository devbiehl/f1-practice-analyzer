# f1-practice-analyzer
A python formula to collect data using OpenF1 APIs and SQLite on Formula 1 practice sessions of users input to calculate performance trends. 

This program uses modular OOP, supports multiple sessions/events and includes logging and error handling.

---

### Project Versions
- 'main_f1_analyzer': Latest Version using OpenF1 API -- takes user input for Track, Session and Year. Includes tire compound mapping to driver lap times and mapping drivers to teams. Updates database with lap analysis for each session the user inputs and connects it to Event(race weekend) for fast Query.

- 'f1_practice.py': Legacy version using the OpenF1 API (includes tire compound logic and session flexibility with user input).

- 'old_f1_script.py': Legacy version using Ergast API for basic lap time and position analysis.

---

### Features
- Pulls live session, lap, and tire data using 'session_key'.
- Analyzes fastest laps on **Soft** compounds (for qualifying simulations) -- excludes outlier slow laps.
- Calculates average lap times on **Medium/Hard** compounds (for race simulations) -- excludes outlier slow laps.
- Maps driver numbers to full names using OpenF1 metadata.
- Generates a clean summary report to terminal
- Builds database for Event(race weekend(track name and year)), each session(practice 1,2,3), drivers name and number, team names, driver analysis(fastest soft tire performance, avg medium and hard compound times, and best race pace(lowest avg time) compound)

---

### How to Use
1. Clone this repo.
2. Run the script:
   ```bash
   python3 main_f1_analyzer.py

You will be prompted to input:

- track name (e.g. Catalunya)
- session name (e.g. Practice 1)
- race year (e.g. 2025)

---

### Requirements
- Python 3.7+
- requests library
- sqlite3

---

### EXAMPLE OUTPUT

Summary for Practice 1 at Silverstone, 2025
------------------------------------------------------------

Fastest Soft Tire Performance
------------------------------------------------------------
Lewis Hamilton (#44)
    Fastest Lap (SOFT): 1:26.892
Lando Norris (#4)
    Fastest Lap (SOFT): 1:26.915
Oscar Piastri (#81)
    Fastest Lap (SOFT): 1:27.042
Charles Leclerc (#16)
    Fastest Lap (SOFT): 1:27.095
George Russell (#63)
    Fastest Lap (SOFT): 1:27.163
Isack Hadjar (#6)
    Fastest Lap (SOFT): 1:27.217
Alexander Albon (#23)
    Fastest Lap (SOFT): 1:27.304
Liam Lawson (#30)
    Fastest Lap (SOFT): 1:27.351
Kimi Antonelli (#12)
    Fastest Lap (SOFT): 1:27.367
Max Verstappen (#1)
    Fastest Lap (SOFT): 1:27.432
Fernando Alonso (#14)
    Fastest Lap (SOFT): 1:27.678
Lance Stroll (#18)
    Fastest Lap (SOFT): 1:27.844
Carlos Sainz (#55)
    Fastest Lap (SOFT): 1:27.909
Arvid Lindblad (#36)
    Fastest Lap (SOFT): 1:27.958
Esteban Ocon (#31)
    Fastest Lap (SOFT): 1:28.057
Franco Colapinto (#43)
    Fastest Lap (SOFT): 1:28.086
Paul Aron (#97)
    Fastest Lap (SOFT): 1:28.142
Oliver Bearman (#87)
    Fastest Lap (SOFT): 1:28.147
Pierre Gasly (#10)
    Fastest Lap (SOFT): 1:28.332


Fastest Race Pace Performance
------------------------------------------------------------
George Russell (#63)
    AVG RACE PACE (MEDIUM): 1:28.081
Oscar Piastri (#81)
    AVG RACE PACE (MEDIUM): 1:28.139
Lando Norris (#4)
    AVG RACE PACE (MEDIUM): 1:28.247
Isack Hadjar (#6)
    AVG RACE PACE (MEDIUM): 1:28.391
Liam Lawson (#30)
    AVG RACE PACE (MEDIUM): 1:28.406
Max Verstappen (#1)
    AVG RACE PACE (MEDIUM): 1:28.544
Lewis Hamilton (#44)
    AVG RACE PACE (MEDIUM): 1:28.553
Charles Leclerc (#16)
    AVG RACE PACE (MEDIUM): 1:28.558
Kimi Antonelli (#12)
    AVG RACE PACE (MEDIUM): 1:28.714
Gabriel Bortoleto (#5)
    AVG RACE PACE (MEDIUM): 1:28.761
Esteban Ocon (#31)
    AVG RACE PACE (MEDIUM): 1:29.062
Pierre Gasly (#10)
    AVG RACE PACE (MEDIUM): 1:29.087
Franco Colapinto (#43)
    AVG RACE PACE (MEDIUM): 1:29.130
Lance Stroll (#18)
    AVG RACE PACE (HARD): 1:29.161
Oliver Bearman (#87)
    AVG RACE PACE (MEDIUM): 1:29.205
Fernando Alonso (#14)
    AVG RACE PACE (HARD): 1:29.369
Arvid Lindblad (#36)
    AVG RACE PACE (MEDIUM): 1:29.379
Paul Aron (#97)
    AVG RACE PACE (MEDIUM): 1:29.515
Alexander Albon (#23)
    AVG RACE PACE (HARD): 1:29.582
Carlos Sainz (#55)
    AVG RACE PACE (HARD): 1:29.859


--- Team Race Pace Averages (MEDIUM/HARD) ---
McLaren: 1:28.193 (MEDIUM)
Mercedes: 1:28.398 (MEDIUM)
Racing Bulls: 1:28.398 (MEDIUM)
Ferrari: 1:28.556 (MEDIUM)
Red Bull Racing: 1:28.962 (MEDIUM)
Alpine: 1:29.108 (MEDIUM)
Haas F1 Team: 1:29.134 (MEDIUM)
Kick Sauber: 1:29.138 (MEDIUM)
Aston Martin: 1:29.265 (HARD)
Williams: 1:29.720 (HARD)
