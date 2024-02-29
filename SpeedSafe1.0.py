import googlemaps
from datetime import datetime
import polyline
import matplotlib.pyplot as plt
import numpy as np

# Defining Lists before appended
gps_points = []
colors = []

# Initialising gMaps Client
API_KEY = 'GOOGLE_MAPS_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

# Defining Arguments and calling gmaps direction function
origin = "Origin"
destination = "Destination"
directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=datetime.now())

# Decoding Polyline in direction results
for step in directions_result[0]['legs'][0]['steps']:
    encoded_polyline = step['polyline']['points']
    decoded_polyline = polyline.decode(encoded_polyline)
    gps_points.extend(decoded_polyline)

# Extract latitude and longitude coordinates
latitudes = [point[0] for point in gps_points]
longitudes = [point[1] for point in gps_points]

# Calculate filtered points using moving average / sliding window
window_size = 5
x_filtered = np.convolve(longitudes, np.ones(window_size) / window_size, mode='valid')
y_filtered = np.convolve(latitudes, np.ones(window_size) / window_size, mode='valid')

# Calculating magnitude of gradient change
dx = np.gradient(x_filtered)
dy = np.gradient(y_filtered)
gradient_change_list = 1 / np.sqrt(dx ** 2 + dy ** 2)

for change in gradient_change_list:
    if change < 10000:              # Very low gradient change (straight section) - blue
        colors.append('blue')
    elif 10000 < change < 15000:    # Low gradient change (shallow corner) - yellow
        colors.append('yellow')
    elif 15000 < change < 20000:    # Moderate gradient change (moderate corner) - orange
        colors.append('orange')
    else:                           # High gradient change (sharp corner) - red
        colors.append('red')

# Plot the data
plt.scatter(x_filtered, y_filtered, color=colors, label='Filtered Data', zorder=3)
plt.plot(longitudes, latitudes, '-', color='black', label='Route')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Interpolated Curve through GPS Points')
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()
