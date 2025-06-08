# f1-practice-analyzer
A python formula to collect data using OpenF1 APIs and JSON parsing on Formula 1 practice session of users choice to calculate performance trends.

---

### Project Versions

- 'f1_practice.py': Latest version using the OpenF1 API (includes tire compound logic and session flexibility with user input).
- 'old_f1_script.py': Legacy version using Ergast API for basic lap time and position analysis.

---

### Features
- Pulls live session, lap, and tire data using 'session_key'.
- Analyzes fastest laps on **Soft** compounds (for qualifying simulations).
- Calculates average lap times on **Medium/Hard** compounds (for race simulations).
- Maps driver numbers to full names using OpenF1 metadata.
- Generates a clean summary report to '.txt' file.

---

### How to Use
1. Clone this repo.
2. Run the script:
   ```bash
   python3 f1_practice.py

You will be prompted to input:

-track name (e.g. Catalunya)
-session name (e.g. Practice 1)
-race year (e.g. 2025)
-file name for output (.txt format)

---

### Requirements
- Python 3.7+
- requests library

---

### EXAMPLE OUTPUT

SUMMARY OF PRACTICE 2



Fastest Drivers in Qualifying simulations

Oscar Piastri: 1:12.760
George Russell: 1:13.046
Max Verstappen: 1:13.070
Lando Norris: 1:13.070
Charles Leclerc: 1:13.260
Kimi Antonelli: 1:13.298
Fernando Alonso: 1:13.301
Isack Hadjar: 1:13.400
Liam Lawson: 1:13.494
Lewis Hamilton: 1:13.533
Nico Hulkenberg: 1:13.592
Yuki Tsunoda: 1:13.683
Carlos Sainz: 1:13.721
Alexander Albon: 1:13.839
Lance Stroll: 1:13.839
Gabriel Bortoleto: 1:13.959
Esteban Ocon: 1:14.005
Oliver Bearman: 1:14.126
Franco Colapinto: 1:14.303
Pierre Gasly: 1:19.572


Fastest Drivers in Race simulations by Compound

Liam Lawson (MEDIUM): 1:14.642
Oliver Bearman (MEDIUM): 1:15.225
Kimi Antonelli (MEDIUM): 1:17.061
George Russell (MEDIUM): 1:18.252
Isack Hadjar (MEDIUM): 1:18.257
Lando Norris (MEDIUM): 1:18.651
Pierre Gasly (MEDIUM): 1:19.175
Alexander Albon (MEDIUM): 1:19.188
Gabriel Bortoleto (MEDIUM): 1:19.300
Lewis Hamilton (MEDIUM): 1:19.739
Carlos Sainz (MEDIUM): 1:20.294
Oscar Piastri (MEDIUM): 1:20.324
Esteban Ocon (MEDIUM): 1:20.347
Nico Hulkenberg (MEDIUM): 1:20.350
Yuki Tsunoda (MEDIUM): 1:20.582
Charles Leclerc (MEDIUM): 1:20.617
Max Verstappen (MEDIUM): 1:20.648
Fernando Alonso (MEDIUM): 1:21.403
Franco Colapinto (HARD): 1:19.566
Lance Stroll (HARD): 1:18.295
