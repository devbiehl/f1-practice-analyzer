import sqlite3

conn = sqlite3.connect('f1_analysis.db')
cur = conn.cursor()

# View the most recent session and event
cur.execute('''
    SELECT s.session_id, s.name, e.name, e.year
    FROM Session s
    JOIN Event e ON s.event_id = e.event_id
    ORDER BY s.session_id DESC
    LIMIT 1
''')

print(cur.fetchone())


# Replace with the correct session_id
session_id_to_delete = 4

# Get the event_id before deleting the session
cur.execute("SELECT event_id FROM Session WHERE session_id = ?", (session_id_to_delete,))
event_id = cur.fetchone()[0]

# Delete the session
cur.execute("DELETE FROM Session WHERE session_id = ?", (session_id_to_delete,))

# Check if the event has any other sessions
cur.execute("SELECT COUNT(*) FROM Session WHERE event_id = ?", (event_id,))
remaining_sessions = cur.fetchone()[0]

# If no other sessions exist for that event, delete the event too
if remaining_sessions == 0:
    cur.execute("DELETE FROM Event WHERE event_id = ?", (event_id,))

conn.commit()
conn.close()
