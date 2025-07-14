# Event Data Pipeline
A python formula to collect data using OpenF1 APIs and SQLite on Formula 1 practice sessions of users input to calculate performance trends. 

This is a modular object oriented program for event analysis. With minimal code changes it can be used for Business KPIs, Finance analysis, etc. It can support multiple sessions/events and includes logging and error handling.

---

### Features
- Pulls live session, lap, and tire data via session key
- Identifies fastest laps on **Soft** compounds (for qualifying simulations)
- Calculates average lap times on **Medium/Hard** compounds (for race simulations)
- Maps driver numbers to full names using OpenF1 metadata.
- Generates a clean summary report to terminal
- Builds a normalized SQLite database:
    - Stores race weekend (Event) -> sessions -> driver/team data
    - Records tire-based performance stats (fastest laps, average pace, compound choices)
    - Includes loggging and error handling for traceability

---

### EXAMPLE OUTPUT
```
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
```
---

### How to Use
1. Clone this repository:
    ```bash
    git clone https://github.com/devbiehl/event-data-pipeline.git
    cd event-data-pipeline

2. Install requirements:
    ```bash
    pip install -r requirements.txt

3. Run the pipeline:
   ```bash
   python3 main.py

You will be prompted to input:

- track name (e.g. Silverstone)
- session name (e.g. Practice 1)
- race year (e.g. 2025)

---

### Project Structure
```
event-data-pipeline/
|
|-- event_pipeline/         # Modular codebase
|   |-- session.py          # Core pipeline runner
|   |-- data_ingestor.py    # API data fetch and process
|   |-- lap_analyzer.py     # Lap time summary logic
|   |-- db_handler.py       # SQLite layer
|   |-- logging_config.py   # Logging setup
|   |-- driver.py           # Driver object builder
|   |-- team.py             # Team object builder
|   |-- db_schema.py        # SQLite schema
|   |-- utils.py            # Helper functions
|   |-- __init__.py         # Package initializer
|
|-- tests/                  # pytest unit tests
|   |-- test_session.py
|
|-- main.py                 # Entry point
|-- requirements.txt
|-- .gitignore
|__ README.md
```

---

### Testing
Tests using pytest and pytest-mock

1. To run tests:

    ```bash
    pytest -v
    ```

---

### Legacy Scripts
- 'main_f1_analyzer': Legacy Version using OpenF1 API -- takes user input for Track, Session and Year. Includes tire compound mapping to driver lap times and mapping drivers to teams. Updates database with lap analysis for each session the user inputs and connects it to Event(race weekend) for fast Query.

- 'f1_practice.py': Legacy version using the OpenF1 API (includes tire compound logic and session flexibility with user input).

- 'old_f1_script.py': Legacy version using Ergast API for basic lap time and position analysis.

---


### Requirements
- Python 3.7+
- requests
- sqlite3 (built in)
- pytest
- pytest-mock

---

### Author
Devin Biehl -- GitHub
"This project is part of a portfolio focused on data engineering and analytical pipelines."

---

### License
[MIT](LICENSE)