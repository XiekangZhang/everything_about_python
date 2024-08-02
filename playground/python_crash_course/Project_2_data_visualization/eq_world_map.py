import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

if __name__ == "__main__":
    filename = "data/eq_data_30_day_m1.json"
    with open(filename) as f:
        # INFO: converts data into a format Python can work with: in this case, a giant dictionary
        all_eq_data = json.load(f)

    all_eq_dicts = all_eq_data["features"]

    mags, lons, lats, hover_texts = [], [], [], []
    for eq_dict in all_eq_dicts:
        mags.append(eq_dict["properties"]["mag"])
        lons.append(eq_dict["geometry"]["coordinates"][0])
        lats.append(eq_dict["geometry"]["coordinates"][1])
        hover_texts.append(eq_dict["properties"]["title"])

    # Map the earthquakes.
    # data = [Scattergeo(lon=lons, lat=lats)]
    data = [{
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_texts,
        "marker": {
            "size": [5 * mag for mag in mags],
            "color": mags,
            "colorscale": "viridis",
            "reversescale": True,
            "colorbar": {"title": "Magnitude"}
        }
    }]
    my_layout = Layout(title="Global Earthquakes")

    fig = {"data": data, "layout": my_layout}
    offline.plot(fig, filename="global_earthquakes.html")
