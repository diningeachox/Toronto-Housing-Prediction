# Toronto-Housing-Prediction
A machine learning model for predicting Toronto condo prices. 

## Dataset
The raw data was scraped from realmaster.ca sold listings over a one month period. Data from 2000+ condos were compiled, forming the dataset.
The scraping was done with BeautifulSoup. 
Toronto neighborhood data can be obtained here: https://open.toronto.ca/dataset/neighbourhood-profiles/
Toronto subway data can be obtained here: https://scruss.com/blog/2005/12/14/toronto-subway-station-gps-locations/ 


## Proprocessing
A major component of this project was to include relevant **geographic data** for the condos as well as the data about the buildings themselves. For each condo, I used its location to determine what Toronto neighborhood it was in, along with important metrics such as **average income, unemployment rate** and **population density** of said neighborhood. Then I used the subway data against each condo to calculate the **distance to the nearest subway station**. 

In order to extract the geographical coordinates from each condo's location, I used the google API called Geocoder. If you want to get geographical coordinates using Geocoder you will have to sign up and get your own API key. You are allowed up to **2500 location queries per day** free of charge.

I then compared these coordinates to the district polygons given in the Toronto neighborhood dataset to determine which neighborhood the condo belonged to.

Categorical variables such as balcony type were given one-hot encodings. All real-valued data were normalized with the Yeo-Johnson transform, this resulted in lower errors for the model. Square feet were given as a range, I split this data into two variables: **Min Square Feet** and **Max Square Feet**.

## Independent Variables
The independent variables (X = (X_1, X_2, ...)) used for the model are:
| Feature  | Data Type | 
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

These variables were selected with certain domain knowledge in mind, such as:
* The floor of the unit affecting the price
* The location of the unit affecting the price
* Units with balconies are worth more than units without
* High income areas have higher real estate prices

## Visualizations
Below is a geographical scatterplot of all the locations of the condos, with a color scheme for showing mean average income of the nieghborhood and the prices of the condos.
![toronto_condos_plot](https://user-images.githubusercontent.com/24876548/135324573-efcb1a1c-f1ae-4388-8da8-ac53942d37c9.png| width=400)


## Methods used to improve predictions
* Using the Yeo-Johnson transform on all real-valued variables to a normal distribution
* Selecting the 15 best variables with sklearn.SelectKBest
* Hyperparameter Grid Search 
* Stacking models

## Files
scraper.py is used to scrape data from realmaster.ca, right now it scrapes listing which are already sold
