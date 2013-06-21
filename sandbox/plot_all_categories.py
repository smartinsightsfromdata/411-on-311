# This script plots the number of 311 request on a temporal scale,
# aggregated by month and day of the week.

import json
import matplotlib.pyplot as plt
from itertools import groupby
import datetime
import numpy as np
import sys

db_name = sys.argv[1]
# Useful lists
month_names = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL',
  'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
dayofweeks_names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

# Open the json data file
data_file = '311-' + db_name + '.json'
f =  open('../data/'+data_file, 'r')

# Read in the json database (returns a dictionary)
req_data = json.load(f)
f.close()

# Retrieve the year-month-day as a string
dates_s = [e[8] for e in req_data['data'][:-1] if int(e[8][0:4]) > 2010]

# Aggregate data by month
# Convert year-month to integers and reverse the order (lower to higher)
dates_i = [int(e[0:4]+e[5:7]) for e in dates_s][::-1]

# Count the number of reports per month
counts = [(k, len(list(g))) for (k, g) in groupby(dates_i)]

# Plot the counts
plt.figure()
# Create the shading rectangles for readabiliy
for i in range(1, len(counts), 2):
  plt.axvspan(i-0.5, i+0.5, color='#DDDDDD', alpha=0.7)
plt.plot([e[1] for e in counts], 'o-', linewidth=2, color='#3399CC')
# Lambda function that returns "motnh labels" (the year is attached if
# the month is January
m_label = lambda ym: str(ym/100) + ' ' + month_names[ym%100-1] \
  if ym%100 == 1 else month_names[ym%100-1]
month_labels = [m_label(e[0]) for e in counts] 
plt.xticks(range(len(counts)), month_labels, rotation='vertical')
plt.xlim(-0.5, len(counts)-0.5)

# Aggregate data by weekday
weekdays_i = [datetime.date(int(e[0:4]),int(e[5:7]),int(e[8:10])).weekday()
  for e in dates_s]

# Plot 
plt.figure()
plt.hist(weekdays_i, range(8), rwidth=0.7, color='#3399CC')
plt.xticks(np.array(range(8))+0.5, dayofweeks_names)
plt.show()
