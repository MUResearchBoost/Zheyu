import csv
import re
import os
path = os.path.abspath('.')
address = path + '\\spiders\\data_collected\\engineering_affiliation.txt'

name = list()
affiliation = list()
with open(address, 'r') as f:
    reader = csv.reader(f)
    for rows in reader:
        if len(rows) == 2:
            name.append(rows[0])
            affiliation.append(rows[1])
        elif len(rows) == 1:
            name.append(rows[0])
            affiliation.append('None')
        elif len(rows) > 2:
            name.append(rows[0])
            affiliation.append(rows[1]+rows[2])

print(name)
print(affiliation)

s1 ="///\\\dedeer/efe'''""'''"
s2 = re.sub("[\'\\\\/\"]", "", s1)
print(s1,s2)