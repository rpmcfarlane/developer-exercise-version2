import csv
import pynn.nearest_neighbor_index as nni

# Example use: finding the nearest hospital or urgent care facility to an incident. 
# Input: a file including the list of hospital coordinates and the incident's coordinates
# Example points from:
#       https://data-fairfaxcountygis.opendata.arcgis.com/datasets/Fairfaxcountygis::hospitals-and-urgent-care-facilities/explore

input_points = []
# FILE_NAME should be the name of a csv file where 
# the first two values in a row are the x and y coordinates of hospitals
FILE_NAME = 'examples/Hospitals_and_Urgent_Care_Facilities.csv'
# QUERY_POINTS should be the list of GPS coordinates of incidents that you want to find the nearest
# hospital to
QUERY_POINTS = [(0, 0), (11800000, 7000000), (12000000, 7500000)]
with open(FILE_NAME, 'r') as file:
    reader = csv.reader(file)
    # skip the header
    next(reader)
    # add the x and y for each hospital
    for row in reader:
        input_points.append((float(row[0]), float(row[1])))

# Index the coordinates of the hospitals to speed up the searches based on the queries
nearest_neighbor_index = nni.NearestNeighborIndex(input_points)

for query in QUERY_POINTS:
    # Use the indexed NearestNeighborIndex to find the nearest hospital
    print(f'The nearest hospital or urgent care to {query} is located at {nearest_neighbor_index.find_nearest(query)}')
