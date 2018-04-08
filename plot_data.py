#!/usr/bin/env python3
from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    DataRange1d, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper
# from bokeh.palettes import Viridis5
import pandas as pd
from preprocessing import parse_to_dataframe
try:
    from api import API_KEY
except ImportError:
    raise FileNotFoundError("No API key found. Create one at https://developers.google.com/maps/documentation/javascript/get-api-key and save the line `API_KEY='your key'` in api.py")
    
df = parse_to_dataframe()

map_options = GMapOptions(lat=52.0687206, lng=4.9863232, map_type="roadmap", zoom=7)
plot = GMapPlot(x_range=Range1d(),y_range=Range1d(),map_options=map_options)
plot.title.text = "Test plot"
plot.api_key = API_KEY

source=ColumnDataSource(data=dict(lat=df.latitude.tolist(),lon=df.longitude.tolist(),size=df.length.values/1000))
circle=Circle(x="lon",y="lat",size="size")
plot.add_glyph(source,circle)
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
show(plot)

