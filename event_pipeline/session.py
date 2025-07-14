from .data_ingestor import SessionFetcher, DataIngestor
from .lap_analyzer import LapAnalyzer
from .db_handler import DBHandler
from .logging_config import setup_logger

class Session:
    def __init__(self, track_name, session_name, year):
        self.track_name = track_name
        self.session_name = session_name
        self.year = year
        self.session_key = None
        self.drivers = {}
        self.teams = {}

    def run(self):
        logger = setup_logger(self.track_name, self.session_name)

        self.session_key = SessionFetcher(self.track_name, self.session_name, self.year).get_session_key()
        if not self.session_key:
            logger.error("Invalid session key.")
            return
        
        self.drivers, self.teams = DataIngestor(self.session_key).load_data()

        analyzer = LapAnalyzer(self.drivers, self.teams, self.track_name, self.session_name, self.year)
        analyzer.summary()

        db = DBHandler(self.drivers, self.track_name, self.session_name, self.year, self.session_key)
        db.save_to_db()