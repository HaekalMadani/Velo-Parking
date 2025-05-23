from django.shortcuts import render, redirect
from django.conf import settings
from django import forms
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
import warnings
import os
import base64
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from .models import Feedback
from .forms import FeedbackForm


warnings.filterwarnings("ignore")

def homepage(request):
    # Read the CSV file
    df = pd.read_csv('/Users/haekalmadani/Desktop/PBL3 jango/myproject/static/data/station_20.csv')

    # Extract necessary data
    markers = df[['Address', 'lat ', 'lon', 'Station name', 'StationId', 'Capacity', 'Fee', 'Infrastrucutre']].values.tolist()

    context = {
        'markers': markers,
        'name': 'user1',
    }
    return render(request, 'home/homepage.html', context)

def navigate_view(request, latitude, longitude, place):
    context = {
        'latitude': latitude,
        'longitude': longitude,
        'place': place
    }
    return render(request, 'home/navigate.html', context)



def occupancy_view(request, station_id):
    df = pd.read_csv('/Users/haekalmadani/Desktop/PBL3 jango/myproject/static/data/station_20_hr.csv')

    # Rename columns to match the DataFrame
    df.columns = ['ID', 'Year', 'Quarter', 'Time', 'Occupancy', 'Lat_Lon']

    # Print the first few rows of the DataFrame
    print("First few rows of the DataFrame:")
    print(df.head())

    # Print unique IDs in the DataFrame
    print("Unique station IDs in the DataFrame:")
    print(df['ID'].unique())

    df_filtered = df[df['ID'] == int(station_id)]
    print(f"Filtered DataFrame for station ID {station_id}:")
    print(df_filtered)

    if df_filtered.empty:
        context = {
            'error': f'No data available for station ID {station_id}'
        }
        return render(request, 'home/occupancy_juvisy.html', context)

    def categorize_occupancy(occupancy):
        if occupancy <= 20:
            return 'Uncrowded'
        elif occupancy <= 40:
            return 'Less Crowded'
        elif occupancy <= 60:
            return 'Relatively Crowded'
        else:
            return 'Crowded'

    df_filtered['Category'] = df_filtered['Occupancy'].apply(categorize_occupancy)

    df_filtered['Time'] = df_filtered['Time'].str.replace(' ', '')
    df_filtered['Time'] = df_filtered['Time'].str.split('-').apply(lambda x: f"{x[0]}-{x[1]}" if len(x) == 2 else x[0])
    df_filtered = df_filtered.sort_values(by=['Time'])
    df_filtered = df_filtered.drop_duplicates(subset=['Time'], keep='first')

    df_grouped = df_filtered.groupby('Time').agg({'Occupancy': 'mean', 'Category': 'first'}).reset_index()

    time_labels = df_grouped['Time'].tolist()
    occupancy_data = [round(occ, 2) for occ in df_grouped['Occupancy'].tolist()]
    categories = df_grouped['Category'].tolist()

    print("Time labels:", time_labels)
    print("Occupancy data:", occupancy_data)
    print("Categories:", categories)

    if not occupancy_data:
        context = {
            'error': f'No occupancy data available for station ID {station_id}'
        }
        return render(request, 'home/occupancy_juvisy.html', context)

    peak_index = occupancy_data.index(max(occupancy_data))
    peak_hour = time_labels[peak_index]
    occupancy_percentage = occupancy_data[peak_index]

    hourly_data = [(time, f"{occupancy:.2f}", category) for time, occupancy, category in zip(time_labels, occupancy_data, categories)]

    context = {
        'time_labels': time_labels,
        'occupancy_data': occupancy_data,
        'categories': categories,
        'peak_hour': peak_hour,
        'occupancy_percentage': f"{occupancy_percentage:.2f}",
        'hourly_data': hourly_data
    }

    return render(request, 'home/occupancy_juvisy.html', context)




