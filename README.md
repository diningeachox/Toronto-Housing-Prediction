# Toronto-Housing-Prediction
A machine learning model for predicting Toronto condo prices

## Dataset
The raw data was scraped from realmaster.ca sold listings over a one month period. This resulted in 2000+ condos forming the dataset.
The scraping was done with BeautifulSoup. 

## Proprocessing
A major component of this project was to use relevant geographic data for the condos as well as the data about the buildings themselves. For each condo, I used its location to determine what Toronto neighborhood it was in, along with important metrics such as **average income, unemployment rate** and **population density** of said neighborhood. Then I downloaded Toronto subway data from https://scruss.com/blog/2005/12/14/toronto-subway-station-gps-locations/ and used it against each condo to calculate the **distance to the nearest subway station**. 

In order to extract the geographical coordinates from each condo's location, I used the google API called Geocoder. I then compared these coordinates to the district polygons given in the Toronto neighborhood dataset to determine which neighborhood the condo belonged to.

Categorical variables such as balcony type were given one-hot encodings. All real-valued data were normalized with the Yeo-Johnson transform, this resulted in lower errors for the model. 

## Independent Variables
The independent variables (X = (X_1, X_2, ...)) used for the model are:
| Feature  | Range |
| ------------- | ------------- |
| Latitude  | Real-valued  |
| Longitude  | Real-valued |
| Latitude  | Real-valued  |
| Longitude  | Real-valued |
Floor                 2617 non-null   int64  
 3   Bedrooms              2617 non-null   float64
 4   Bathrooms             2617 non-null   float64
 5   x0_Encl               2617 non-null   float64
 6   x0_Jlte               2617 non-null   float64
 7   x0_None               2617 non-null   float64
 8   x0_Open               2617 non-null   float64
 9   x0_Terr               2617 non-null   float64
 10  base_parking          2617 non-null   int64  
 11  addition_parking      2617 non-null   int64  
 12  Min square feet       2617 non-null   int64  
 13  Max square feet       2617 non-null   int64  
 14  Latitude              2617 non-null   float64
 15  Longitude             2617 non-null   float64
 16  city_district         2617 non-null   object 
 17  district_code         2617 non-null   int64  
 18  mean_district_income  2617 non-null   int64  
 19  unemployment_rate     2617 non-null   float64
 20  pop_density           2617 non-null   int64  
 21  nearest_station       2617 non-null   float64

## Methods used to improve predictions
