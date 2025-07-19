from collections import defaultdict
from .driver import Driver
from .team import Team
from .logging_config import setup_logger
logger = setup_logger()

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
            driver_stints.setdefault(driver, []).append({
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
        
        # Temporary structure driver -> comp -> laps
        compound_laps_temp = defaultdict(lambda: defaultdict(list))

        # first pass: collect all laps
        for lap in self.lap_data:
            driver = lap.get('driver_number')
            lap_time = lap.get('lap_duration')
            lap_number = lap.get('lap_number')
            is_valid = not lap.get('deleted', False)
            is_pit_out = lap.get('is_pit_out_lap', False)

            if not driver or lap_time is None or not is_valid or is_pit_out:
                continue # skip out laps

            compound = get_compound(driver, lap_number)
            compound_laps_temp[driver][compound].append((lap_time, lap_number))

        # second pass: filter and assign to objects
        for driver, compound_data in compound_laps_temp.items():
            name = name_map.get(driver, f"Driver {driver}")
            team = team_map.get(driver, "Unknown")

            # Add driver object if not already in self.drivers
            if driver not in self.drivers:
                self.drivers[driver] = Driver(name=name, number=driver, team_name=team)
                if team not in self.teams:
                    self.teams[team] = Team(name=team)
                self.teams[team].add_driver(self.drivers[driver])
            
            for compound, laps in compound_data.items():
                if not laps:
                    continue

                filtered_laps = []
                
                if compound in ("MEDIUM", "HARD"):
                    if len(laps) >= 5:
                        sorted_laps = sorted(laps, key=lambda x: x[0])
                        cutoff_idx = int(len(sorted_laps) * 0.9)
                        filtered_laps = sorted_laps[:cutoff_idx]
                    else:
                        fastest = min(t[0] for t in laps)
                        cutoff = max(fastest * 1.04, 65)
                        filtered_laps = [lap for lap in laps if lap[0] <= cutoff]
                else: 
                    fastest = min(t[0] for t in laps)
                    cutoff = max(fastest * 1.08, 65)
                    filtered_laps = [lap for lap in laps if lap[0] <= cutoff]


                for lap_time, lap_number in filtered_laps:
                    self.drivers[driver].add_lap(lap_time, compound)

        logger.debug(f"Total laps processed: {len(self.lap_data)}")
        logger.debug(f"Total drivers mapped: {len(self.drivers)}")

        return self.drivers, self.teams
    