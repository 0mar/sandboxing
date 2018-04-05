#!/usr/bin/env python3
import xml.etree.ElementTree as ET
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
    metingen = root.findall(".//{http://datex2.eu/schema/2/2_0}siteMeasurements")

    for i in range(len(metingen)):
        ids[i] = metingen[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteReference")[0].attrib["id"]
        times[i] = metingen[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementTimeDefault")[0].text
        durations[i] = metingen[i].findall(".//{http://datex2.eu/schema/2/2_0}duration")[0].text

    data = {'ID': ids, 'Date_time': times, 'Duration': durations}
    df = pd.DataFrame.from_dict(data)
    df.head()

    locaties = rootLocations.findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteRecord")

    ids = {}
    names = {}
    latitudes = {}
    longitudes = {}
    lenghts = {}

    for i in range(0, len(metingen)):
        ids[i] = locaties[i].attrib["id"]
        naam = locaties[i].findall(".//{http://datex2.eu/schema/2/2_0}measurementSiteName")[0]
        names[i] = naam.findall(".//{http://datex2.eu/schema/2/2_0}value")[0].text
        latitudes[i] = locaties[i].findall(".//{http://datex2.eu/schema/2/2_0}latitude")[0].text
        longitudes[i] = locaties[i].findall(".//{http://datex2.eu/schema/2/2_0}longitude")[0].text
        if len(locaties[i].findall(".//{http://datex2.eu/schema/2/2_0}lengthAffected")) > 0:
            lenghts[i] = locaties[i].findall(".//{http://datex2.eu/schema/2/2_0}lengthAffected")[0].text
        else:
            lenghts[i] = 0

    locations = {'ID': ids, 'Names': names, 'Latitude': latitudes, 'Longitude': longitudes, 'Lenght': lenghts}
    df_loc = pd.DataFrame.from_dict(locations)
    df_loc.head()
    joined = pd.merge(df_loc, df, on='ID', how='inner')
    return joined


if __name__=='__main__':
    df = parse_to_dataframe()