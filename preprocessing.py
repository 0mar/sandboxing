#!/usr/bin/env python3
import lxml.etree as ET
import pandas as pd
import numpy as np

times_file = "data/traveltime.xml"
locations_file = "data/measuring_locations.xml"
speed_file = "data/trafficspeed.xml"
prefix = ".//{http://datex2.eu/schema/2/2_0}"


def parse_travel_times():
    """
    Parses the travel times from the indicated XML file

    :return: DataFrame with IDs and measurements
    """
    tree = ET.parse(times_file)
    data = {"id": [], "timestamp": [], "duration": []}
    entries = tree.getroot().findall(prefix + "siteMeasurements")
    for entry in entries:
        data["id"].append(entry.find(prefix + "measurementSiteReference").attrib["id"])
        data["timestamp"].append(entry.find(prefix + "measurementTimeDefault").text)
        data["duration"].append(entry.find(prefix + "duration").text)
    df = pd.DataFrame.from_dict(data)
    return df


def parse_measuring_locations():
    """
    Parses measuring locations from the indicated XML file

    :return: DataFrame with IDs and locations.
    """
    tree = ET.parse(locations_file)
    data = {"id": [], "names": [], "latitude": [], "longitude": [], "length": []}
    entries = tree.getroot().findall(prefix + "measurementSiteRecord")
    for entry in entries:
        data["id"].append(entry.attrib["id"])
        name = entry.find(prefix + "measurementSiteName")
        data["names"].append(name.find(prefix + "value").text)
        data["latitude"].append(entry.find(prefix + "latitude").text)
        data["longitude"].append(entry.find(prefix + "longitude").text)
        length_element = entry.find(prefix + "lengthAffected")
        if length_element is not None:
            data["length"].append(int(float(length_element.text)))
        else:
            data["length"].append(0)

    df = pd.DataFrame.from_dict(data)
    return df


def parse_traffic_speeds():
    """
    Parses traffic speeds from the indicated XML file.
    Averages the measured speeds and stores them.
    The number of lanes(?) varies for every measuring point.
    To obtain the number of cars, we do the following:
    First we find the total number of measurements, then we take every 4 car count and sum those up.
    To obtain the average speed, we take every 4th speed record and compute a weighted average.
    We could also get the standard deviation, should we be so inclined.
    Don't think we are, though.

    :return: DataFrame with IDs, counting results and speeds
    """
    tree = ET.parse(speed_file)
    data = {"id": [], "amount": [], "speed": []}
    entries = tree.getroot().findall(prefix + "siteMeasurements")
    for entry in entries:
        data["id"].append(entry.find(prefix + "measurementSiteReference").attrib['id'])
        measurements = entry.findall(prefix + 'averageVehicleSpeed')
        assert len(measurements) % 4 == 0  # Checking if this is always true
        if len(measurements)==0:
            print("No measurements found")
        counts = np.zeros(len(measurements) // 4, dtype=int)
        speeds = np.zeros(len(measurements) // 4)
        for lane in range(len(measurements) // 4):
            index = lane * 4 + 3
            speeds[lane] += int(measurements[index].find(prefix + 'speed').text)
            counts[lane] += np.maximum(int(measurements[index].attrib["numberOfInputValuesUsed"]), 0)
        data["amount"].append(np.average(counts))
        print("Counts", np.average(counts))

        if sum(counts) > 0:
            data["speed"].append(np.average(speeds, weights=counts))
            print("Speed", np.average(speeds, weights=counts))
        else:
            data["speed"].append(0)

        print("from data", speeds, counts)
    df = pd.DataFrame.from_dict(entries)
    return df


def parse_to_dataframe():
    """
    Parses three files and combines them to a data frame.

    :return: Data frame containing traffic information per ID
    """
    locations = parse_measuring_locations()
    traveltimes = parse_travel_times()
    # trafficspeeds = parse_traffic_speeds()
    df = pd.merge(locations, traveltimes, on="id", how="left")
    # df = pd.merge(df, trafficspeeds, on="id", how="left")
    return df


if __name__ == "__main__":
    demo_df = parse_to_dataframe()
    print(demo_df)
