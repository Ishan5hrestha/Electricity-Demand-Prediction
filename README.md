# Electricity-Demand-Prediction
Predict the electric demand for upcoming week with historical data using KNN. The prediction is done with respect to time of the year. The data shows predictible curves each year on closer months. Initially temperature and humidity data from Tribhuwan International Airport were also taken with the electric data but they showed little correlation. So they were dropped and only month, date and time were taken into account which resulted in over 95% accuracy.

## Tools used
- HTML, CSS, JS
- Django
- Scikit-learn
- MySQL

## Installation
```
pip install django
pip install -U scikit-learn
```
## Run
```
python manage.py runserver
```
## Interface
The website features panel for NEA officials to:
- Login and view or download 
- Upload electric data
- Upload temperature and humidity data in the same format as were given by TIA
- Generate full dataset from uploaded data
- Train model using the generated dataset
- Predict the value of upcoming week's data

## Our Project

Database of electric data from Nepal Electricity Authority(NEA) and meterological data From Tribhuwan International Airport(TIA) has not been included due to confidentiality.
