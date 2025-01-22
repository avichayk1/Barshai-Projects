# import pandas as pd
# import os
#
# # Define the folder path
# folder = r"C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_271224\israel-public-transportation"
# folder = folder.replace("\\", "/")  # Ensure forward slashes
#
# # Read the data
# stop_times = pd.read_csv(os.path.join(folder, 'stop_times.txt'))
# trips = pd.read_csv(os.path.join(folder, 'trips.txt'))
# routes = pd.read_csv(os.path.join(folder, 'routes.txt'))
# stops = pd.read_csv(os.path.join(folder, 'stops.txt'))
#
# # Merge stop_times with trips on 'trip_id'
# stops_with_trips = pd.merge(stop_times, trips, on='trip_id')
#
# # Merge the result with routes on 'route_id', selecting 'route_short_name' and 'agency_id'
# stops_with_routes_and_agencies = pd.merge(
#     stops_with_trips,
#     routes[['route_id', 'route_short_name', 'agency_id', 'route_type']],
#     on='route_id'
# )
#
# # Merge with stops to get stop_name and stop_desc (for station)
# stops_with_routes_and_agencies_and_stop_name = pd.merge(
#     stops_with_routes_and_agencies,
#     stops[['stop_id', 'stop_name', 'stop_desc', 'parent_station']],
#     on='stop_id'
# )
#
#
# # Function to get trips based on route_short_name and station
# def get_trips_by_route_and_station(route_short_name_input, station_input):
#     # Filter the data based on route_short_name and station
#     filtered_data = stops_with_routes_and_agencies_and_stop_name[
#         (stops_with_routes_and_agencies_and_stop_name['route_short_name'] == route_short_name_input) &
#         (stops_with_routes_and_agencies_and_stop_name['stop_name'] == station_input)
#         ]
#
#     # If there are matching trips, print the trips details
#     if not filtered_data.empty:
#         print(f"Trips for Route: {route_short_name_input} and Station: {station_input}")
#         print(filtered_data[['trip_id', 'route_short_name', 'stop_name', 'stop_desc']])  # Adjust columns as needed
#     else:
#         print(f"No trips found for Route: {route_short_name_input} and Station: {station_input}")
#
#
# # Example of input (change these values as needed)
# route_short_name_input = input("Enter the route short name: ")
# station_input = input("Enter the station name: ")
#
# # Call the function to get the trips
# get_trips_by_route_and_station(route_short_name_input, station_input)
#######################################################################

# import pandas as pd
# import os
#
# # Define the folder path
# folder = r"C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_271224\israel-public-transportation"
# folder = folder.replace("\\", "/")  # Ensure forward slashes
#
# # Read the trips data
# trips = pd.read_csv(os.path.join(folder, 'trips.txt'))
# routes = pd.read_csv(os.path.join(folder, 'routes.txt'))
# merged_trips_and_routes= pd.merge(trips, routes[['route_id', 'route_short_name']], on='route_id')
#
# # Function to get a trip by trip_id
# def get_trip_by_trip_id(trip_id_input):
#     # Filter the trips data for the given trip_id
#     trip_data = merged_trips_and_routes[merged_trips_and_routes['trip_id'] == str(trip_id_input)]
#
#     # If trip_data is not empty, print the trip details
#     if not trip_data.empty:
#         print(f"Details for Trip ID: {trip_id_input}")
#         print(trip_data[['trip_id', 'route_id', 'service_id', 'trip_headsign','route_short_name'
#                          ]])  # Adjust columns as needed
#     else:
#         print(f"No trip found for Trip ID: {trip_id_input}")
#
#
# # Example of input (change this value as needed)
# trip_id_input = input("Enter the trip ID: ")
#
# # Call the function to get the trip by trip_id
# get_trip_by_trip_id(trip_id_input)


################################

import pandas as pd
import os

# Define the folder path
folder = r"C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_271224\israel-public-transportation"
folder = folder.replace("\\", "/")  # Ensure forward slashes

# Read the stop_times data
stop_times = pd.read_csv(os.path.join(folder, 'stop_times.txt'))
stops = pd.read_csv(os.path.join(folder, 'stops.txt'))
stops_with_stop_times = pd.merge(stop_times, stops[['stop_id','stop_name']], on='stop_id')

# Function to get a trip by trip_id and save to a CSV file
def get_station_by_trip_id(trip_id_input, output_file):
    # Filter the stop_times data for the given trip_id
    trip_data = stops_with_stop_times[stops_with_stop_times['trip_id'] == str(trip_id_input)]

    # If trip_data is not empty, save the trip details to a CSV file
    if not trip_data.empty:
        print(f"Details for Trip ID: {trip_id_input}")
        # Save the filtered data to a CSV file
        trip_data.to_csv(output_file, index=False)
        print(f"Data for Trip ID {trip_id_input} saved to {output_file}")
    else:
        print(f"No trip found for Trip ID: {trip_id_input}")

# Example of input (change this value as needed)
trip_id_input = input("Enter the trip ID: ")

# Define the output file path (you can modify the file name as needed)
output_file = os.path.join(folder, f'trip_{trip_id_input}_details.csv')

# Call the function to get the trip by trip_id and save it to CSV
get_station_by_trip_id(trip_id_input, output_file)
