# Spotify_Popularity_Classification

This project seeks to classify rap songs as either popular or not based on various features obtained from Spotify's API. The project is outlined as follows:
- Scrapes Wikipedia for albums from 2015-2020
- Pulls all songs from Spotify that are part of those albums
- Perform some initial EDA, condense dataset into rap only songs
- Build various models to predict rap song popularity



Items of note in this repository include:
  * **scripts/* **: These scripts are how I got my data and put them in SQL
  * **Spotify_EDA.ipynb**: Initial analysis of dataset, visualizations, some feature engineering
  * **Rap_Modeling.ipynb**: Handles class imbalance and then proceeds into various models
  * **Rap_Release_Radar_Test.ipynb**: Tests best model on new rap songs from Spotify's release radar playlist

#  EDA and Visualization 

![Image](Images/life_expect_by_status.png?raw=true)

