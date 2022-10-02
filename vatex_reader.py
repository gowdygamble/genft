import json
import csv

fn = 'vatex_validation_v1.0.json'

with open(fn) as f:
    data = json.load(f)


column_titles = ['a', 'b', 'c', 'd']

row_collect = []

for i in range(3):
    id = data[i]['videoID'][:11]
    time_start = data[i]['videoID'][-13:-7]
    time_end = data[i]['videoID'][-6:]
    label = data[i]['videoID']

    row_collect.append([id, time_start, time_end, label])

with open('val.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(column_titles)
    write.writerows(row_collect)
