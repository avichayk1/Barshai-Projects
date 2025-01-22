import pandas as pd
import os

# Define the folder path
folder = r"C:\Users\AvichayKadosh\ברשאי\ברשאי - תיקיית ברשאי\לקוחות\משרד התחבורה\הרשות לתחצ\אגף טכנולוגיה\GTFS\DATA\weekly_gtfs\gtfs_090125\israel-public-transportation"
folder = folder.replace("\\", "/")  # Ensure forward slashes

# Read the data
stop_times = pd.read_csv(os.path.join(folder, 'stop_times.txt'))
trips = pd.read_csv(os.path.join(folder, 'trips.txt'))
routes = pd.read_csv(os.path.join(folder, 'routes.txt'))
stops = pd.read_csv(os.path.join(folder, 'stops.txt'))

# Merge stop_times with trips on 'trip_id'
stops_with_trips = pd.merge(stop_times, trips, on='trip_id')

# Merge the result with routes on 'route_id', selecting 'route_short_name' and 'agency_id'
stops_with_routes_and_agencies = pd.merge(
    stops_with_trips,
    routes[['route_id', 'route_short_name', 'agency_id', 'route_type']],
    on='route_id'
)

stops_with_routes_and_agencies_and_stop_name = pd.merge(
    stops_with_routes_and_agencies,
    stops[['stop_id','stop_code', 'stop_name', 'stop_desc', 'parent_station']],
    on='stop_id'
)

# Filter out rows where route_type equals 2 - rail
filtered_stops_with_routes_and_agencies = stops_with_routes_and_agencies_and_stop_name#[stops_with_routes_and_agencies_and_stop_name['route_type'] != 2]

# Extract 'city' from 'stop_desc' using regex
filtered_stops_with_routes_and_agencies['city'] = filtered_stops_with_routes_and_agencies['stop_desc'].str.extract(r'עיר:\s*(.*?)\s*רציף')

# Select relevant columns: 'stop_id', 'route_short_name', 'agency_id', and 'city'
result = filtered_stops_with_routes_and_agencies[['stop_id','stop_code','stop_name','city', 'route_short_name', 'agency_id', 'parent_station','route_id']]

# Group by 'stop_id' and aggregate route_short_name and agency_id as comma-separated strings
grouped = result.groupby('stop_id').agg({
    'stop_code': 'first',
    'stop_name': 'first',
    'city': 'first',  # Just take the first city value for each stop_id
    'route_id': 'first',
    'route_short_name': lambda x: ', '.join(sorted(set(map(str, x)))),  # Convert to strings before joining
    'agency_id': lambda x: ', '.join(map(str, sorted(set(x)))),  # Ensure all agency_ids are strings
    'parent_station':'first'
}).reset_index()

# Add counts for route_short_name and agency_id
grouped['route_short_name_count'] = grouped['route_short_name'].apply(lambda x: len(x.split(', ')))
grouped['agency_id_count'] = grouped['agency_id'].apply(lambda x: len(x.split(', ')))

# Convert route_short_name and agency_id columns to remove any unwanted characters
grouped['route_short_name'] = grouped['route_short_name'].str.replace(r"[\[\]']+", "", regex=True)
grouped['agency_id'] = grouped['agency_id'].str.replace(r"[\[\]']+", "", regex=True)

# Save the result to a new CSV file
output_file = os.path.join(folder, 'stops_routes_agencies_with_counts_and_city_train.csv')
grouped.to_csv(output_file, index=False, encoding='utf-8')

