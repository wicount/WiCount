import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from sklearn.linear_model import LinearRegression
from scipy import stats
import sqlite3 as lite



def read_data():
    # Read csv file into a dataframe.
    # Ideally this should just import the dataframe from DataAnalysis.py but issue with PATH file.
    try:
        df = pd.read_csv('full_dataset_hour.csv', index_col=0)
        # index_col parameter removes the 'unnamed column' which is added when reading from a csv

    except OSError:
        print("Filename not found!")
    except Exception as e: print(e)

    df['GroundTruth'] = df.Capacity * df.SurveyPercentage
    df = df[['room_id', 'Count', 'GroundTruth', 'SurveyPercentage', 'Capacity', 'Room', 'LogDate', 'Date']]
    df['SurveyPercentage'] = df['SurveyPercentage'].apply(lambda x: x*100)

    return df


def prepare_data(df):

    df['UniqueClass'] = df['Date'] + ' ' + df['Room']
    uniquedf = df['UniqueClass']

    count = uniquedf.value_counts().sort_index()
    # sorting to match the number of values for a given hour with

    df = df.sort_values(['UniqueClass', 'LogDate']).reset_index(drop=True)
    # Now indexes match the count values so we can use them for loop traversal in the list builder

    maxlist = []
    averagelist = []
    medianlist = []
    modelist = []

    row = 0
    for step in count:

        max = 0
        temp = []

        for j in range(row, row+step):
            temp.append(df.Count[j])
            if df.Count[j] > max:
                max = df.Count[j]

        maxlist.append(max)
        # make max list
        average = float(format(np.average(temp), '.2f'))
        # make average list
        #formatting to 2 decimal places produces string so need to cast as float
        median = np.median(temp)
        # make median list
        mode = stats.mode(temp[0])
        # make mode list (index 0 selects the value rather than the whole array)
        averagelist.append(average)
        medianlist.append(median)
        modelist.append((mode[0])[0])
        # index 0 is the value, 1 is the number of occurrences
        # second index 0 selects the value rather than an array containing the value + type
        # the scipy-stats module returns the lowest of any equally frequently occurring values.

        row += step

    df2 = pd.DataFrame(columns=df.columns)

    row = 0
    for step in count:
        df2 = df2.append(df.loc[row], ignore_index=True)
        row+=step

    df2['MaxCount'] = maxlist
    df2['AverageCount'] = averagelist
    df2['MedianCount'] = medianlist
    df2['ModeCount'] = modelist

    try:
        df2 = df2.drop('Count', axis=1)
    # no longer need count for specific time since we're using the average and maximum values for testing.
    except ValueError:
        pass
    # ValueError exception raised if Count has already been dropped.

    return df2


def train_model(trainingdf):
    wicountlm = sm.ols(formula="GroundTruth ~  MedianCount", data=trainingdf).fit()
    return wicountlm


def classify_prediction(df, i):

    # passing in this: df2_test.Predictions[row], row
    prediction = df.Predictions[i]

    capacity = df.Capacity[i]
    # selects the relevant capacity value for the room and assigns to a variable
    percentile_0 = 0
#     percentile_25 = capacity * 0.25
    percentile_50 = capacity * 0.5
#     percentile_75 = capacity * 0.75
    percentile_100 = capacity

# making ternary bins rather than original 0/25/50/75/100
    if prediction <= (percentile_50 - ((percentile_50 - percentile_0)/2)):
        return 0
    elif prediction >= percentile_50 - ((percentile_50 - percentile_0)/2) and prediction <= percentile_100 - ((percentile_100 - percentile_50)/2):
        return 50
    # if prediction (43) is greater than 20 and less than 60
    elif prediction >= percentile_100 - ((percentile_100 - percentile_50)/2):
        return 100


def make_predictions(df, wicountlm):

    predictions = wicountlm.predict(df)

    df['Predictions'] = predictions

    df = df.reset_index(drop=True)
    percentage = []


    for row in range(df.shape[0]):
        percentage.append(classify_prediction(df, row))

    print(df.shape)

    df['PredictedPercentage'] = percentage
    return df


def get_count_upload():

    # toDo: this needs the name of the file upload with count values. Currently using original dataset minus
    # surveypercentage for testing
    try:
        df = pd.read_csv('full_dataset_hour.csv', index_col=0)
        df = df.drop('SurveyPercentage', axis=1)


    except Exception as e:
        print(e)
    return df


def update_analytics_table(df):
    try:
        con = lite.connect('wicount.sqlite3')
        df.to_sql(con=con, name='analytics', if_exists='append', flavor='sqlite', index=False)
        # Set index to False because it's not a column but will be treated as one.
        print("Success! Table created or updated.")
    except Exception as e:
        print(e)


if __name__ == '__main__':

    trainingdf = read_data()
    # reads dataframe taken from the survey table (DataAnalytics.py)
    trainingdf = prepare_data(trainingdf)
    wicountlm = train_model(trainingdf)
    # training the model

    df = get_count_upload()
    df = prepare_data(df)
    # toDo: get dataframe from the count upload. Needs same columns to be present as the training data,
    # can fix by dropping SurveyData etc.

    df = make_predictions(df, wicountlm)
    print(df)
    update_analytics_table(df)


