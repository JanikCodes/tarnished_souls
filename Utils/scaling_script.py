import csv
import json
import os

# Get the directory of the mainscript.py file
script_dir = os.path.dirname(os.path.realpath(__file__))

csv_file_path = os.path.join(script_dir, '..', 'Data', 'ERScaling.csv')
json_file_path = os.path.join(script_dir, '..', 'Data', 'weapons.json')

# Load the weapon data from the JSON file
weapon_data = []
with open(json_file_path, 'r') as file:
    weapon_data = json.load(file)

# Load the scaling data from the CSV file
scaling_data = []
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        scaling_data.append(row)

# Function to get the scaling value based on weapon name and attribute
def get_scaling_value(weapon_name, attribute):
    weapon_name = weapon_name.lower()  # Convert weapon name to lowercase

    for row in scaling_data:
        if row['Weapon Name'].lower() == weapon_name:
            if attribute == "Arc":
                return row[" Base Arc Scale"]
            elif attribute == "Fai":
                return row["Base Fth Scale"]
            elif attribute != "-" and attribute != "":
                return row[f"Base {attribute} Scale"]
            else:
                return "0"

    # Handle case when attribute or weapon name is not found
    return "-"

# Iterate over weapon data and update scaling values
for weapon in weapon_data:
    weapon_name = weapon['name']
    for scale in weapon['scalesWith']:
        attribute = scale['name']
        scale['scaling'] = get_scaling_value(weapon_name, attribute)

# Write the updated weapon data to the JSON file
with open(json_file_path, 'w') as file:
    json.dump(weapon_data, file, indent=4)

print("Scaling values updated in weapons.json.")