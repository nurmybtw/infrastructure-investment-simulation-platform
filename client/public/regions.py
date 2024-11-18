import json
import os

with open('kz.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

regions = []

for region in data['features']:
    regions.append(region['properties'])

# path = os.path('regions.json')
with open('regions.json', 'w', encoding='utf-8') as f:
    json.dump(regions, f)