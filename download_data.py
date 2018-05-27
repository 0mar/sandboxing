#!/usr/bin/env python3
"""
This script downloads the latest travel times and if not present, the measuring data from NDW and unpacks these files in the 'data' folder.
"""
import urllib.request
import gzip
import zipfile
import shutil
import os

travel_time_url = "http://opendata.ndw.nu/traveltime.xml.gz"
measuring_locations_url = "http://www.ndw.nu/downloaddocument/4ceb5142ed9e79bad0db5382736c474a/MST.zip"

travel_time_file = "data/traveltime.xml"
measuring_locations_file = "data/measuring_locations.xml"


def download(url, file_name, overwrite):
    """
    Downloads gzipped files from the internet and unpacks them.

    :param url: URL to the file
    :param file_name: the name the downloaded file gets
    :param overwrite: True if file should be overwritten, False otherwise
    :return: None
    """
    ext = ".comp"
    os.makedirs("data", exist_ok=True)
    if os.path.exists(file_name):
        if overwrite:
            print("Overwriting %s" % file_name)
        else:
            print("%s exists, not overwriting" % file_name)
            return
        print("Downloading from %s" % url)
        urllib.request.urlretrieve(url, file_name + ext)
        print("Unpacking in %s" % file_name)
        if url.endswith('.zip'):
            zip_ref = zipfile.ZipFile(file_name + ext, 'r')
            zip_ref.extractall('data')
            zip_ref.close()
        elif url.endswith('.gz'):
            with gzip.open(file_name + ext, "rb") as f_in:
                with open(file_name, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        os.remove(file_name + ext)


if __name__ == "__main__":
    download(travel_time_url, travel_time_file, overwrite=True)
    download(measuring_locations_url, measuring_locations_file, overwrite=False)
