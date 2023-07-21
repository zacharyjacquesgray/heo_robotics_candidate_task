import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from datetime import datetime

file_path = "iss_elset.json"  # elset data as json downloaded from space-track.org 

with open(file_path, "r") as json_file:
    data = json.load(json_file)

# Relevant data initialisations for altitude data and its associated timestamp
semi_major_axis_array = []
eccentricity_array = []
timestamps = []

# Extract relevant data to calculate altitude from ELSET json
for item in data:
    semi_major_axis_array.append(float(item["SEMIMAJOR_AXIS"]))
    eccentricity_array.append(float(item["ECCENTRICITY"]))
    timestamps.append(item["EPOCH"])

earth_radius = 6371  # kilometres

# Calculate altitudes over the year
altitude_array = []
# Altitude = (semimajor_axis * (1 - eccentricity) - earth_radius)
for semi_major_axis, eccentricity in zip(semi_major_axis_array, eccentricity_array):
    altitude_array.append(semi_major_axis * (1 - eccentricity) - earth_radius)

# Convert timestamps to datetime objects
timestamps_datetime = [datetime.fromisoformat(ts) for ts in timestamps]

# Find the earliest and latest datetimes obtained
earliest_timestamp = min(timestamps_datetime)
latest_timestamp = max(timestamps_datetime)

# Print dates obtained to console.
earliest_date_time = earliest_timestamp.strftime("%d-%m-%Y %H:%M:%S")
latest_date_time = latest_timestamp.strftime("%d-%m-%Y %H:%M:%S")
print("Datetime of the earliest data obtained:", earliest_date_time)
print("Datetime of the latest data obtained:", latest_date_time)

# Set time array
time_array = np.linspace(earliest_timestamp.timestamp(), latest_timestamp.timestamp(), len(altitude_array))

# Plot the altitude
plt.figure()
plt.plot(timestamps_datetime, altitude_array)
plt.xlabel('21 July 2022 - 21 July 2023')
plt.ylabel('Altitude (km)')

# Set ticks and labels for the months
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))

plt.title('Mean Altitude of International Space Station from 21 July 2022 to 21 July 2023')
plt.grid(True)

plt.show()