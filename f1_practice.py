import json
import requests
from collections import defaultdict

def get_session_key(track_name, session_name, year):
    # Get all sessions
    response = requests.get('https://api.openf1.org/v1/sessions')
    data = response.json()

    # get session key from track name and session type. with error handling
    found_track = False
    for session in data:
        if (session.get('circuit_short_name', '').lower() == track_name.lower() and session.get('year') == int(year)):
            found_track = True
            if session.get('session_name', '').lower() == session_name.lower():
                return session.get('session_key')
    
    if not found_track:
        print(f"Track name '{track_name}' not found for year {year}.")
    else: 
        print(f"Session name '{session_name}' not found for track: '{track_name}'.")

    # return none if no match found
    return None

def build_lap_data_url(session_key):
    if session_key:
        return f"https://api.openf1.org/v1/laps?session_key={session_key}"
    return None

def build_tire_data_url(session_key):
    if session_key:
        return f"https://api.openf1.org/v1/stints?session_key={session_key}"
    return None

def build_driver_data_url(session_key):
    if session_key:
        return f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    return None

def build_stints(tire_data):
    driver_stints = {}

    for stint in tire_data:
        driver = stint['driver_number']
        start_lap = stint['lap_start']
        end_lap = stint['lap_end']
        if driver not in driver_stints:
            driver_stints[driver] = []
        driver_stints[driver].append({
            'stint_number': stint['stint_number'],
            'compound': stint['compound'],
            'start_lap': start_lap,
            'end_lap': end_lap
        })

    return driver_stints

def get_compound_for_lap(driver_stints, driver_number, lap_number):
    if driver_number not in driver_stints:
        return "Unknown"
    for stint in driver_stints[driver_number]:
        if stint['start_lap'] <= lap_number <= stint['end_lap']:
            return stint['compound']
    return 'Unknown'

def get_fastest_soft_laps(lap_data, driver_stints):
    # Returns list of (driver_number, fastest_soft_lap_time)
    # Only including valid laps
    driver_soft_laps = {}

    for lap in lap_data:
        driver = lap.get('driver_number')
        lap_time = lap.get('lap_duration')
        lap_number = lap.get('lap_number')
        is_valid = lap.get('deleted') == False
        is_pit_out = lap.get('is_pit_out_lap', False)

        if driver and lap_time is not None and lap_time <=85 and not is_pit_out:
            compound = get_compound_for_lap(driver_stints, driver, lap_number)
            if compound == "SOFT":
                if driver not in driver_soft_laps or lap_time < driver_soft_laps[driver]:
                    driver_soft_laps[driver] = lap_time
    
    return sorted(driver_soft_laps.items(), key=lambda t: t[1])


def get_avg_time_per_compound(lap_data, driver_stints, compounds=["MEDIUM", "HARD"]):
    lap_totals = defaultdict(lambda: defaultdict(list))

    for lap in lap_data:
        driver = lap.get('driver_number')
        lap_time = lap.get('lap_duration')
        lap_number = lap.get('lap_number')
        is_pit_out = lap.get('is_pit_out_lap', False)
    
        if driver and lap_time is not None and lap_time <= 90 and not is_pit_out:
            compound = get_compound_for_lap(driver_stints, driver, lap_number)
            #print(f"Found lap: Driver {driver}, Lap {lap_number}, Compound {compound}, Time {lap_time}")
            if compound in compounds:
                lap_totals[driver][compound].append(lap_time)
    result = {}
    for driver, compound_times in lap_totals.items():
        result[driver] = {
            compound: sum(times) / len(times)
            for compound, times in compound_times.items()
        }

    return sorted(result.items(), key=lambda t: t[1].get('MEDIUM', float('inf')))

def attach_driver_names(time_data, driver_data):
    name_map = {
        d['driver_number']: f"{d.get('first_name', '')} {d.get('last_name', '')}" 
        for d in driver_data if d.get('driver_number')
        }
    
    result = []
    for driver, lap_time in time_data:
        name = name_map.get(driver, "Unknown")
        result.append({
            'driver_number': driver,
            'name': name,
            'lap_time': lap_time
        })
    
    return result

def attach_driver_names_by_compound(time_data, driver_data):
    name_map = {
        d['driver_number']: f"{d.get('first_name', '')} {d.get('last_name', '')}" 
        for d in driver_data if d.get('driver_number')
        }
    
    result = []
    for driver, compound_times in time_data:
        name = name_map.get(driver, "Unknown")
        for compound, lap_time in compound_times.items():
            result.append({
                'driver_number': driver,
                'name': name,
                'compound': compound,
                'lap_time': lap_time
            })
    
    return result

def minutes_conversion(seconds):
    minutes = int(seconds // 60)
    remainder = seconds % 60
    return f"{minutes}:{remainder:06.3f}"

def summary_report(fastest_soft_time, avg_medhard_time, session_name, output_file):
    report = (
        f"SUMMARY OF {session_name.upper()}\n\n"
        f"\n\nFastest Drivers in Qualifying simulations\n\n"
    )
    for driver in fastest_soft_time:
        formatted_time = minutes_conversion(driver['lap_time'])
        report += f"{driver['name']}: {formatted_time}\n"

    report += f"\n\nFastest Drivers in Race simulations by Compound\n\n"

    for driver in avg_medhard_time:
        formatted_time = minutes_conversion(driver['lap_time'])
        report += f"{driver['name']} ({driver['compound']}): {formatted_time}\n"

    with open(output_file, 'w') as file:
        file.write(report)


def main():
    track_name = input("Enter track name (e.g. Spa-Francorchamps): ")
    session_name = input("Enter session name (e.g. Practice 1): ")
    year = input("Enter year (e.g. 2025): ")
    output_file = input("Enter new file name(.txt format): ")
    session_key = get_session_key(track_name, session_name, year)

    if session_key:
        lap_url = build_lap_data_url(session_key)
        driver_url = build_driver_data_url(session_key)
        tire_url = build_tire_data_url(session_key)

        lap_data = requests.get(lap_url).json()
        driver_data = requests.get(driver_url).json()
        tire_data = requests.get(tire_url).json()

        driver_stints = build_stints(tire_data)

        fastest_qual_sim = get_fastest_soft_laps(lap_data, driver_stints)
        avg_race_pace = get_avg_time_per_compound(lap_data, driver_stints)

        fastest_soft_time = attach_driver_names(fastest_qual_sim, driver_data)
        avg_medhard_time = attach_driver_names_by_compound(avg_race_pace, driver_data)

        summary_report(fastest_soft_time, avg_medhard_time, session_name, output_file)

if __name__ == '__main__':
    main()
