import json

if __name__ == "__main__":
    # Explore the structure of the data
    filename = "data/eq_data_1_day_m1.json"
    with open(filename) as f:
        # INFO: converts data into a format Python can work with: in this case, a giant dictionary
        all_eq_data = json.load(f)

    all_eq_dicts = all_eq_data["features"]

    mags, lons, lats = [], [], []
    for eq_dict in all_eq_dicts:
        mags.append(eq_dict["properties"]["mag"])
        lons.append(eq_dict["geometry"]["coordinates"][0])
        lats.append(eq_dict["geometry"]["coordinates"][1])
    print(mags[:10])
    print(lons[:5])
    print(lats[:5])

    # readable_file = "data/readable_eq_data.json"
    # with open(readable_file, "w") as f:
    #    json.dump(all_eq_data, f, indent=4)
