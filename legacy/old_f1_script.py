import urllib.request
import json
# F1 API URL
url = 'https://ergast.com/api/f1/2023/1/laps.json?limit=2000'

# Request data and read response
response = urllib.request.urlopen(url)
data = response.read().decode()

# parse the JSON data
laps_data = json.loads(data)

# read the JSON to find keys to loop
#print(json.dumps(laps_data, indent=4))

# created a function to convert to seconds
def seconds_conversion(timing):
    time_str = timing['time'] # 'str' to keep format
    #convert to seconds
    mins, seconds = map(float, time_str.split(':'))
    total_seconds = mins * 60 + seconds
    return total_seconds

# and one to convert back to minutes
def minutes_conversion(seconds):
    minutes = int(seconds // 60)
    remainder = seconds % 60
    return f"{minutes}:{remainder:.3f}"

#extract all lap times by driver
driver_laps = {}
for lap in laps_data['MRData']['RaceTable']['Races'][0]['Laps']:
    for timing in lap['Timings']:
        driver = timing['driverId']
        lap_seconds = seconds_conversion(timing)
        
        # add to dict
        driver_laps.setdefault(driver, []).append(lap_seconds)

#find the average lap time of drivers
driver_averages = {
    driver: sum(times) / len(times)
    for driver, times in driver_laps.items()
    if len(times) >= 5 #Filter drivers who didnt complete enough laps
}

# sort by fastest lap time average
sorted_averages = sorted(driver_averages.items(), key=lambda times: times[1])

#find the finsihing position

results_url = 'https://ergast.com/api/f1/2023/1/results.json'

results_response = urllib.request.urlopen(results_url)
results_data = results_response.read().decode()

finish_pos = json.loads(results_data)

#print(json.dumps(finish_pos, indent=4))

finishing_info = {}

# loop to find driver name, constructor and finish position
for finish in finish_pos['MRData']['RaceTable']['Races'][0]['Results']:
    driver_id = finish['Driver']['driverId']
    full_name = finish['Driver']['givenName'] + ' ' + finish['Driver']['familyName']
    constructor_name = finish['Constructor']['name']
    position = finish['position']

    # add to dict
    finishing_info[driver_id] = {
        'name': full_name,
        'position': position,
        'constructor': constructor_name
    }

# print name, avg lap time, finish pos, and team
for driver, avg_time in sorted_averages:
    info = finishing_info.get(driver, {'name': driver, 'position': 'N/A', 'constructor': 'N/A'})
    formatted_time = minutes_conversion(avg_time)
    print(f"{info['name']} ({info['constructor']}) - Average Lap Time: {formatted_time} (Position: {info['position']})")
