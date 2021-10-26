# Electricity-Demand-Prediction
Predict the electric demand for upcoming week with historical data using KNN.  
The prediction is done with respect to time of the year. When we visualized the data, we found predictible curves each year on closer months. Initially temperature and humidity data from Tribhuwan International Airport were also taken but they showed little correlation with the electric data. So they were dropped and only month, date and time were taken into account which resulted in over 95% accuracy.

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
- Login and view or download data
- Upload electric data
- Upload temperature and humidity data in the same format as were given by TIA
- Generate full dataset from uploaded data
- Train model using the generated dataset
- Predict the value of upcoming week's data

## Our Project
### Obatining the data
We visited New Baneshwar area grid to obtain electric data. The data were completely hand written. We obtained 2.5 years of hourly data from year 2074.  
These data had to be converted to digital form by our team.

![IMG_20200126_132303](https://user-images.githubusercontent.com/45944370/138814962-30660680-a13e-48f2-9191-e093257df026.jpg)

![2021-10-26 11_15_33-Window](https://user-images.githubusercontent.com/45944370/138814664-47986b9f-6518-4ce2-b913-97456a38e5a3.png)

### Data Visualization
Except some few exceptions, the electric load showed quite similar curves everyday. With change in weather and temperature there was slight change in electric load too. This was tied to months and days of the calendar as a month has similar climate every year.  
The Blue line is for electric load while Orange is temperature fluctuation during a day.
![Datagraph](https://user-images.githubusercontent.com/45944370/138815481-c9e08922-0233-446c-ac3e-5dfccfd62251.png)
![2021-10-26 11_29_09-forecast_puredataset csv - Excel](https://user-images.githubusercontent.com/45944370/138816087-b43106f1-b475-4b9b-ba68-2397e3f0da4b.png)


### FrontEnd Design
Our user interface was designed using HTML, CSS, JavaScript with Bootstrap to easen the process.
![2021-10-26 11_22_07-Greenshot](https://user-images.githubusercontent.com/45944370/138815297-5cd438fa-23dc-4e0b-b36d-7413fe2bf0b1.png)



Database of electric data from Nepal Electricity Authority(NEA) and meterological data From Tribhuwan International Airport(TIA) has not been included due to confidentiality.
