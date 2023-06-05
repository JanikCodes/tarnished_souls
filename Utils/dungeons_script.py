import json

# Read the dungeon names from dungeons.txt
with open('dungeons.txt', 'r') as dungeons_file:
    dungeons = dungeons_file.read().splitlines()

# Load the locations from locations.json
with open('locations.json', 'r') as locations_file:
    all_locations = json.load(locations_file)

# Create a dictionary to store the dungeon locations
dungeon_locations = {}

# Iterate over each location
for location in all_locations:
    for dungeon in dungeons:
        if dungeon.lower() in location['name'].lower():
            if dungeon not in dungeon_locations:
                dungeon_locations[dungeon] = []
            dungeon_locations[dungeon].append(location)

# Save the dungeon locations into a new JSON file
output_filename = 'dungeon_locations.json'
with open(output_filename, 'w') as output_file:
    json.dump(dungeon_locations, output_file, indent=4)

print(f"Created {output_filename} containing the dungeon locations.")