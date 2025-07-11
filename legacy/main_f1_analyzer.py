import requests
import json
import sqlite3
from logging_config import setup_logger
from f1db import connect_db, create_table, insert_session_summary

logger = setup_logger()

class Driver:
    def __init__(self, name, number, team_name=None):
        self.number = number
        self.name = name
        self.team_name = team_name
        self.lap_times = []
        self.compound_laps = {} # compound --> list of lap times

    def add_lap(self, lap_time, compound):
        # driver lap builder
        self.lap_times.append(lap_time)
        if compound not in self.compound_laps:
            self.compound_laps[compound] = []
        self.compound_laps[compound].append(lap_time)

    def avg_lap_time(self, compound=None):
        # avg lap builder
        if compound:
            laps = self.compound_laps.get(compound, [])
        else:
            laps = self.lap_times     
        return sum(laps) / len(laps) if laps else None

    def fastest_lap_time(self, compound='SOFT'):
        # fastest lap builder
        laps = self.compound_laps.get(compound, [])
        return min(self.lap_times) if self.lap_times else None
    
    def best_avg_compound(self):
        med = self.avg_lap_time("MEDIUM")
        hard = self.avg_lap_time("HARD")
        if med and (not hard or med < hard):
            return med, "MEDIUM"
        elif hard:
            return hard, "HARD"
        else:
            return None, None


class Team:
    def __init__(self, name):
        self.name = name
        self.drivers = []

    def add_driver(self, driver):
        # add drivers to team
        self.drivers.append(driver)
    
    def team_avg(self, compound=None):
        # avg lap times of teams
        avg_times = [driver.avg_lap_time(compound) for driver in self.drivers if driver.avg_lap_time(compound)]
        return sum(avg_times) / len(avg_times) if avg_times else None

