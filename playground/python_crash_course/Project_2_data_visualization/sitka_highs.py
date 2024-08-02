import csv
from datetime import datetime

import matplotlib.pyplot as plt

if __name__ == "__main__":
    filename = "data/sitka_weather_2018_simple.csv"
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        # for index, column_header in enumerate(header_row):
        #    print(index, column_header)
        # Get dates and high temperatures from this file.
        dates, highs, lows = [], [], []
        for row in reader:
            highs.append(int(row[5]))
            lows.append(int(row[6]))
            dates.append(datetime.strptime(row[2], "%Y-%m-%d"))

    # Plot the high and low temperatures
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    # INFO: alpha --> transparent
    ax.plot(dates, highs, c="red", alpha=0.5)
    ax.plot(dates, lows, c="blue", alpha=0.5)
    # INFO: fill shading area between two y_values --> fill_between(x_values, y_values1, y_values2, ...)
    ax.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)
    # Format plot
    ax.set_title("Daily high and low temperatures - 2018", fontsize=24)
    ax.set_xlabel("", fontsize=16)
    fig.autofmt_xdate() # INFO: draws the data labels diagonally to prevent them from overlapping
    ax.set_ylabel("Temperature (F)", fontsize=16)
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.show()
