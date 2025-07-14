import sqlite3

def connect_db():
    conn = sqlite3.connect('f1_analysis.db')
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Event(
        event_id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name        TEXT NOT NULL,
        year        INTEGER NOT NULL
    );

    
    CREATE TABLE IF NOT EXISTS Session (
        session_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        event_id    INTEGER NOT NULL,
        name        TEXT NOT NULL,
        session_key INTEGER,
    
        FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Team(
        team_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id  INTEGER,
        name        TEXT NOT NULL,
        UNIQUE(session_id, name),     
        
        FOREIGN KEY (session_id) REFERENCES Session(session_id)
    );
                      
    CREATE TABLE IF NOT EXISTS Driver (
        driver_id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name                TEXT NOT NULL UNIQUE,
        number              INTEGER NOT NULL                  
    );                 
    
    CREATE TABLE IF NOT EXISTS DriverSessionParticipation   (
        session_driver_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id          INTEGER NOT NULL,
        driver_id           INTEGER NOT NULL,
        team_id             INTEGER NOT NULL,
        number              INTEGER,
        UNIQUE(session_id, driver_id),
    
        FOREIGN KEY (session_id) REFERENCES Session(session_id) ON DELETE CASCADE              
        FOREIGN KEY (driver_id) REFERENCES Driver(driver_id) ON DELETE CASCADE
        FOREIGN KEY (team_id) REFERENCES Team(team_id) ON DELETE CASCADE                            
    );

    CREATE TABLE IF NOT EXISTS Analysis (
        analysis_id             INTEGER PRIMARY KEY AUTOINCREMENT,
        session_driver_id       INTEGER NOT NULL,
        fastest_soft_time       REAL,
        avg_med_time            REAL,
        avg_hard_time           REAL,
        best_avg_compound       TEXT,
        
        FOREIGN KEY (session_driver_id) REFERENCES DriverSessionParticipation(session_driver_id) ON DELETE CASCADE
    );
                      
    CREATE INDEX IF NOT EXISTS idx_session_event ON Session(event_id);
    CREATE INDEX IF NOT EXISTS idx_team_session ON Team(session_id);
    CREATE INDEX IF NOT EXISTS idx_driver_session ON DriverSessionParticipation(session_id, driver_id);
    CREATE INDEX IF NOT EXISTS idx_analysis_participation ON Analysis(session_driver_id);
    ''')

def insert_event(conn, name, year):
    cur = conn.cursor()
    name = name.strip().title()
    cur.execute("SELECT event_id FROM Event WHERE (name, year) = (?, ?)", (name, year))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Event (name, year) VALUES (?, ?)",
                (name, year))
    event_id = cur.lastrowid
    return event_id

def insert_session(conn, event_id, name, session_key):
    cur = conn.cursor()
    name = name.strip().title()
    cur.execute("SELECT session_id FROM Session WHERE event_id = ? AND name = ?", (event_id, name))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Session (event_id, name, session_key) VALUES (?, ?, ?)",
                (event_id, name, session_key))
    session_id = cur.lastrowid
    return session_id

def get_or_create_team(conn, session_id, name):
    cur = conn.cursor()
    name = name.strip().title()
    cur.execute("SELECT team_id FROM Team WHERE session_id = ? AND name = ?", (session_id, name))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Team (session_id, name) VALUES (?, ?)",
                (session_id, name))
    return cur.lastrowid

def get_or_create_driver(conn, name, number):
    cur = conn.cursor()
    name = name.strip().title()
    cur.execute("SELECT driver_id FROM Driver WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO Driver (name, number) VALUES (?, ?)",
                (name, number))
    return cur.lastrowid

def insert_driver_session(conn, session_id, driver_id, team_id, number):
    cur = conn.cursor()
    cur.execute('''
        SELECT session_driver_id FROM DriverSessionParticipation
        WHERE session_id = ? and driver_id = ?''',
        (session_id, driver_id,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute('''
        INSERT INTO DriverSessionParticipation (session_id, driver_id, team_id, number)
        VALUES (?, ?, ?, ?)''', (session_id, driver_id, team_id, number))
    return cur.lastrowid

def insert_analysis(conn, session_driver_id, fastest_soft_time, avg_med_time, avg_hard_time, best_avg_compound):
    cur = conn.cursor()
    cur.execute('''
                INSERT INTO Analysis (session_driver_id, fastest_soft_time, avg_med_time, avg_hard_time, best_avg_compound)
                VALUES (?, ?, ?, ?, ?)''', 
                (session_driver_id, fastest_soft_time, avg_med_time, avg_hard_time, best_avg_compound)
                )
    analysis_id = cur.lastrowid
    return analysis_id

def insert_session_summary(conn, track_name, year, session_name, session_key, driver_results):
    cur = conn.cursor()
    event_id = insert_event(conn, track_name, year)
    session_id = insert_session(conn, event_id, session_name, session_key)
    for driver in driver_results:
        team_id = get_or_create_team(conn, session_id, driver.team_name)
        driver_id = get_or_create_driver(conn, driver.name, driver.number)
        session_driver_id = insert_driver_session(conn, session_id, driver_id, team_id, driver.number)

        insert_analysis(
            conn,
            session_driver_id,
            driver.fastest_soft_time,
            driver.avg_med,
            driver.avg_hard,
            driver.best_avg_compound
        )
    conn.commit()

