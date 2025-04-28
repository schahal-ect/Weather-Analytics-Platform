# Historical Weather Analytics Platform

This Python-based project processes 67,000+ historical weather records (1840–2025) and generates dynamic HTML-based statistical reports hosted on a Raspberry Pi NGINX server.

## Features
- Parses historical weather data year-by-year.
- Calculates monthly high/low temperatures and precipitation summaries.
- Displays results using CGI-generated HTML tables.
- Color-coded KPI dashboard with real-time weather statistics.

## Technologies Used
- Python 3
- Pandas
- NumPy
- HTML/CSS
- NGINX (Raspberry Pi server hosting)

## Setup Instructions
1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the CSV creation script:
   ```bash
   python create_all_csv_files.py
   ```

3. Deploy the CGI script:
   - Place `display_weatherstats.py` inside `/usr/lib/cgi-bin/` on Raspberry Pi.
   - Ensure the script is executable.

4. Access the dashboard by visiting:
   ```
   http://<your-raspberrypi-ip>:8080/cgi-bin/display_weatherstats.py
   ```

## Author
Saket Chahal
