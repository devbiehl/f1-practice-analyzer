import requests
from driver import Driver
from team import Team
from logging_config import setup_logger
logger = setup_logger()

class SessionFetcher:
    def __init__(self, track_name, session_name, year):
        self.track_name = track_name
        self.session_name = session_name
        self.year = year

    def get_session_key(self):
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

class URLBuilder:
    def __init__(self, session_key):
        self.session_key = session_key

    def lap_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/laps?session_key={self.session_key}"
        return None
    
    def tire_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/stints?session_key={self.session_key}"
        return None
    
    def driver_data_url(self):
        if self.session_key:
            return f"https://api.openf1.org/v1/drivers?session_key={self.session_key}"
        return None

class DriverBuilder:
    def __init__(self, lap_data, driver_data, tire_data):
        self.lap_data = lap_data
        self.driver_data = driver_data
        self.tire_data = tire_data
        self.drivers = {}
        self.teams = {}

    def build(self):
        logger.info("Building driver objects and assigning lap/tirre data")
        # build a name lookup number -> name
        name_map = {
            d['driver_number']: f"{d.get('first_name', '')} {d.get('last_name', '')}".strip()
            for d in self.driver_data if d.get('driver_number')
        }

        # build a team lookup
        team_map = {
            d['driver_number']: d.get('team_name', 'Unknown')
            for d in self.driver_data if d.get('driver_number')
        }

        # build stint dictionary dr number -> list of stints
        driver_stints = {}
        for stint in self.tire_data:
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
        for lap in self.lap_data:
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

        logger.debug(f"Total laps processed: {len(self.lap_data)}")
        logger.debug(f"Total drivers mapped: {len(self.drivers)}")

        return self.drivers, self.teams
    
class DataIngestor:
    def __init__(self, session_key):
        self.url_builder = URLBuilder(session_key)

    def load_data(self):
        lap_data = requests.get(self.url_builder.lap_data_url()).json()
        driver_data = requests.get(self.url_builder.driver_data_url()).json()
        tire_data = requests.get(self.url_builder.tire_data_url()).json()

        builder = DriverBuilder(lap_data, driver_data, tire_data)
        return builder.build()

 