class Session:
    def __init__(self, track_name, session_name, year):
        self.track_name = track_name
        self.session_name = session_name
        self.year = year
        self.drivers = {}
        self.teams = {}

    def fetch_data(self):
        #call API + build driver objects
            # Get all sessions
        logger.info(f"Fetching session key for: {self.track_name} - {self.session_name} ({self.year})")
        self.session_key = None
        response = requests.get('https://api.openf1.org/v1/sessions')
        data = response.json()

        # get session key from track name and session type. with error handling
        found_track = False
        for session in data:
            if (session.get('circuit_short_name', '').lower() == self.track_name.lower() and session.get('year') == int(self.year)):
                found_track = True
                if session.get('session_name', '').lower() == self.session_name.lower():
                    self.session_key = session.get('session_key')
                    logger.info(f"Found session_key: {self.session_key}")
                    return self.session_key
        
        if not found_track:
            logger.warning(f"Track '{self.track_name}' not found for year {self.year}")
        elif self.session_key is None:
            logger.warning(f"Session '{self.session_name}' not found at track '{self.track_name}'")


        # return none if no match found
        return None

    def build_lap_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/laps?session_key={self.session_key}"
        return None

    def build_tire_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/stints?session_key={self.session_key}"
        return None

    def build_driver_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/drivers?session_key={self.session_key}"
        return None


    def build_driver_objects(self):
        logger.info("Building driver objects and assigning lap/tirre data")
        # parse lap_data, assign to each driver
        if not self.session_key:
            print("Session key not set. Call fetch_data() first.")
            return
        
        #fetch raw data
        lap_url = self.build_lap_data_url()
        driver_url = self.build_driver_data_url()
        tire_url = self.build_tire_data_url()

        lap_data = requests.get(lap_url).json()
        driver_data = requests.get(driver_url).json()
        tire_data = requests.get(tire_url).json()

        # build a name lookup number -> name
        name_map = {
            d['driver_number']: f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
            for d in driver_data if d.get('driver_number')
        }

        # build a team lookup
        team_map = {
            d['driver_number']: d.get('team_name', 'Unknown')
            for d in driver_data if d.get('driver_number')
        }

        # build stint dictionary dr number -> list of stints
        driver_stints = {}
        for stint in tire_data:
            driver = stint['driver_number']
            if driver not in driver_stints:
                driver_stints[driver] = []
            driver_stints[driver].append({
                'stint_number': stint['stint_number'],
                'compound': stint['compound'],
                'start_lap': stint['lap_start'],
                'end_lap': stint['lap_end']
            })

        # Helper to get compound per lap
        def get_compound(driver_number, lap_number):
            stints = driver_stints.get(driver_number, [])
            for stint in stints:
                if stint['start_lap'] <= lap_number <= stint['end_lap']:
                    return stint['compound']
            return "Unknown"
        
        # Parse laps and populate driver objects
        for lap in lap_data:
            driver = lap.get('driver_number')
            lap_time = lap.get('lap_duration')
            lap_number = lap.get('lap_number')
            is_valid = not lap.get('deleted', False)
            is_pit_out = lap.get('is_pit_out_lap', False)

            if not driver or lap_time is None or not is_valid or is_pit_out or lap_time > 90:
                continue # skip out laps

            name = name_map.get(driver, f"Driver {driver}")
            team = team_map.get(driver, "Unknown")

            # Add driver object if not already in self.drivers
            if driver not in self.drivers:
                self.drivers[driver] = Driver(name=name, number=driver, team_name=team)

                if team not in self.teams:
                    self.teams[team] = Team(name=team)
                self.teams[team].add_driver(self.drivers[driver])

            compound = get_compound(driver, lap_number)
            self.drivers[driver].add_lap(lap_time, compound)

        logger.debug(f"Total laps processed: {len(lap_data)}")
        logger.debug(f"Total drivers mapped: {len(self.drivers)}")
    def summary(self):
        logger.info("Creating session summary an lap time analysis")
        # helper func to sort avg times
        def best_avg_lap(obj):
            if isinstance(obj, Driver):
                med = obj.avg_lap_time("MEDIUM")
                hard = obj.avg_lap_time("HARD")
            elif isinstance(obj, Team):
                med = obj.team_avg("MEDIUM")
                hard = obj.team_avg("HARD")
            else:
                return None, None # unexpected type fallback
            
            compound_times = {
                'MEDIUM': med,
                'HARD': hard
            }

            valid = {comp: t for comp, t in compound_times.items() if t is not None}

            if not valid:
                return None, None # fallback

            best_compound = min(valid, key=valid.get)
            return valid[best_compound], best_compound
        
        # return formatted results
        print(f"\nSummary for {self.session_name.title()} at {self.track_name.title()}, {self.year}")
        print("-" * 60)

        # build list of tuples for fastest soft laps
        qualy_times = []
        for driver in self.drivers.values():
            fastest_soft = None
            #gets fastest soft ONLY
            soft_laps = driver.compound_laps.get('SOFT', [])
            if soft_laps:
                fastest_soft = min(soft_laps)
            qualy_times.append((driver, fastest_soft))

        # Filter drivers without SOFT lap time
        qualy_times = [qt for qt in qualy_times if qt[1] is not None]

        # Sort fastest soft laps
        qualy_times.sort(key=lambda qt: qt[1])

        # build list of tuples for fastest race pace
        race_pace = []
        for driver in self.drivers.values():
            best_avg, compound = best_avg_lap(driver)
            if best_avg:
                race_pace.append((driver, best_avg, compound))

        race_pace.sort(key=lambda x: x[1])

        print(f"\nFastest Soft Tire Performance")
        print('-' * 60)
        for driver, fastest_soft in qualy_times:
            print(f"{driver.name} (#{driver.number})")
            if fastest_soft:
                print(f"    Fastest Lap (SOFT): {format_time(fastest_soft)}")
        
        print(f"\nFastest Race Pace Performance")
        print('-' * 60)

        for driver, best_avg, compound in race_pace:
            print(f"{driver.name} (#{driver.number})")
            print(f"    AVG RACE PACE ({compound}): {format_time(best_avg)}")

        team_pace = []
        for team in self.teams.values():
            best_avg, compound = best_avg_lap(team)
            if best_avg:
                team_pace.append((team, best_avg, compound))

        team_pace.sort(key=lambda x: x[1])

        print("\n--- Team Race Pace Averages (MEDIUM/HARD) ---")
        for team, best_avg, compound in team_pace:
            if best_avg:
                print(f"{team.name}: {format_time(best_avg)} ({compound})")
        print()
    def save_to_db(self):
        if not self.session_key:
            logger.warning("No session_key found - skipping database insert.")
            return
        
        import os
        logger.info("Saving session summary to database")
        
        conn = connect_db()

        # Only run schema creation if DB file doesnt exist
        if not os.path.exists('f1_analysis.db'):
            logger.info("Database not found. Creating schema.")
            create_table(conn)

        # BUild driver results for database
        driver_results = []
        for driver in self.drivers.values():
            soft_laps = driver.compound_laps.get("SOFT", [])
            fastest_soft = min(soft_laps) if soft_laps else None
            avg_med = driver.avg_lap_time("MEDIUM")
            avg_hard = driver.avg_lap_time("HARD")
            best_avg, best_compound = driver.best_avg_compound()

            # Insert values into object
            driver.fastest_soft_time = fastest_soft
            driver.avg_med = avg_med
            driver.avg_hard = avg_hard
            driver.best_avg_compound = best_compound

            driver_results.append(driver)

        logger.debug(f"Number of drivers to save: {len(driver_results)}")
        insert_session_summary(conn, self.track_name, self.year, self.session_name, self.session_key, driver_results)
        conn.commit()
        conn.close()

            

def format_time(seconds):
    if seconds is None:
        return "N/A"
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:06.3f}"

def run_f1_analysis():
    try:
        track_name = input('Enter Track Name(e.g. Catalunya): ').strip().title()
        session_name = input('Enter Session Name(e.g. Practice 1): ').strip().title()
        year = input('Enter race year(e.g. 2025): ').strip()

        global logger
        logger = setup_logger(track_name, session_name)

        session = Session(track_name, session_name, year)
        session.fetch_data()
        if not session.session_key:
            logger.error("Invalid session input. Exiting early.")
            return
        session.build_driver_objects()
        session.summary()
        session.save_to_db()
        logger.info("Run completed successfully.")
    except Exception as e:
        logger.exception("Unhandled exception during run:")

if __name__ == '__main__':
    run_f1_analysis()