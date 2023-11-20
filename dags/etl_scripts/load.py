import os
from sqlalchemy import create_engine
from etl_scripts.utils import get_object
from db.connection import warehouse_connection
from datetime import datetime

def load_data():
    
    warehouse_connection()
    db_url = os.getenv('db_url')
    #engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')
    engine = create_engine(db_url)
    
    date = datetime.now().date()
    df = get_object(f'processed/{date}.csv')
    df_animal = get_object(f'processed/{date}_animal.csv')
    df_date = get_object(f'processed/{date}_date.csv')
    df_outcome = get_object(f'processed/{date}_outcome.csv')
    df_breed = get_object(f'processed/{date}_breed.csv')
    

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
    

    df.to_sql(name= 'ADOPTION',con=engine, if_exists='append',index=False,dtype=df_schema)
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