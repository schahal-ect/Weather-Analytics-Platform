import pandas as pd
import numpy as np
import re

def parse_weather_by_year(year):
    file_path = f"weather_data/toronto_weather_{year}.html"
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = re.findall(
        r"/cities/toronto/day/.*?</a></div></td>\s*"
        r"<td class='text-right.*?'>(.*?)</td>\s*"
        r"<td class='text-right.*?'>(.*?)</td>\s*"
        r"<td class='text-right.*?'>(.*?)</td>",
        content,
        re.S | re.M
    )

    date_range = pd.date_range(start=f"{year}-01-01", periods=len(pattern))
    months = date_range.month_name().str.lower()
    days_of_month = date_range.day
    day_of_year = np.arange(1, len(pattern)+1)

    records = []

    for i, match in enumerate(pattern):
        try:
            high = float(match[0])
        except:
            high = np.nan
        try:
            low = float(match[1])
        except:
            low = np.nan
        try:
            precip = float(match[2])
        except:
            precip = 0.0

        records.append([
            "Toronto",
            day_of_year[i],
            months[i],
            days_of_month[i],
            year,
            high,
            low,
            precip
        ])

    df = pd.DataFrame(records, columns=[
        "city", "day_of_year", "month", "day_of_month", "year",
        "high_temp", "low_temp", "precipitation"
    ])

    return df

import pandas as pd
import numpy as np

def create_all_csv_files(start_year, end_year):
    all_data = []

    for year in range(start_year, end_year + 1):
        try:
            print(f"Parsing data for year {year}...")
            df = parse_weather_by_year(year)
            df.to_csv(f"toronto_weather_{year}.csv", index=False)
            all_data.append(df)
        except Exception as e:
            print(f"Error parsing year {year}: {e}")

    full_df = pd.concat(all_data, ignore_index=True)
    full_df.to_csv("toronto_weather_1840_to_2025.csv", index=False)
    return full_df

# Execution from command-line
if __name__ == "__main__":
    df = create_all_csv_files(1840, 2025)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print(df)
    print(df.info())
    print(df.shape)
    print(df.describe())
