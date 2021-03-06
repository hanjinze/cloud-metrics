#!/usr/local/bin/python2.7
# -*- coding: UTF-8 -*-

# metrics.cgi (python)
# --------------------
#
# Display google motion chart based on csv data files
# 
# Example of csv file
# -------------------
# filename: user.data.of.eucalyptus.in.india.20110101-20121231.csv
# content:
# name, count, sum, min, avg
# steenoven, 2, 398426.0, 198126.0, 199213.0
# ...
#
# Input (GET/POST)
# ----------------
# metrics
# s_date
# e_date
# title

from datetime import date, timedelta, datetime

print "Content-Type: text/html;charset=utf-8"

# HTTP GET/POST
import cgi
form = cgi.FieldStorage() # instantiate only once!
metrics = form.getlist('metrics')
metrics = metrics[0]

s_date = form.getlist('s_date')
s_date = datetime.strptime(s_date[0], '%Y%m%d')
e_date = form.getlist('e_date')
e_date = datetime.strptime(e_date[0], '%Y%m%d')
xaxis = form.getlist('xaxis')
xaxis = xaxis[0]
yaxis = form.getlist('yaxis')
yaxis = yaxis[0]
gtype = form.getlist('type')
gtype = gtype[0]
title = form.getlist('title')
title = title[0]

#Variables
gchart_pname = "motionchart"
gchart_cname = "google.visualization.MotionChart"
gchart_options = """ {};
        options['state'] =
	'{\"xZoomedDataMin\":0,\"yAxisOption\":\"2\",\"yZoomedDataMin\":0,\"time\":\"$syear-$smonth-$sday\",\"yLambda\":1,\"iconType\":\"VBAR\",\"nonSelectedAlpha\":0.4,\"xZoomedIn\":false,\"showTrails\":false,\"dimensions\":{\"iconDimensions\":[\"dim0\"]},\"yZoomedIn\":false,\"xZoomedDataMax\":19,\"iconKeySettings\":[],\"xLambda\":1,\"colorOption\":\"2\",\"playDuration\":15000,\"xAxisOption\":\"2\",\"sizeOption\":\"_UNISIZE\",\"orderedByY\":false,\"uniColorForNonSelected\":false,\"duration\":{\"timeUnit\":\"D\",\"multiplier\":1},\"yZoomedDataMax\":139,\"orderedByX\":true};';
	options['width'] = 650;
	options['height'] = 480"""
delimiter = ","
data_dir = "../data4graphs/"
file_extension = ".csv"
cnt = 0

# COLUMNS of REPORT
column_names = ['ownerid', 'instances'] # When we draw graphs/charts we need to show value names. The first line of csv file has column names but we adjust the names here. This would be removed once we have good column names in csv file.
column_name0 = column_names[0]
column_name1 = column_names[1]

#for (c_date = datetime.strptime(s_date, '%Y%m%d'), i = 0; c_date <= e_date; c_date = c_date + timedelta(1)), i++):
filename = data_dir + metrics + "." + s_date.strftime("%Y%m%d") + "-" + e_date.strftime("%Y%m%d") + file_extension
import os.path
import sys

if os.path.isfile(filename) != True:
	print
	print filename
	sys.exit(1)
f = open(filename, 'r')
lines = f.readlines()
if lines is None:
	print
	print lines
	sys.exit(2)

csv_lines = []
# When multiple files, we skip first line of the files which is a comlumn definition.
for line in lines:
	csv_lines.append(line.rstrip().split(delimiter))

# Make tables for the report
i = 0
rows = []
row_size = 0
for csv_line in csv_lines:
	if i == 0:
		i = i + 1
		continue
	rows.append([csv_line[0],'new Date(' + s_date.strftime("%Y") + ',' + s_date.strftime("%m") + ')', csv_line[1]]) # csv_line[0] = ownerId, csv_line[1] = instances
	row_size = row_size + 1


column_size = 3

# HTML
#print metrics
#print lines
#print csv_lines
output = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>%(title)s</title>
      <script type="text/javascript" src="http://www.google.com/jsapi"></script>
      <script type="text/javascript">
      google.load('visualization', '1', {packages: ['%(gchart_pname)s']});
      function drawVisualization() {
		      var data = new google.visualization.DataTable();
		      data.addColumn('string', '%(column_name0)s');
		      data.addColumn('date', 'Date');
			      data.addColumn('number', '%(column_name1)s');
		      data.addRows(["""

i = 0
output_add = ""
for row_line in rows:
	if i > 0:
		output_add = output_add + ",\n"
		
	#output_add = output_add + "['" + ('\', \'' . join(map(str, row_line))) + "']"
	output_add = output_add + "['" + row_line[0] + "', " + row_line[1] + ", " + row_line[2] +  "]"
	i = i + 1
output_add = output_add + "]);"

output = output + output_add

output_add = """
		      var options = %(gchart_options)s;
		      var annotatedtimeline = new %(gchart_cname)s(
			      document.getElementById('visualization'));
		      annotatedtimeline.draw(data, options);
		      }

      google.setOnLoadCallback(drawVisualization);
      </script>
      </head>
      <body style="font-family: Arial;border: 0 none;">
      <div id="visualization" style="width: 650px; height: 400px;"></div>
      </body>
      </html>
""" 
output = output + output_add

output = output % vars()

print output
