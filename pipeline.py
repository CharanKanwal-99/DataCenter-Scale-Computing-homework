import pandas as pd
import numpy as np

def extract_data(source):
     
    # Reading csv file
    return pd.read_csv(source)

def transform_data(data):

    # Copying the data
    df = data.copy()

    # Dropping column with 25% & above missing value
    df = df.drop(['Name', 'Outcome Subtype'], axis = 1)

    # Deriving columns "Month" & "Year" from column "MonthYear"
    df[["Month","year"]] = df["MonthYear"].str.split(" ", expand=True)
    
    # Replacing unknown value from Column "Sex upon outcome" by NaN value to new "sex" column
    df["sex"] = df["Sex upon Outcome"].replace("Unknown", np.nan)

    # Dropping columns - "Sex upon outcome"
    df = df.drop(["Sex upon Outcome", "MonthYear"], axis = 1)

    return df

def load_data(data, target):
    # Exporting dataframe to csv file
    data.to_csv(target)

if __name__ == "__main__":

    source= "https://data.austintexas.gov/api/views/9t4d-g238/rows.csv"
    target = "Processed.csv"

    print("Starting...")
    df = extract_data(source)
    new_df = transform_data(df)
    load_data(new_df, target=target)
    
    print("Complete")
