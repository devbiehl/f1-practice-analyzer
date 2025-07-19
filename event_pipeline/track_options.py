from collections import defaultdict
import requests
from .data_ingestor import DataIngestor
from .logging_config import setup_logger
logger = setup_logger()

class TrackBuilder:
    def __init__(self, track_data):
        self.track_data = track_data
        self.track_options = []

    def build(self):
        seen = set()
        for data in self.track_data:
            name = data.get("circuit_short_name")
            country = data.get("country_name", "Unknown")
            year = data.get("year")

            key = (name, year)
            if key not in seen:
                seen.add(key)
                self.track_options.append({
                    "name": name,
                    "country": country,
                    "year": year
                })
        return self.track_options
    
    def list_tracks(self):
        print("\nAvailable Tracks:")
        for idx, track in enumerate(self.track_options, 1):
            print(f"{idx}. {track['name']} ({track['country']}, {track['year']})")


    def pick_track(self):
        self.list_tracks()
        while True:
            choice = input("Select a track number: ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.track_options):
                    selected = self.track_options[index]
                    logger.info(f"Selected track: {selected['name']} ({selected['country']}, {selected['year']})")
                    return selected['name']
            logger.warning("Invalid entry. Select again")
    

class TrackOptions:
    def __init__(self, year):
        self.year = year

    def safe_get(self, url):
        try:
            return requests.get(url).json()
        except Exception as e:
            logger.error(f"Failed to fetch from {url}: {e}")
            return []

    def get_track_options(self):
        url = f"https://api.openf1.org/v1/meetings?year={self.year}"
        track_data = self.safe_get(url)
        track_builder = TrackBuilder(track_data)
        return track_builder.build(), track_builder