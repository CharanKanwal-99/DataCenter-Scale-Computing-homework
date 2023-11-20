from etl_scripts.utils import load_object
from etl_scripts.utils import get_object
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def transform_data(**kwargs):

    # Copying the data
    date = kwargs['execution_date'].strftime('%Y-%m-%d')
    file = f'raw/{date}.csv'
    df = get_object(file)
    
    # Replacing unknown value from Column "Sex upon outcome" by NaN value to new "sex" column
    df["Sex"] = df["sex_upon_outcome"].replace("Unknown", np.nan)
    df['ID'] = df['animal_id']
    df['outcome'] = df['outcome_type']
    df['Animal'] = df['animal_type']
    df['Dt'] = df['datetime']
    df['recorded_name'] = df['name']
    
    cols_to_drop = ['outcome_type','animal_type','datetime','animal_id','name']
    df.drop(cols_to_drop,axis=1,inplace=True)

    # Transforming dataframe to match schema of warehouse
    date = (kwargs['execution_date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    print(date)
    file = f'processed/{date}_outcome.csv'
    df_outcome = get_object(file)
    
    df_outcome = check_for_updates(df,df_outcome,'outcome')
    df = df.merge(df_outcome)


    date = (kwargs['execution_date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    file = f'processed/{date}_animal.csv'
    df_animal = get_object(file)
    
    df_animal = check_for_updates(df,df_animal,'Animal')
    df = df.merge(df_animal)


    date = (kwargs['execution_date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    file = f'processed/{date}_breed.csv'
    df_breed = get_object(file)
    
    df_breed = check_for_updates(df,df_breed,'breed')
    df = df.merge(df_breed)


    date = (kwargs['execution_date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    file = f'processed/{date}_date.csv'
    df_date = get_object(file)
    
    df_date = check_for_updates(df,df_date,'Dt')
    df_date['Dt'] = pd.to_datetime(df_date['Dt'])
    df['Dt'] = pd.to_datetime(df['Dt'])
    df_date['Mnt'] = df_date['Dt'].dt.month
    df_date['Yr'] = df_date['Dt'].dt.year
    
    df = df.merge(df_date)
    
    # Retaining the useful columns
    cols = ['recorded_name','Dt_id','outcome_id','Animal_id','Sex','breed_id','color','ID']

    df = df[cols]
    
    date = kwargs['execution_date'].strftime('%Y-%m-%d')
    load_object(df, f'processed/{date}.csv')
    load_object(df_animal, f'processed/{date}_animal.csv')
    load_object(df_breed, f'processed/{date}_breed.csv')
    load_object(df_date, f'processed/{date}_date.csv')
    load_object(df_outcome, f'processed/{date}_outcome.csv')




def check_for_updates(df,df1,col):
    
    df2 = df[col].drop_duplicates().reset_index()
    df2[f'{col}_id'] = df2.index + 1
    df2.drop('index',axis=1,inplace=True)
    if len(df1) == 0:
        return df2

    new_values = df2.loc[~df2[col].isin(df1[col])]

    max_id = df1[f'{col}_id'].max()

    new_values[f'{col}_id'] = range(max_id + 1, max_id + 1 + len(new_values))

    df1 = df1.append(new_values, ignore_index=True)

    return df1

