import csv

def generate_csv(filename, values):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for v in values:
            writer.writerow([v])

# data1.csv: números
generate_csv("data1.csv", list(range(1, 151)))

# data2.csv: códigos alfanuméricos
generate_csv("data2.csv", [f"A{str(i).zfill(3)}" for i in range(1, 151)])

# data3.csv: usuarios
generate_csv("data3.csv", [f"user{str(i).zfill(3)}" for i in range(1, 151)])
