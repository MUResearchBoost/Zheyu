import csv
address = 'E:/onedrive/missouricoursework/research/pyspider/MU_faculty/MU_faculty/affiliation.txt'

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