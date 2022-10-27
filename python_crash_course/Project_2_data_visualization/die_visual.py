from plotly.graph_objs import Bar, Layout
from plotly.offline import offline

from die import Die

if __name__ == "__main__":
    # Create a D6 dice and a D10.
    die_1 = Die()
    die_2 = Die(10)

    # Make some rolls, and store results in a list
    # IDEA: refactor
    """
        results = []
        for roll_num in range(50_000):
            results.append(die_1.roll() + die_2.roll())"""
    results = [die_1.roll() + die_2.roll() for _ in range(50_000)]

    # IDEA: refactor
    """
        frequencies = []
        for value in range(2, die_1.num_sides + die_2.num_sides + 1):
        # INFO: __list__.count(key) --> occurrences of the given key
            frequencies.append(results.count(value))"""
    frequencies = [results.count(value) for value in range(2, die_1.num_sides + die_2.num_sides + 1)]

    # Visualize the result
    x_values = list(range(2, die_1.num_sides + die_2.num_sides + 1))
    data = [Bar(x=x_values, y=frequencies)]

    x_axis_config = {"title": "Result", "dtick": 1}
    y_axis_config = {"title": "Frequency of Result"}
    my_layout = Layout(title="Results of rolling a D6 and a D10 50000 times",
                       xaxis=x_axis_config,
                       yaxis=y_axis_config)
    offline.plot({"data": data,
                  "layout": my_layout},
                 filename="d6_d10.html")
