#!/usr/bin/env python3

import cgi
import pandas as pd
import numpy as np

print("Content-Type: text/html\n")

# Load data
df = pd.read_csv("toronto_weather_1840_to_2025.csv")

# Group by month and calculate required statistics
monthly = df.groupby("month").agg(
    {
        "high_temp": ["mean", "max"],
        "low_temp": ["mean", "min"],
        "precipitation": "mean"
    }
).reset_index()

monthly.columns = ["month", "avg_high", "max_high", "avg_low", "min_low", "avg_precip"]

# Temperature CSS class assignment
css_temps = [
    "temp120", "temp110", "temp100", "temp90", "temp80", "temp70", "temp60",
    "temp50", "temp40", "temp30", "temp20", "temp10", "temp0", "temp-10",
    "temp-20", "temp-30"
]

degree_temps = [
    48.89, 43.33, 37.78, 32.22, 26.67, 21.11, 15.56,
    10.00, 4.45, -1.11, -6.67, -12.22, -17.78, -23.33,
    -28.89, -34.44
]

def temp_class(value):
    for i in range(len(degree_temps)):
        if value >= degree_temps[i]:
            return f'class="{css_temps[i]}"'
    return f'class="{css_temps[-1]}"'

# Begin HTML
print("""
<html>
<head>
<title>Toronto Weather Summary (1840-2025)</title>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  padding: 5px;
  text-align: center;
}
.temp120 { background-color: #990000; color: white; }
.temp110 { background-color: #cc0000; color: white; }
.temp100 { background-color: #ff0000; color: white; }
.temp90  { background-color: #ff3333; color: white; }
.temp80  { background-color: #ff6600; color: black; }
.temp70  { background-color: #ff9900; color: black; }
.temp60  { background-color: #ffcc00; color: black; }
.temp50  { background-color: #ffff66; color: black; }
.temp40  { background-color: #ccff66; color: black; }
.temp30  { background-color: #99ffcc; color: black; }
.temp20  { background-color: #66ccff; color: black; }
.temp10  { background-color: #3399ff; color: white; }
.temp0   { background-color: #0066cc; color: white; }
.temp-10 { background-color: #003399; color: white; }
.temp-20 { background-color: #000066; color: white; }
.temp-30 { background-color: #000033; color: white; }
</style>
</head>
<body>
<h2>Toronto Weather Summary (1840-2025)</h2>
<table>
<tr>
<th>Month</th>
<th>Average High</th>
<th>Average Low</th>
<th>Record High</th>
<th>Record Low</th>
<th>Avg Precipitation</th>
</tr>
""")

# Output table rows
month_order = ['january', 'february', 'march', 'april', 'may', 'june',
               'july', 'august', 'september', 'october', 'november', 'december']

monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
monthly = monthly.sort_values('month')

for index, row in monthly.iterrows():
    print(f"<tr>")
    print(f"<td>{row['month'].capitalize()}</td>")
    print(f"<td {temp_class(row['avg_high'])}>{row['avg_high']:.1f}</td>")
    print(f"<td {temp_class(row['avg_low'])}>{row['avg_low']:.1f}</td>")
    print(f"<td {temp_class(row['max_high'])}>{row['max_high']:.1f}</td>")
    print(f"<td {temp_class(row['min_low'])}>{row['min_low']:.1f}</td>")
    print(f"<td>{row['avg_precip']:.2f}</td>")
    print(f"</tr>")

print("</table>")

# Begin Record Listings
print(f"<h3>Record Entries (1840-2025)</h3>")

for month in month_order:
    # Record High
    max_high = df[df['month'] == month]['high_temp'].max()
    high_rows = df[(df['month'] == month) & (df['high_temp'] == max_high)]

    for _, row in high_rows.iterrows():
        print(f"<p><strong>Highest Temperature in {month.capitalize()}:</strong></p>")
        print("<table>")
        print("<tr>" + "".join([f"<th>{col}</th>" for col in row.index]) + "</tr>")
        print("<tr>")
        for col in row.index:
            val = row[col]
            if col == "high_temp" or col == "low_temp":
                print(f"<td {temp_class(val)}>{val:.1f}</td>")
            elif isinstance(val, float):
                print(f"<td>{val:.2f}</td>")
            else:
                print(f"<td>{val}</td>")
        print("</tr></table><br>")

    # Record Low
    min_low = df[df['month'] == month]['low_temp'].min()
    low_rows = df[(df['month'] == month) & (df['low_temp'] == min_low)]

    for _, row in low_rows.iterrows():
        print(f"<p><strong>Lowest Temperature in {month.capitalize()}:</strong></p>")
        print("<table>")
        print("<tr>" + "".join([f"<th>{col}</th>" for col in row.index]) + "</tr>")
        print("<tr>")
        for col in row.index:
            val = row[col]
            if col == "high_temp" or col == "low_temp":
                print(f"<td {temp_class(val)}>{val:.1f}</td>")
            elif isinstance(val, float):
                print(f"<td>{val:.2f}</td>")
            else:
                print(f"<td>{val}</td>")
        print("</tr></table><br>")

# End HTML
print("""
</body>
</html>
""")
