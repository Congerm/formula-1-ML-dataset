# formula-1-ML-dataset
This is a project for a statistics machine learning course. A collaboration between Bekah Jensen and Matthew Conger.

## Checkpoint 1: Project proposal summary

**Date:** October 27, 2026

Our project will use Formula 1 data from the OpenF1 API to investigate whether weather conditions, vehicle and driver statistics, overtakes, and race position can help predict the number of yellow flags associated with a race event. Each observation will represent a race event.

We will build a reproducible dataset and machine-learning pipeline by collecting, cleaning, and combining relevant OpenF1 data. Descision Trees will serve as the reference model. We will evaluate our model with cross-validation.

The project will be reproducible through an ingestion Jupyter notebook that documents data collection and transformation. The main risks are incomplete or imperfect API data, too many potential predictors, and computational limits. If necessary, we will reduce the number of predictors or focus on a smaller scope.

## Checkpoint 2: Data checkpoint

**Date:** November 5, 2026

For our second checkpoint, we collected session and weather information from the OpenF1 API and combined it into one dataset. The dataset has 619 observations and 23 variables. Each row represents one Formula 1 Practice, Qualifying, or Race session. Along with basic session and circuit information, we included the date, location, cancellation status, weather measurements, and the number of yellow flags recorded during each session.

We checked and cleaned the collected data and do not have any blank values. The number of yellow flags ranges from 0 to 84, which shows that the response is not evenly distributed. We will keep this in mind when we train and evaluate our decision-tree model.

Here is a quick overview of the dataset:

| Dataset detail | Result |
|---|---|
| Observations | 619 |
| Variables | 23 |
| Session types | Practice, Qualifying, Race |
| Response variable | `yellow_flag_count` |
| Response range | 0–84 |

**Full dataset:** [`sessions_with_weather_and_yellow_flags.csv`](sessions_with_weather_and_yellow_flags.csv)
