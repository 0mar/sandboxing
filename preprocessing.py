#!/usr/bin/env python3
import lxml.etree as ET
import pandas as pd
import numpy as np

times_file = 'data/traveltime.xml'
locations_file = 'data/201411281300_MST_NDW01_MT_662.xml'


def parse_to_dataframe():
    treeTimes = ET.parse(times_file)
    treeLocations = ET.parse(locations_file)
    root = treeTimes.getroot()
    rootLocations = treeLocations.getroot()

    ids = {}
    times = {}
    durations = {}
    measurements = root.findall(".//{http://datex2.eu/schema/2/2_0}siteMeasurements")

    for i in range(len(measurements)):
        ids[i] = measurements[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteReference")[0].attrib["id"]
        times[i] = measurements[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementTimeDefault")[0].text
        durations[i] = measurements[i].findall(".//{http://datex2.eu/schema/2/2_0}duration")[0].text

    data = {'id': ids, 'timestamp': times, 'duration': durations}
    df = pd.DataFrame.from_dict(data)
    df.head()

    locations = rootLocations.findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteRecord")

    ids = {}
    names = {}
    latitudes = {}
    longitudes = {}
    lengths = {}

    for i in range(0, len(measurements)):
        ids[i] = locations[i].attrib["id"]
        naam = locations[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteName")[0]
        names[i] = naam.findall(".//{http://datex2.eu/schema/2/2_0}value")[0].text
        latitudes[i] = locations[i].findall(".//{http://datex2.eu/schema/2/2_0}latitude")[0].text
        longitudes[i] = locations[i].findall(".//{http://datex2.eu/schema/2/2_0}longitude")[0].text
        if len(locations[i].findall(".//{http://datex2.eu/schema/2/2_0}lengthAffected")) > 0:
            lengths[i] = int(locations[i].findall(".//{http://datex2.eu/schema/2/2_0}lengthAffected")[0].text)
        else:
            lengths[i] = 0

    locations = {'id': ids, 'names': names, 'latitude': latitudes, 'longitude': longitudes, 'length': lengths}
    df_loc = pd.DataFrame.from_dict(locations)
    df_loc.head()
    joined = pd.merge(df_loc, df, on='id', how='left')
    return joined


if __name__ == '__main__':
    df = parse_to_dataframe()
