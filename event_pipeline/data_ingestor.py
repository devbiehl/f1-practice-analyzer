import requests
from .data_filter import DriverBuilder
from .logging_config import setup_logger
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

class DataIngestor:
    def __init__(self, session_key):
        self.url_builder = URLBuilder(session_key)

    def safe_get(self, url):
        if not url:
            logger.warning("Missing session_key; cannot build URL.")
            return []
        try:
            return requests.get(url).json()
        except Exception as e:
            logger.error(f"Failed to fetch data from {url}: {e}")
            return []

    def load_data(self):
        lap_data = self.safe_get(self.url_builder.lap_data_url())
        driver_data = self.safe_get(self.url_builder.driver_data_url())
        tire_data = self.safe_get(self.url_builder.tire_data_url())

        builder = DriverBuilder(lap_data, driver_data, tire_data)
        return builder.build()