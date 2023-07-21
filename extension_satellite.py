from skyfield.api import EarthSatellite, Topos, load
import json
import matplotlib.pyplot as plt
import numpy as np

file_path = "iss_elset.json"  # elset data as json downloaded from space-track.org

with open(file_path, "r") as json_file:
    data = json.load(json_file)

ts = load.timescale()

# Extract the epoch time with microseconds
epoch_time_str = data[0]["EPOCH"]
year = int(epoch_time_str[0:4])
month = int(epoch_time_str[5:7])
day = int(epoch_time_str[8:10])
hour = int(epoch_time_str[11:13])
minute = int(epoch_time_str[14:16])
second = int(epoch_time_str[17:19])
microsecond = int(epoch_time_str[20:]) * 1000  # Convert to microseconds

epoch_time = ts.utc(year, month, day, hour, minute, second, microsecond)

# Extract the orbital elements
mean_motion = float(data[0]["MEAN_MOTION"])
eccentricity = float(data[0]["ECCENTRICITY"])
inclination = float(data[0]["INCLINATION"])
ra_of_asc_node = float(data[0]["RA_OF_ASC_NODE"])
arg_of_pericenter = float(data[0]["ARG_OF_PERICENTER"])
semimajor_axis_km = float(data[0]["SEMIMAJOR_AXIS"])

# Calculate the orbital period in seconds
G = 6.67430e-20  # Universal gravitational constant in km^3/(kg s^2)
M = 5.97219e24   # Mass of the Earth in kg
period_seconds = 2 * np.pi * np.sqrt((semimajor_axis_km ** 3) / (G * M))

# Time array for one complete orbit (normalized between 0 and 1)
num_time_steps = 1000
time_steps = np.linspace(0, 1, num_time_steps)

# Create an Earth satellite based on the orbital elements
satellite = EarthSatellite(None, None, None, inclination, ra_of_asc_node, arg_of_pericenter, mean_motion, eccentricity, epoch_time)

# Lists to store latitude and longitude values
latitudes = []
longitudes = []

# Propagate the satellite position for each time step
for t_norm in time_steps:
    t = epoch_time + t_norm * period_seconds
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    latitudes.append(latitude)
    longitudes.append(longitude)

# Plot the latitude and longitude on an Earth diagram
plt.figure(figsize=(10, 6))
plt.plot(longitudes, latitudes, label="ISS Orbit")
plt.xlabel("Longitude (degrees)")
plt.ylabel("Latitude (degrees)")
plt.title("International Space Station (ISS) Orbit")
plt.grid(True)
plt.legend()
plt.show()