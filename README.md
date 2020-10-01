# Spotify_Popularity_Classification

This project seeks to classify rap songs as either popular or not based on various features obtained from Spotify's API. The project aims to create a model that prioritizes predictive performance over interpretable performance. 

**Model Use Case**: An artist creates a new song. Using the model, the artist can see the prediction on whether or not it will be popular. If yes, the artist can spend the time and money promoting the song, spending money on ads, etc. If no, then the artist knows to not waste time and get back to the drawing board (studio).

Items of note in this repository include:
  * **scripts**: These scripts are how I got my data and stored it in a mysql database
  * **Spotify_EDA.ipynb**: Initial analysis of dataset, visualizations, some feature engineering, separated out rap songs from all songs
  * **Rap_Modeling.ipynb**: Handles class imbalance and then proceeds into various models
  * **Rap_Release_Radar_Test.ipynb**: Tests best model on new rap songs from Spotify's release radar playlist

#  EDA and Visualization 

After clearning and organizing the data, the first thing I wanted to check was class imbalance. The following chart shows our rap songs, where 1 represents a popular song and 2 represents an unpopular song

![Image](pics/orig_pop_count_rap.png?raw=true)

A clear class imbalance. This will need to be addressed in the modeling notebook. The next chart of note I would like to share from the EDA notebook is one detailing the correlation better the predictor features and the target variable. This chart shows the features with the largest correlation. Note, that because of class imbalance and the fact that models don't go strictly off correlation that this should not be read as the ground truth, but instead an early insight:

![Image](pics/correlation_w_popularity.png?raw=true)

#  Modeling

To address class imbalance, I created two training and testing sets:
1. Using upscaling techniques
1. Using balanced class weighting

I proceed to use these throughout the modeling process, creating models utilizing the following algorithms: logistic regression, decision tree classification, random forest classification, xgboost classification, and then finally aggregating them all together into a voting classifier. Random Forest and the Voting Classifier performed the best overal. 

**Evaluation Metric**: I chose to model for the best f1-score. Originally I thought recall would be most important, because if a song truly was popular, I would want to make sure my model predicts the most amount of popular songs out of ones that are truly popular. However, precision of my model would represent "of all the songs I predicted to be popular, how many actually were". I believe this to be an import metric as well. If my model predicted popular for everything, recall would be 1, but precision and f1 would likely suffer and the model would be poor. Thus, I want to harmonize the two and predict for the best all around model -- thus, the f1-score. 

The following chart shows feature importance from the perspective of the random forest model. Note this does not indicate a positive or negative relationship as the correlation chart does above, however, it more or less says the same features have the largest effects, namely energy, liveness, speechiness, and danceability.

**Note**: [Here](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) is a link to describtions for Spotify song features.

![Image](pics/random_forest_feature_imp.png?raw=true)

**The results of all models are shown below**
Accuracy - Top left
F1-Score - Top right
Recall - Bottom left
Precision - Bottom right

**Best F1: 0.82**

![Image](pics/model_performance.png?raw=true)

#  Test on Spotify Release Radar (Very New Songs)

I grabbed data from one of Spotify's release radar playlists, and then segmented that into rap only by the same criteria I did in my EDA notebook. Once split out, the set had the following distribution of the target variable, popular:

![Image](pics/release_radar_pop_count.png?raw=true)

**Important** -- Note the class imbalance here is the opposite from my original dataset. This will be talked about in the analysis and conclusion section below.

**Best F1: 0.615**

#  Analysis and Conclusion

#  Next Steps