def occupancy_city(request):
    # Load and preprocess the data
    df = pd.read_excel('/Users/haekalmadani/Desktop/PBL3 jango/myproject/static/data/filtering_dataset.xlsx')
    df = df[df['Occupancy'] != 0]
    df = df[df['Occupancy'] <= 100]
    df['Year'] = df['Year'].astype(str)
    df['Period'] = df['Year'] + ' ' + df['Trimester']

    # Convert Period column to Period type
    df['Period'] = pd.PeriodIndex(df['Period'], freq='Q')

    # Split into train and test sets
    X = df['Occupancy'].values
    size = int(len(X) * 0.7)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]

    # Prepare lists to hold results
    predictions = []
    periods = []
    actuals = []

    # Walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(method='statespace')
        output = model_fit.forecast()
        yhat = output[0]

        # Append the forecast and actual results
        predictions.append(yhat)
        actuals.append(test[t])
        periods.append(df['Period'].iloc[size + t])  # Get the period for the current test sample
        history.append(test[t])

    # Evaluate forecasts
    rmse = np.sqrt(mean_squared_error(test, predictions))
    mape = mean_absolute_percentage_error(test, predictions)

    # Create a DataFrame for the forecast results
    results_df = pd.DataFrame({
        'Period': periods,
        'Forecasted_Occupancy': predictions,
        'Actual_Occupancy': actuals
    })

    # Forecast the next 8 quarters (2 years)
    forecast_steps = 12
    forecast = model_fit.forecast(steps=forecast_steps)
    forecast_periods = pd.period_range(start=df['Period'].max() + 1, periods=forecast_steps, freq='Q')
    forecast_df = pd.DataFrame({'Period': forecast_periods, 'Forecasted_Occupancy': forecast})

    # Add season information
    forecast_df['Season'] = forecast_df['Period'].apply(lambda x: x.quarter)

    # Convert season to a readable format
    season_map = {1: 'winter', 2: 'spring', 3: 'summer', 4: 'fall'}
    forecast_df['Season'] = forecast_df['Season'].map(season_map)

    # Format the period strings
    forecast_df['Period_Display'] = forecast_df['Period'].apply(lambda x: f"{x.start_time.strftime('%Y')} ({x.start_time.strftime('%b')} - {x.end_time.strftime('%b')})")

    # Combine actual data and forecast for plotting
    combined_df = pd.concat([df[['Period', 'Occupancy']], forecast_df.set_index('Period').rename(columns={'Forecasted_Occupancy': 'Occupancy'})])

    # Prepare data for plotting
    train_idx = [*range(len(train))]
    test_pred_idx = [*range(train_idx[-1] + 1, train_idx[-1] + 1 + len(test))]
    forecast_idx = [*range(test_pred_idx[-1] + 1, test_pred_idx[-1] + 1 + len(forecast))]

    # Plot the results
    plt.figure(figsize=(19, 6))
    plt.plot(train_idx, train, label='Train')
    plt.plot(test_pred_idx, test, label='Test')
    plt.plot(test_pred_idx, predictions, label='Forecast', color='red')
    plt.plot(forecast_idx, forecast, label='Future Forecast', color='green', linestyle='--')
    plt.legend(loc='best')
    plt.title('ARIMA Model Forecast')
    plt.xlabel('Period')
    plt.ylabel('Occupancy Rate')

    all_periods = [str(p) for p in df['Period']] + [str(p) for p in forecast_periods]
    plt.xticks(ticks=forecast_idx, labels=all_periods[-len(forecast_idx):], rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Plot for seasonal comparison
    season_avg = forecast_df.groupby('Season')['Forecasted_Occupancy'].mean()
    # Example usage if you had a second variable
    season_avg.plot(kind='pie', colors=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'], figsize=(10, 6), autopct='%1.1f%%')

    plt.title('Average Forecasted Occupancy by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Occupancy')
    plt.xticks(rotation=0)

    buffer_season = BytesIO()
    plt.savefig(buffer_season, format='png')
    plt.close()
    buffer_season.seek(0)
    season_plot_data = base64.b64encode(buffer_season.getvalue()).decode('utf-8')

    context = {
        'rmse': rmse,
        'mape': mape * 100,
        'results_df': results_df.to_html(index=False),
        'future_forecast_table': forecast_df.to_html(index=False),
        'plot_data': plot_data,
        'season_plot_data': season_plot_data,
        'future_forecast': forecast_df.to_dict('records'),
        'season_comparison': season_avg.to_frame().reset_index().to_html(index=False),
    }

    return render(request, 'home/occupancy_city.html', context)

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            
             # Count all feedback submissions
            return redirect(f'/homepage/feedback/thanks')  # Redirect to thanks view with count parameter
    else:
        form = FeedbackForm()
    return render(request, 'home/feedback.html', {'form': form})

def feedback_thanks_view(request):
    return render(request, 'home/thanks.html')

def userProfile(request):
    feedback_count = Feedback.objects.count() 
    return render(request, 'home/user.html', {'feedback_count': feedback_count})  # Pass feedback_count to the template