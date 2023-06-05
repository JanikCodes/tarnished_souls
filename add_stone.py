import json


with open('stone_items.json') as f:
    data = json.load(f)

for item in data:
    if item["name"].startswith("Smithing"):
        name = item["name"]
        url = item["image"]
        sql = f"insert into item values(null, '{name}', 250, 300, 'smithing_stone', 'smithing_stone', 0,0,0,0,0,0,0,0,1,0,'{url}',0,0,0,0,0,0,0,0);"
        with open('Data/sql-statements.txt', 'a') as f:
            f.write(f"{sql}\n")

for item in data:
    if item["name"].startswith("Somber Smithing"):
        name = item["name"]
        url = item["image"]
        sql = f"insert into item values(null, '{name}', 250, 300, 'somber_smithing_stone', 'smithing_stone', 0,0,0,0,0,0,0,0,1,0,'{url}',0,0,0,0,0,0,0,0);"
        with open('Data/sql-statements.txt', 'a') as f:
            f.write(f"{sql}\n")