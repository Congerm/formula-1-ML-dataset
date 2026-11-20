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

**Full dataset:** [`sessions_with_weather_and_yellow_flags.csv`](DATA/sessions_with_weather_and_yellow_flags.csv)



## Checkpoint 3: Working investigation

**Date:** November 12, 2026

### Working code and evidence

Our source-to-cleaned-data pipeline runs end to end:

1. `data_check.ipynb` pulls sessions, weather, and yellow-flag events from the
   OpenF1 API (data from 2023 onward, collected November 2026; OpenF1 API
   access is free) and writes raw CSVs.
2. `DATA/data_pull/get_track_lengths.py` and `DATA/data_pull/get_track_types.py`
   pull circuit length and track type (street vs. race) from the f1-circuits
   reference table at aidb.si, matched against circuits seen in lap-time data.
3. `DATA/combine_flag_on_track.py` merges the sessions/weather/flags table with
   circuit length and type via `circuit_name_mapping.csv` and writes
   `DATA/sessions_complete.csv`.

Reproduce with `uv run python DATA/combine_flag_on_track.py` after the pull
scripts have run (the merge prints join coverage).
The cleaned output is `DATA/sessions_complete.csv` ([link](DATA/sessions_complete.csv)).

### Cleaned dataset and quality checks

Each observation is one Formula 1 session (Practice, Qualifying, or Race):
session and circuit identifiers, average weather measurements over the session
(rainfall, air/track temperature, humidity, wind, pressure), track
characteristics (lap length, laps, total race distance, track type), and the
response `yellow_flag_count`. 619 rows collected, 28 columns.

Quality checks so far: we discovered that the OpenF1 sessions endpoint also
returns future calendar sessions that have not happened yet. These rows carry
zeroed weather measurements and zero yellow flags, which would contaminate
training (139 rows, about 22% of the data, including the entire 2027
schedule and the three remaining 2026 rounds). We now drop any session whose
`date_end` is after the collection date, leaving **480 real sessions**. The
same check resolved a join gap: the 2027 calendar includes Algarve and
Istanbul, which do not appear in our track tables.
`yellow_flag_count` ranges 0–84 and is heavily right-skewed, so we report
metrics on the raw scale and note the skew.

### Initial ML result

We fit a `RandomForestRegressor` on the cleaned dataset to predict
`yellow_flag_count` from weather averages, track characteristics, session
type, track type, and circuit name (one-hot encoded). Evaluation uses a
75/25 train-test split (360 train / 120 test, `random_state=42`) with RMSE,
MAE, and R² on the test set, compared against a mean baseline.
Code and output: [`initial_fit.ipynb`](initial_fit.ipynb).

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Mean baseline | 8.905 | 4.398 | −0.009 |
| Random forest | 8.430 | 3.859 | 0.096 |

The forest improves on the baseline, but R² of 0.096 is very low: session
weather and track features alone explain little of the variance in yellow
flags. Feature importances are dominated by a circuit indicator
(`circuit_short_name_Baku` at 0.24, likely capturing Baku's unusually high
flag counts), followed by pressure (0.11), track temperature (0.10), wind
direction (0.09), and rainfall (0.09).

### Next question

- Plan change since Nov 5: we moved from a single decision tree to a random
  forest as the main model, and added circuit and track metadata as
  predictors. Given the low R², our next step is to add the more informative
  predictors from our original proposal — driver/vehicle statistics,
  overtakes, and race position — since session-level weather and track
  descriptors alone are clearly not enough.
- Uncertain or blocked: the response is skewed and much of the signal may
  live at the driver/lap level rather than the session level. If added
  predictors do not lift performance, we will reduce scope to Race sessions
  only or try a transformed response (e.g., log of `yellow_flag_count`).

## Checkpoint 4: Evidence and interpretation

**Date:** November 19, 2026

### Evidence So Far
The dataset shows that there are enough observations for each session type. Practice sessions account for 51% of the data while both qualifying and races each contain 24% of the observations. While the practice sessions do account for half of the data, this does not indicate an extreme class imbalance.
| Session Type | Count   |
| ------------ | ------- |
| Practice     | 246     |
| Qualifying   | 117     |
| Race         | 116     |
| **Total**    | **479** |

