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
    def prepare_summary(self):
        self.fastest_soft_time = min(self.compound_laps.get("SOFT", []), default=None)
        self.avg_med = self.avg_lap_time("MEDIUM")
        self.avg_hard = self.avg_lap_time("HARD")
        self.best_avg, self.best_avg_compound = self.best_avg_compound()