print(f"File saved to: {output_file}")
############################################
#
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
# stops_with_routes_and_agencies_and_stop_name = pd.merge(
#     stops_with_routes_and_agencies,
#     stops[['stop_id', 'stop_name','stop_code', 'stop_desc', 'parent_station']],
#     on='stop_id'
# )
#
# # Filter out rows where route_type equals 2 - rail
# filtered_stops_with_routes_and_agencies = stops_with_routes_and_agencies_and_stop_name[stops_with_routes_and_agencies_and_stop_name['route_type'] != 2]
#
# # Extract 'city' from 'stop_desc' using regex
# filtered_stops_with_routes_and_agencies['city'] = filtered_stops_with_routes_and_agencies['stop_desc'].str.extract(r'עיר:\s*(.*?)\s*רציף')
#
# # Select relevant columns: 'stop_id', 'route_short_name', 'agency_id', and 'city'
# result = filtered_stops_with_routes_and_agencies[['stop_id','stop_code','stop_name','city', 'route_short_name', 'agency_id', 'parent_station','route_id']]
# # Filter rows where parent_station is empty or NaN
# result = result[~result['parent_station'].isnull()]
# # Group by 'stop_id' and aggregate route_short_name and agency_id as comma-separated strings
# grouped = result.groupby('stop_id').agg({
#     'stop_code': 'first',
#     'stop_name': 'first',
#     'city': 'first',  # Just take the first city value for each stop_id
#     'route_short_name': lambda x: ', '.join(sorted(set(map(str, x)))),  # Convert to strings before joining
#     'agency_id': lambda x: ', '.join(map(str, sorted(set(x)))),  # Ensure all agency_ids are strings
#     'parent_station':'first'
# }).reset_index()
#
# # Add counts for route_short_name and agency_id
# grouped['route_short_name_count'] = grouped['route_short_name'].apply(lambda x: len(x.split(', ')))
# grouped['agency_id_count'] = grouped['agency_id'].apply(lambda x: len(x.split(', ')))
#
# # Convert route_short_name and agency_id columns to remove any unwanted characters
# grouped['route_short_name'] = grouped['route_short_name'].str.replace(r"[\[\]']+", "", regex=True)
# grouped['agency_id'] = grouped['agency_id'].str.replace(r"[\[\]']+", "", regex=True)
#
# # Save the result to a new CSV file
# output_file = os.path.join(folder, 'stops_routes_agencies_with_counts_and_city_just_central_station.csv')
# grouped.to_csv(output_file, index=False, encoding='utf-8')
#
# print(f"File saved to: {output_file}")

#########################################
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
# agency=pd.read_csv(os.path.join(folder, 'agency.txt'))
# # Merge stop_times with trips on 'trip_id'
# stops_with_trips = pd.merge(stop_times, trips, on='trip_id')
# # Merge the result with routes on 'route_id', selecting 'route_short_name' and 'agency_id'
# stops_with_routes_and_agencies = pd.merge(
#     stops_with_trips,
#     routes[['route_id', 'route_short_name', 'agency_id', 'route_type']],
#     on='route_id'
# )
# stops_with_routes_and_agencies=pd.merge(stops_with_routes_and_agencies, agency[['agency_id','agency_name']], on='agency_id')
#
# stops_with_routes_and_agencies_and_stop_name = pd.merge(
#     stops_with_routes_and_agencies,
#     stops[['stop_id', 'stop_name', 'stop_desc', 'parent_station']],
#     on='stop_id'
# )
#
# # Filter out rows where route_type equals 2 - rail
# filtered_stops_with_routes_and_agencies = stops_with_routes_and_agencies_and_stop_name[stops_with_routes_and_agencies_and_stop_name['route_type'] != 2]
#
# # Extract 'city' from 'stop_desc' using regex
# filtered_stops_with_routes_and_agencies['city'] = filtered_stops_with_routes_and_agencies['stop_desc'].str.extract(r'עיר:\s*(.*?)\s*רציף')
#
# # Select relevant columns: 'stop_id', 'route_short_name', 'agency_id', and 'city'
# result = filtered_stops_with_routes_and_agencies[['stop_id','stop_name','city', 'route_short_name', 'agency_id','agency_name', 'parent_station','route_id']]
#
# # Group by 'stop_id' and aggregate route_short_name and agency_id as comma-separated strings
# # grouped = result.groupby('stop_id').agg({
# #     'stop_name': 'first',
# #     'city': 'first',  # Just take the first city value for each stop_id
# #     'route_short_name': lambda x: ', '.join(sorted(set(map(str, x)))),  # Convert to strings before joining
# #     'agency_id': lambda x: ', '.join(map(str, sorted(set(x)))),  # Ensure all agency_ids are strings
# #     'parent_station':'first'
# # }).reset_index()
#
# # Add counts for route_short_name and agency_id
# # grouped['route_short_name_count'] = grouped['route_short_name'].apply(lambda x: len(x.split(', ')))
# # grouped['agency_id_count'] = grouped['agency_id'].apply(lambda x: len(x.split(', ')))
# #
# # # Convert route_short_name and agency_id columns to remove any unwanted characters
# # grouped['route_short_name'] = grouped['route_short_name'].str.replace(r"[\[\]']+", "", regex=True)
# # grouped['agency_id'] = grouped['agency_id'].str.replace(r"[\[\]']+", "", regex=True)
#
# # Save the result to a new CSV file
# output_file = os.path.join(folder, 'stops_routes_agencies_with_counts_and_city_.csv')
# # grouped.to_csv(output_file, index=False, encoding='utf-8')
# result.to_csv(output_file, index=False, encoding='utf-8')
#
# print(f"File saved to: {output_file}")
