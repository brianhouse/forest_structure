#!/usr/bin/env python3

import csv, json
from housepy import util, strings

# parse the csv
data = []
with open("Niwot_Plot_Data2012yr2.csv") as f:
    rows = csv.reader(f)
    for r, row in enumerate(rows):
        if r == 0:
            labels = row
            continue
        if len("".join(row)) == 0:
            continue
        data.append({labels[i]: item for (i, item) in enumerate(row[:len(labels)])})
# print(json.dumps(data, indent=4))

# keep these fields / purge missing data
fields = ['Latitude', 'Longitude', 'Elevation', 'Line', 'Distance_(m)', '2012_DBH_(cm^2)', 'Family', 'Genus', 'Species']
def check(s):   # did this to get all DBHs, but now just grabbing the one
    for field in fields:
        if field in s:
            return True
    return False
for d, datum in enumerate(data):
    data[d] = {strings.slugify(key): strings.as_numeric(value) for (key, value) in datum.items() if check(key) and len(value.strip())}
    if len(data[d]) < len(fields) or 'distance_m' not in data[d]:
        data[d] = None
    else:
        data[d]['size'] = (data[d]['2012_dbh_cm2'] / 2) * 0.01 # radius in meters
        data[d]['distance'] = data[d]['distance_m']
        del data[d]['2012_dbh_cm2']
        del data[d]['distance_m']
data = [datum for datum in data if datum is not None]


# organize by gentraso / transect (line)
gentraso = {}
for datum in data:
    t = datum['line']
    del datum['line']
    if t not in gentraso:
        gentraso[t] = []
    gentraso[t].append(datum)
for transect, data in gentraso.items():
    data.sort(key=lambda d: d['distance'])


print(json.dumps(gentraso, indent=4))

util.save("niwot.data", gentraso)

