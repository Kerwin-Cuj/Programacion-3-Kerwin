import csv

def load_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = [row[0] for row in reader]
    return data
