import csv

if __name__ == "__main__":
    filename = "data/sitka_weather_07-2018_simple.csv"
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        print(header_row)