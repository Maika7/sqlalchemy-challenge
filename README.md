# sqlalchemy-challenge

Climate Analysis and API
Project Overview
This project focuses on conducting a climate analysis of weather data for Honolulu, Hawaii, using Python, SQLAlchemy, and Flask. It involves exploring precipitation data, analyzing temperature observations, and providing insights into weather patterns using a Flask API. The dataset used is stored in a SQLite database named hawaii.sqlite.

Technologies Used
Python 3.9+
Pandas
Matplotlib
SQLAlchemy
Flask
Setup Instructions
1. Cloning the Repository
bash
Copy code
git clone https://github.com/Maika7/sqlalchemy-challenge.git
cd sqlalchemy-challenge
2. Create a Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv env
source env/bin/activate  # For macOS/Linux
env\Scripts\activate  # For Windows
3. Install Required Packages
bash
Copy code
pip install -r requirements.txt
4. Database Setup
Ensure that the hawaii.sqlite file is placed in the Resources folder within the project directory. This file contains the measurement and station data used for analysis.

Analysis Overview
Precipitation Analysis
Find the Most Recent Date: Extracted from the measurement table.
Retrieve Last 12 Months of Data: A DataFrame is created containing date and precipitation values.
Visualization: Precipitation data is plotted to show rainfall patterns over the last year.
Summary Statistics: Displayed using Pandas to provide insights into precipitation variations.
Station Analysis
Station Count: Query to find the total number of weather stations.
Most Active Station: Identifies the station with the highest number of observations.
Temperature Data Analysis: Retrieves minimum, maximum, and average temperatures from the most active station.
Temperature Observations Histogram: Plots the temperature data as a histogram.
Flask API Overview
The project also includes a Flask API to access the analyzed climate data via various routes.

API Endpoints
/: Lists all available routes.
/api/v1.0/precipitation: Returns the last 12 months of precipitation data as JSON.
/api/v1.0/stations: Returns a JSON list of all weather stations.
/api/v1.0/tobs: Returns temperature observations for the most active station for the last year.
/api/v1.0/<start>: Returns the minimum, average, and maximum temperatures from the specified start date to the most recent date.
/api/v1.0/<start>/<end>: Returns temperature statistics for a given date range.

Example Output
Precipitation Route Example: /api/v1.0/precipitation

json
Copy code
{
    "2017-01-01": 0.03,
    "2017-01-02": 0.0,
    "2017-01-03": 0.0,
    ...
}
Stations Route Example: /api/v1.0/stations

json
Copy code
[
    "USC00519397",
    "USC00519281",
    "USC00516128",
    ...
]
Usage
Run the Flask App:

bash
Copy code
python app.py
Access the API: Open a browser and navigate to http://127.0.0.1:5000/ to view the available routes.

Explore Routes:

Example: http://127.0.0.1:5000/api/v1.0/precipitation to view the precipitation data.
Contributions & Acknowledgments
This project was completed as part of a data science and analytics course. It uses open-source libraries and data provided for educational purposes. Contributions to improve or expand the analysis are welcome.
