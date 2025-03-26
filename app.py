from flask import Flask, request, render_template
import pandas as pd
import pickle
from datetime import datetime

app = Flask(__name__)

# Load the trained model and feature columns
model = pickle.load(open('flight_price_prediction.sav', 'rb'))
model_columns = pickle.load(open('model_columns.pkl', 'rb'))

# Helper function to calculate duration in minutes
def calculate_duration_minutes(dep_time, arr_time):
    dep = datetime.strptime(dep_time, '%Y-%m-%dT%H:%M')
    arr = datetime.strptime(arr_time, '%Y-%m-%dT%H:%M')
    duration = (arr - dep).total_seconds() / 60  # Convert to minutes
    return duration if duration >= 0 else duration + 24 * 60  # Handle overnight flights

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    airline = request.form['airline']
    source = request.form['source']
    destination = request.form['destination']
    total_stops = int(request.form['total_stops'])
    departure_datetime = request.form['departure_datetime']
    arrival_datetime = request.form['arrival_datetime']

    # Extract date and time components
    dep_dt = datetime.strptime(departure_datetime, '%Y-%m-%dT%H:%M')
    arr_dt = datetime.strptime(arrival_datetime, '%Y-%m-%dT%H:%M')
    date = dep_dt.day
    month = dep_dt.month
    dept_hour = dep_dt.hour
    dept_min = dep_dt.minute
    arrival_hour = arr_dt.hour
    arrival_min = arr_dt.minute
    duration_minutes = calculate_duration_minutes(departure_datetime, arrival_datetime)

    # Create a dictionary with input data
    input_data = {
        'Total_Stops': total_stops,
        'Date': date,
        'Month': month,
        'Dept_hour': dept_hour,
        'Dept_min': dept_min,
        'Arrival_hour': arrival_hour,
        'Arrival_min': arrival_min,
        'Duration_minutes': duration_minutes
    }

    # Add one-hot encoded columns (set all to 0 initially)
    for col in model_columns:
        if col not in input_data:
            if col.startswith('Airline_'):
                input_data[col] = 1 if col == f'Airline_{airline}' else 0
            elif col.startswith('Source_'):
                input_data[col] = 1 if col == f'Source_{source}' else 0
            elif col.startswith('Destination_'):
                input_data[col] = 1 if col == f'Destination_{destination}' else 0
            elif col.startswith('Additional_Info_'):
                input_data[col] = 0  # Assume 'No info' as default (adjust if needed)

    # Convert to DataFrame with correct column order
    input_df = pd.DataFrame([input_data], columns=model_columns)

    # Make prediction
    prediction = model.predict(input_df)[0]
    predicted_price = round(prediction, 2)

    # Render result
    return render_template('index.html', prediction_text=f"Predicted Flight Price: ₹{predicted_price}")

if __name__ == "__main__":
    app.run(debug=True)