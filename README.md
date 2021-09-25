# Toronto-Housing-Prediction
A machine learning model for predicting Toronto condo prices

## Dataset
The raw data was scraped from realmaster.ca sold listings over a one month period. This resulted in 2000+ condos forming the dataset.
The scraping was done with BeautifulSoup. 

## Proprocessing
A major component of this project was to use relevant geographic data for the condos as well as the data about the buildings themselves. For each condo, I used its location to determine what Toronto neighborhood it was in, along with important metrics such as **average income, unemployment rate** and **population density** of said neighborhood. Then I downloaded Toronto subway data from https://scruss.com/blog/2005/12/14/toronto-subway-station-gps-locations/ and used it against each condo to calculate the **distance to the nearest subway station**. 

In order to extract the geographical coordinates from each condo's location, I used the google API called Geocoder. I then compared these coordinates to the district polygons given in the Toronto neighborhood dataset to determine which neighborhood the condo belonged to.

Categorical variables such as balcony type were given one-hot encodings. All real-valued data were normalized with the Yeo-Johnson transform, this resulted in lower errors for the model. Square feet were given as a range, I split this data into two variables: **Min Square Feet** and **Max Square Feet**.

## Independent Variables
The independent variables (X = (X_1, X_2, ...)) used for the model are:
| Feature  | Range |
| ------------- | ------------- |
| Latitude  | Real-valued  |
| Longitude  | Real-valued |
| Bedrooms  | Int-valued (range from 1 to 3)  |
| Bathrooms  | Int-valued (range from 1 to 3) |
| Floor  | Int-valued (range from 1 to 40+) |
| Balcony Enclosed  | Bool-valued |
| Balcony Open  | Bool-valued |
| Balcony Terrace  | Bool-valued |
| Balcony Juliet | Bool-valued |
| No Balcony  | Bool-valued |
| Base Parking  | Int valued (range from 0 to 10) |
| Additional Parking  | Int valued (range from 0 to 10) |
| Meaning District Income  | Real-valued  |
| Unemployment Rate  | Real-valued |
| Population Density | Real-valued  |
| Nearest Station | Real-valued |


## Methods used to improve predictions
* Scaling all real-valued variables to [0, 1]
* Using the Yeo-Johnson transform on all real-valued variables
* Selecting the 15 best variables with sklearn.SelectKBest
* Hyperparameter Grid Search 
* Stacking models
