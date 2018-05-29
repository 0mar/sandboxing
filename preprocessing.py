#!/usr/bin/env python3
import lxml.etree as ET
import pandas as pd
import numpy as np

times_file = 'data/traveltime.xml'
locations_file = 'data/201411281300_MST_NDW01_MT_662.xml'
speed_file = 'data/trafficspeed.xml'


def parse_to_dataframe():
    schema = ".//{http://datex2.eu/schema/2/2_0}"
    traveltimes_tree = ET.parse(times_file)
    locations_tree = ET.parse(locations_file)
    trafficspeeds_tree = ET.parse(speed_file)

    data = {"id": [], "timestamp": [], "duration": []}
    measurements = traveltimes_tree.getroot().findall(schema+"siteMeasurements")
    locations = locations_tree.getroot().findall(schema+"measurementSiteRecord")

    for m in measurements:
        data["id"].append(m.find(schema+"measurementSiteReference").attrib["id"])
        data["timestamp"].append(m.find(schema+"measurementTimeDefault").text)
        data["duration"].append(m.find(schema+"duration").text)

    df = pd.DataFrame.from_dict(data)

    ids = {}
    names = {}
    latitudes = {}
    longitudes = {}
    lengths = {}

    for i in range(len(locations)):
        ids[i] = locations[i].attrib["id"]
        naam = locations[i].find(schema+"measurementSiteName")
        names[i] = naam.find(schema+"value").text
        latitudes[i] = locations[i].find(schema+"latitude").text
        longitudes[i] = locations[i].find(schema+"longitude").text
        if len(locations[i].findall(schema+ "lengthAffected")) > 0:
            lengths[i] = int(locations[i].find("%slengthAffected").text)
        else:
            lengths[i] = 0

    locations = {'id': ids, 'names': names, 'latitude': latitudes, 'longitude': longitudes, 'length': lengths}
    df_loc = pd.DataFrame.from_dict(locations)
    joined = pd.merge(df_loc, df, on='id', how='left')
    return joined


if __name__ == '__main__':
    df = parse_to_dataframe()
