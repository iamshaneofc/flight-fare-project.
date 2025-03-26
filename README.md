# Flight Fare Project

This repository contains tools for analyzing and predicting flight fares based on a dataset of flight details.

## Contents
- **`flight_fare_analysis.ipynb`**: A Jupyter Notebook for Exploratory Data Analysis (EDA) with visualizations like price distributions, airline comparisons, and correlation heatmaps.
- **`flight_fare_prediction.ipynb`**: A Jupyter Notebook to train an XGBoost model for predicting flight prices and save it for deployment.
- **`app.py`**: A Flask application to serve the prediction model via a web interface.
- **`templates/index.html`**: HTML template for the Flask app with a form to input flight details and display predicted prices.

## Usage
1. **Analysis**: Run `flight_fare_analysis.ipynb` in Jupyter or VS Code to explore the dataset (`Data_Train.xlsx` required).
2. **Prediction**: Run `flight_fare_prediction.ipynb` to generate `flight_price_prediction.sav` and `model_columns.pkl`.
3. **Web App**: Run `app.py` with Flask to launch the prediction interface (`python app.py`).

## Notes
- Large files (`Data_Train.xlsx`, `.sav`, `.pkl`) are not included due to size limits. Download the dataset separately and place it in the project folder.
- Ensure dependencies are installed: `pip install pandas numpy matplotlib seaborn scikit-learn xgboost flask`.

## Future Improvements
- Add day-of-week price analysis.
- Enhance the web app with more styling or features.
