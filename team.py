from driver import Driver

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