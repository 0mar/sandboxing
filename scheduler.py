#!/usr/bin/env python3

import sched
import time
from datetime import datetime
import sys
import os

import pandas as pd
from preprocessing import parse_to_dataframe
from filter_data import filter_df_on_locations
from download_data import download_all

def debug(*args):
    if False: # Set to True to see auxiliary information
        print(args)

def parse_data(file_name):
    # todo: check timestamp of data/file
    # Todo: convert to pickle
    print("Getting data at %s" % datetime.now().strftime("%d-%m-%y %H:%M"))
    download_all()
    debug("Parsing data to dataframe")
    full_df = parse_to_dataframe()
    debug("Retrieved %d entries" % len(full_df))
    df = filter_df_on_locations(full_df, "Tilburg", "Eindhoven")
    debug("Filtered to %d entries" % len(df))
    debug("Appending data to dataframe")
    old_df = pd.read_csv(file_name)
    new_df = pd.concat([old_df, df])
    debug("New dataframe size: %s\n" % new_df.shape)
    new_df.to_csv(file_name, sep='|')


def collect_data(minutes, file_id):
    """
    Collect data for `time` minutes and store in a large dataframe

    :param minutes: Number of minutes the downloader should run for.
    :param file_id: Name of the file all the data will be stored in.
    :return: None
    """
    file_name = file_id + ".csv"
    print("Storing dataframe in '%s'" % file_name)
    if os.path.exists(file_name):
        print("*Warning*: Overwriting %s" % file_name)
    with open(file_name, 'w'):
        pd.DataFrame().to_csv(file_name, sep='|')  # Just for clearing the file
    print("Starting downloader at %s, scheduled for %d minutes" % (datetime.now().strftime("%d-%m-%y %H:%M"), minutes))
    scheduler = sched.scheduler(time.time, time.sleep)
    for minute in range(minutes):
        scheduler.enter(60 * minute, 1, parse_data, (file_name,))
    scheduler.run()


if __name__ == "__main__":
    try:
        duration = int(sys.argv[1])
    except (ValueError, IndexError):
        duration = 60
    try:
        name = sys.argv[2]
    except IndexError:
        name = "data/dataset - %s (%d minutes)" % (datetime.now().strftime("%d-%m %H%M"), duration)
    collect_data(duration, name)
