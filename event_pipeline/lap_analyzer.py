from .logging_config import setup_logger
from .utils import format_time, best_avg_lap 
from .driver import Driver
from .team import Team
logger = setup_logger()

class LapAnalyzer:
    def __init__(self, drivers, teams, track_name, session_name, year):
        self.drivers = drivers
        self.teams = teams
        self.track_name = track_name
        self.session_name = session_name
        self.year = year

    def print_summary(self):
        logger.info("Creating session summary an lap time analysis")        
        # return formatted results
        print(f"\nSummary for {self.session_name.title()} at {self.track_name.title()}, {self.year}")
        print("-" * 60)

    def print_fastest_soft(self):
        # build list of tuples for fastest soft laps
        qualy_times = []
        for driver in self.drivers.values():
            fastest_soft = None
            #gets fastest soft ONLY
            soft_laps = driver.compound_laps.get('SOFT', [])
            fastest_soft = min(soft_laps) if soft_laps else None
            qualy_times.append((driver, fastest_soft))

        # Filter drivers without SOFT lap time
        qualy_times = [qt for qt in qualy_times if qt[1] is not None]
        # Sort fastest soft laps
        qualy_times.sort(key=lambda qt: qt[1])

        print(f"\nFastest Soft Tire Performance")
        print('-' * 60)
        for driver, fastest_soft in qualy_times:
            print(f"{driver.name} (#{driver.number})")
            if fastest_soft:
                print(f"    Fastest Lap (SOFT): {format_time(fastest_soft)}")

    def print_race_pace(self):
        # build list of tuples for fastest race pace
        race_pace = []
        for driver in self.drivers.values():
            best_avg, compound = best_avg_lap(driver)
            if best_avg:
                race_pace.append((driver, best_avg, compound))

        race_pace.sort(key=lambda x: x[1])
        
        print(f"\nFastest Race Pace Performance")
        print('-' * 60)
        for driver, best_avg, compound in race_pace:
            print(f"{driver.name} (#{driver.number})")
            print(f"    AVG RACE PACE ({compound}): {format_time(best_avg)}")

    def print_team_pace(self):
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
        
    def summary(self):
        self.print_summary()
        self.print_fastest_soft()
        self.print_race_pace()
        self.print_team_pace()