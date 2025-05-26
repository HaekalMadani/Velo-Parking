# Velo-Parking
Velo-Parking is a Django-based web application that helps cyclists in France check the availability of bicycle parking spaces and forecast future usage trends. Whether you're commuting daily or planning a ride, Velo-Parking makes it easier to find a spot—now and in the future.

# Features
- Real-Time Availability – Check which bike parking areas are currently free

- Forecasting with ARIMA – Predict parking availability for upcoming weeks/months

- Location-Based Insights – View data specific to different parking locations across France

- Interactive Dashboard – Visualize historical trends and forecasted data

# Forecasting Model
Uses the ARIMA (AutoRegressive Integrated Moving Average) model

Trained on a dataset of public bicycle parking lots in France

Forecasts are generated monthly to help users plan ahead

# Tech Stack
Backend: Django (Python)

Forecasting: ARIMA model via statsmodels

Frontend: Django templates with HTML/CSS

Data: Public dataset of bicycle parking in France

# Screenshots
## HomePage:
![alt text](https://github.com/HaekalMadani/Velo-Parking/blob/main/images/homepage.png?raw=true)

## Selecting a parking lot:
![alt text](https://github.com/HaekalMadani/Velo-Parking/blob/main/images/map-select.png?raw=true)

## Example of prediction of hourly occupancy 
[alt text](https://github.com/HaekalMadani/Velo-Parking/blob/main/images/stats1.png?raw=true)
