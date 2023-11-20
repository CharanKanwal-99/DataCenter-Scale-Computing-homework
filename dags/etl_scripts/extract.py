import requests
import pandas as pd
from etl_scripts.utils import load_object
from datetime import datetime


def extract_data(**kwargs):
    #date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:10]
    date = kwargs['execution_date'].strftime('%Y-%m-%d')
    url = f"https://data.austintexas.gov/resource/9t4d-g238.json?$where=datetime between '{date}T00:00:00.000' and '{date}T23:59:59.999'"
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    path = f'raw/{date}.csv'
    load_object(df,path)








