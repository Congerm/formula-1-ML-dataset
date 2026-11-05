# formula-1-ML-dataset
This is a project for a statistics machine learning course. A collaboration between Bekah Jensen and Matthew Conger.

## Checkpoint 1: Project proposal summary

**Date:** \[Oct 27, 2026\]

Our project will use Formula 1 data from the OpenF1 API to investigate whether weather conditions, vehicle and driver statistics, overtakes, and race position can help predict the number of yellow flags associated with a race event. Each observation will represent a race event.

We will build a reproducible dataset and machine-learning pipeline by collecting, cleaning, and combining relevant OpenF1 data. Descision Trees will serve as the reference model. We will evaluate our model with cross-validation.

The project will be reproducible through an ingestion Jupyter notebook that documents data collection and transformation. The main risks are incomplete or imperfect API data, too many potential predictors, and computational limits. If necessary, we will reduce the number of predictors or focus on a smaller scope.

## Checkpoint 2: Data checkpoint

**Date:** \[Nov 3, 2026\]

## Data
- Where did the data come from, and how did you obtain or prepare them?  
  - The data was gathered from OpenF1, where we used API requests to request data from the Sessions, Flag, and Weather endpoints. We also plan to include circuit length and circuit type  ("Permanent", "Temporary \- Street", or "Temporary \- Road"). These predictors will be gathered later. After we requested the data sets from the API endpoints, we calculated the mean for the weather observations. The weather data for each session is calculated multiple times throughout the race, we grouped these observations by session key and took an average of the numerical measures we were interested in. Every time a flag is recorded in the flag endpoint it creates an instance rather than a count of the flag type for a specific race session. We grouped these observations by session key and counted how many instances there were in the data for each session key. We appended both the weather and yellow flag transformed data to the session data which includes information about the meetings and locations of the sessions.  
- What data are available to your team now? What remains to be collected or cleaned?  
  - We currently have the weather, flag instances, and the session data, we have yet to add the circuit type and the circuit length. The circuit type will be gathered from another API endpoint from OpenF1, the circuit length will be sourced online, OpenF1 does not store circuit length information. For the session types that did not have any Flag instances, we filled the NA values with zero.  
- **Route C:** What does your first collected and cleaned sample contain?  
  - Our first collected and cleaned sample contains flag counts, average weather measurements, track location, session ids, and dates.
## Evaluation plan
- What comparison, split, metric, or diagnostic will help answer your question? Why?  
  - We will use the number of Yellow flags to answer our questions because we want to know how other things affect that outcome.  
- How will you avoid data leakage or another misleading comparison?  
  - We will use a cleaning pipeline and then use a standard train/test split before the data enters the ML pipeline to train our model.


**Full dataset:** [`sessions_with_weather_and_yellow_flags.csv`](sessions_with_weather_and_yellow_flags.csv)
