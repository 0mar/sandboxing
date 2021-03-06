# sandboxing

*Playing with road network data*

## What it does

Not so much at the moment. It downloads traffic data and processes this into a pandas dataframe.
But who is to say it will not solve traffic jams in a few weeks?

## Running the code

### Requirements
 * Python3
 * pandas
 * numpy
 * Bokeh (only for plotting)

Additionally, for plotting the data on a Google Maps map, request a Google API key [here](https://developers.google.com/maps/documentation/javascript/get-api-key) and put it in `api.py`.

### Instructions

Clone the repository. Before running any of the files, download the data with `python3 download.py`.

## Other sources of information

A master's thesis that uses the same data as a validation for new road network analysis techniques can be downloaded [here](https://dspace.library.uu.nl/bitstream/handle/1874/334224/Thesis%20-%20Johan%20Meppelink%20-%202016-05-17.pdf?sequence=2) (pdf)
