import matplotlib.pyplot as plt

if __name__ == "__main__":
    x_values = range(1, 1001)
    y_values = [x ** 2 for x in x_values]

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    # INFO: s stands for size of the dot
    # INFO: c represents color
    # INFO: cmap for color map --> gradiant color
    # ax.scatter(x_values, y_values, s=10, c=(0, 0.8, 0))
    ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)

    # Set chart title and label axes
    ax.set_title("Square Numbers", fontsize=24)
    ax.set_xlabel("Value", fontsize=14)
    ax.set_ylabel("Square of Value", fontsize=14)

    # Set size of tick labels
    ax.tick_params(axis="both", which="major", labelsize=14)

    # Set the range for each axis
    ax.axis([0, 1100, 0, 1100000])
    plt.show() # or plt.savefig("squares_plot.png", bbox_inches='tight') --> bbox_inches: trims extra whitespace
