import json

# Load the JSON data from the file
with open('Data/items.json') as f:
    data = json.load(f)

# Filter the list of items by the ones that have "Smithing Stone" in their name
stone_items = []
for item in data:
    if "Smithing Stone" in item["name"]:
        stone_items.append(item)

stone_items = sorted(stone_items, key=lambda x: x['name'])

# Write the filtered list of items to a new JSON file
with open('stone_items.json', 'w') as f:
    json.dump(stone_items, f, indent=4)

print(f"{len(stone_items)} items written to 'stone_items.json'.")