**Circuit counts**

Looking at the instances of flag counts per location type indicates that we have more observations for some locations than others. This may pose a bias issue since there are more instances for locations such as Sakhir than Madring. 

| Circuit | Count |
|---|---:|
| Sakhir | 35 |
| Jeddah | 20 |
| Melbourne | 20 |
| Baku | 20 |
| Miami | 20 |
| Monte Carlo | 20 |
| Catalunya | 20 |
| Montreal | 20 |
| Spielberg | 20 |
| Silverstone | 20 |
| Hungaroring | 20 |
| Spa-Francorchamps | 20 |
| Zandvoort | 20 |
| Monza | 20 |
| Singapore | 20 |
| Suzuka | 20 |
| Austin | 20 |
| Mexico City | 20 |
| Interlagos | 20 |
| Imola | 15 |
| Lusail | 15 |
| Las Vegas | 15 |
| Yas Marina Circuit | 15 |
| Shanghai | 15 |
| Madring | 5 |
| Kuala Lumpur | 4 |

EDA plots: [`EDA.ipynb`](EDA.ipynb) — flag-count histogram, boxplots by circuit, track type, and session type, and rainfall/lap-length scatterplots.

**Other data-quality checks.** We also discovered that the OpenF1 sessions endpoint returns future calendar placeholders, 139 rows (22% of the initial pull) with zero's for weather and flags, including the whole 2027 schedule. Dropping sessions whose `date_end` is after the collection date leaves 480 real sessions with no missing feature values and full coverage of the circuit length/type join. The response remains heavily right-skewed (0–44 flags per session). Evidence: [`combine_flag_on_track.py`](DATA/combine_flag_on_track.py) join output and the filtering cell in [`initial_fit.ipynb`](initial_fit.ipynb).

**Outlier removal.** We dropped the October 4, 2026 Sepang race. It was a real but abnormal event (rain delays, an FIA software glitch, and a red flag produced 84 yellow flags, over double the next-highest session) — leaving 479 sessions and improving the refit to RMSE 4.647, R² 0.136 ([`initial_fit.ipynb`](initial_fit.ipynb)).


### What the Inital Fit Says
Our initial fit of the data using the following predictors:
- Rainfall
- Air Temperature
- Humidity
- Wind Speed
- Pressure
- Track Temperature
- Wind Direction
- Lap Length (km)
- Laps
- Total Track Length
- Circut Name
- Session Type
- Track Type

Gave an RMSE value of 8.43, and an $R^2$ of 0.096. These values indicate that the inital model fit performs poorly. In seeking out to predict the number of yellow flag instances that will ocurr in a given Formula-1 event, our model is about 8-9 flag estimates off from the true flag value. Considering the research question, this initial model needs to be altered. 

Code and output: [`initial_fit.ipynb`](initial_fit.ipynb).

**Baseline comparison.** Against a mean baseline (`DummyRegressor`: RMSE 5.000, MAE 3.673, R² −0.000 on the same 75/25 split), the forest improves RMSE to 4.647 and MAE to 3.301, but R² of 0.136 means session-level aggregates still explain only about a tenth of the variance.

### Interpretation and next step

**Informative limitation.** The most important feature is the Baku circuit indicator (importance 0.19), ahead of any weather variable (track temperature is next). This means some of the model's prediction comes from memorizing the location of a session, not from the weather conditions or other factors.

**What the evidence changed.** Our original plan assumed weather would be a primary predictor. However, from what we have seen, the weather features are not huge contributors to predicting yellow flags, and a lot of the variance comes from other factors, some of which we do not have data for.

Next we will:

1. re-run the forest without the circuit indicators and compare R² against this 0.136 baseline on the same split.

2. if gains remain small, try a Race-sessions-only model or a transformed response, and report results with cross-validation rather than a single split.

3. if it still remains small, we will try to look at other data sources or features that might capture the underlying patterns better.
