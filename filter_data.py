import pandas as pd
import requests
import numpy as np
import json

try:
    from api import API_KEY
except ImportError:
    raise FileNotFoundError(
        "No API key found. Create one at https://developers.google.com/maps/documentation/javascript/get-api-key "
        "and save the line `API_KEY='your key'` in api.py")


def filter_df_on_locations(df, location1, location2):
    coords_1 = get_coords_at(location1)
    coords_2 = get_coords_at(location2)
    coords = np.array([coords_1, coords_2])
    bbox = np.vstack([np.min(coords, axis=0), np.max(coords, axis=0)])

    return df[
        (pd.to_numeric(df["latitude"]) > bbox[0][0]) & (pd.to_numeric(df["longitude"]) > bbox[0][1]) &
        (pd.to_numeric(df["latitude"]) < bbox[1][0]) & (pd.to_numeric(df["longitude"]) < bbox[1][1])]


def get_coords_at(name):
    query = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (name, API_KEY)
    f = requests.get(query)
    geocode = json.loads(f.text)
    if not geocode["status"] == "OK":
        raise ConnectionError("Errors in retrieving latitude and longitude from Google Maps")
    coords = list()
    coords.append(geocode["results"][0]["geometry"]["location"]["lat"])
    coords.append(geocode["results"][0]["geometry"]["location"]["lng"])
    return coords
