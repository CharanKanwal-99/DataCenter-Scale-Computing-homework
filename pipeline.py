import pandas as pd
import numpy as np
from dataclasses import dataclass
import os
from sqlalchemy import create_engine
from sqlalchemy.types import *

@dataclass
class DBConnection():
    user:str
    password:str
    db:str
    host:str
    port:int=5432


def get_credentials():
    user = os.getenv('WAREHOUSE_USER')
    password = os.getenv('WAREHOUSE_PASSWORD')
    db = os.getenv('WAREHOUSE_DB')
    host = os.getenv('WAREHOUSE_HOST')
    port = os.getenv('WAREHOUSE_PORT')
    return DBConnection(user,password,db,host,port)

def connection_string(dbconn:DBConnection):
    conn_url = f"postgresql+psycopg2://{dbconn.user}:{dbconn.password}@{dbconn.host}:{dbconn.port}/{dbconn.db}"
    return conn_url



    
def extract_data(source):
     
    # Reading csv file
    return pd.read_csv(source)
 

def transform_data(data):

    # Copying the data
    df = data.copy()
    
    # Replacing unknown value from Column "Sex upon outcome" by NaN value to new "sex" column
    df["Sex"] = df["Sex upon Outcome"].replace("Unknown", np.nan)
    df['ID'] = df['Animal ID']
    df['outcome'] = df['Outcome Type']
    df['Animal'] = df['Animal Type']
    df['Dt'] = df['DateTime']
    df['recorded_name'] = df['Name']
    
    cols_to_drop = ['Outcome Type','Animal Type','DateTime','Animal ID','Name']
    df.drop(cols_to_drop,axis=1,inplace=True)


    # Transforming dataframe to match schema of warehouse

    df_outcome = df['outcome'].drop_duplicates().reset_index()
    df_outcome['outcome_id'] = df_outcome.index + 1
    df_outcome.drop('index',axis=1,inplace=True)
    df = df.merge(df_outcome)

    df_animal = df['Animal'].drop_duplicates().reset_index()
    df_animal['Animal_id'] = df_animal.index + 1
    df_animal.drop('index',axis=1,inplace=True)
    df = df.merge(df_animal)

    df_breed = df['Breed'].drop_duplicates().reset_index()
    df_breed['Breed_id'] = df_breed.index + 1
    df_breed.drop('index',axis=1,inplace=True)
    df = df.merge(df_breed)



    df_date = df['Dt'].drop_duplicates().reset_index()
    df_date['date_id'] = df_date.index + 1
    df_date.drop('index',axis=1,inplace=True)
    df_date['Dt'] = pd.to_datetime(df_date['Dt'])
    df['Dt'] = pd.to_datetime(df['Dt'])
    df_date['Mnt'] = df_date['Dt'].dt.month
    df_date['Yr'] = df_date['Dt'].dt.year

    df = df.merge(df_date)
    
    # Retaining the useful columns
    cols = ['recorded_name','date_id','outcome_id','Animal_id','Sex','Breed_id','Color','ID']

    df = df[cols]
    
    return df, df_animal,df_date,df_outcome,df_breed





def load_data(db_url, df, df_animal, df_date,df_outcome,df_breed):
    engine = create_engine(db_url)
    df_schema = {
    "recorded_name": String,    
    "date_id": Integer,
    "outcome_id": Integer,
    "Animal_id": Integer,
    "Sex": String,
    "Breed_id": Integer,
    "Color": String,
    "ID": String
     }
    

    df.to_sql(name= 'ADOPTION',con=engine, if_exists='replace',index=False,dtype=df_schema)
    animal_schema = {
        "Animal": String,
        "Animal_id":Integer
    }
    df_animal.to_sql(name='ANIMAL',con=engine, if_exists='replace',index=False,dtype=animal_schema)
    outcome_schema = {
        "outcome":String,
        "outcome_id":Integer
    }
    df_outcome.to_sql(name='OUTCOME',con=engine, if_exists='replace',index=False,dtype=outcome_schema)
    breed_schema = {
        "Breed":String,
        "Breed_id":Integer
    }
    df_breed.to_sql(name='BREED',con=engine, if_exists='replace',index=False,dtype=breed_schema)
    date_schema = {
        "Dt":DateTime,
        "date_id":Integer,
        "Mnt":Integer,
        "Yr":Integer
    }
    df_date.to_sql(name='DATE',con=engine, if_exists='replace',index=False,dtype=date_schema)
    

def run():
    source= "https://data.austintexas.gov/api/views/9t4d-g238/rows.csv"

    print("Starting...")
    df = extract_data(source)
    new_df,df_animal, df_date,df_outcome,df_breed = transform_data(df)
    dbconn = get_credentials()
    url = connection_string(dbconn)
    load_data(url, new_df,df_animal, df_date, df_outcome,df_breed)
    
    print("Complete")

if __name__ == "__main__" :
    run()