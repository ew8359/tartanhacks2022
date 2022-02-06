import csv

with open('nasdaq_screener_1644045855526.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    S = set()
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[0].isalpha():
                S.add(row[0])
            line_count += 1