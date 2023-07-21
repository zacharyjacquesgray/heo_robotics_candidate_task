import json
import matplotlib.pyplot as plt
from datetime import datetime

file_path = "iss_elset.json"

with open(file_path, "r") as json_file:
    data = json.load(json_file)

semi_major_axis_array = []
eccentricity_array = []
timestamps = [] # for first and last time stamps in dataset

# Extract relevant data to calculate altitude from ELSET data.
for item in data:
    semi_major_axis_array.append(float(item["SEMIMAJOR_AXIS"]))
    eccentricity_array.append(float(item["ECCENTRICITY"]))
    timestamps.append(item["EPOCH"])  # Extracting timestamps from the data

print("Semi-Major Axes:", semi_major_axis_array)
print("Eccentricities:", eccentricity_array)

earth_radius = 6371  # kilometers

altitude_array = []
# Altitude = (semimajor_axis * (1 - eccentricity) - earth_radius)
for semi_major_axis, eccentricity in zip(semi_major_axis_array, eccentricity_array):
    altitude_array.append(semi_major_axis * (1 - eccentricity) - earth_radius)

print("Altitudes:", altitude_array)

time_array = range(len(altitude_array))

# Convert timestamps to datetime objects
timestamps_datetime = [datetime.fromisoformat(ts) for ts in timestamps]

# Find the earliest and latest timestamps
earliest_timestamp = min(timestamps_datetime)
latest_timestamp = max(timestamps_datetime)

# Format the earliest and latest timestamps for display
earliest_date_time = earliest_timestamp.strftime("%Y-%m-%d %H:%M:%S")
latest_date_time = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")

print("Date and time of the earliest set:", earliest_date_time)
print("Date and time of the latest set:", latest_date_time)


# Plot the altitude
plt.figure()
plt.plot(time_array, altitude_array)
plt.xlabel('Time')
plt.ylabel('Altitude (km)')
plt.title('Altitude of International Space Station from 21 July 2022 to 21 July 2023')
plt.grid(True)
plt.show()
