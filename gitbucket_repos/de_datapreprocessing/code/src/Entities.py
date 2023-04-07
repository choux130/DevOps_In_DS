# %%
import os
from typing import NamedTuple
import datetime
import pandas as pd
import pandera as pa


# %%
class DefaultValues(NamedTuple):
    MYSQL_DATA_HOST = "mysql"
    MYSQL_DATA_PORT = 3306
    MYSQL_DATA_USER = os.environ.get("MYSQL_USR")
    MYSQL_DATA_PASSWORD = os.environ.get("MYSQL_PWD")
    MYSQL_DATA_DATABASE = "world"
    SQLQuery_CallProc_DataPreprocessing = "CALL DataPreprocessing();"

    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_FOLDERNAME = "data"
    FRAC_TEST_DATASET = 0.2
    RANDOMSEED = 123

def DataFrameScheme_DataFromDB():
    current_year = datetime.date.today().year

    scheme = pa.DataFrameSchema({
        "Code": pa.Column(str, nullable=False, coerce=True), 
        "Name": pa.Column(str, nullable=False, coerce=True), 
        "Region": pa.Column(str, nullable=False, coerce=True), 
        "SurfaceArea": pa.Column(str, nullable=False, coerce=True), 
        "IndepYear": pa.Column(int, pa.Check(lambda x: 0 < x <= current_year), nullable=True, coerce=True),
        "Population": pa.Column(int, pa.Check(lambda x: x > 0), nullable=True, coerce=True),
        "LifeExpectancy": pa.Column(float, pa.Check(lambda x: x > 0), nullable=True, coerce=True), 
        "GovernmentForm": pa.Column(str, nullable=False, coerce=True), 
        "CityName_highest_population": pa.Column(str, nullable=False, coerce=True), 
        "CityDistrict_highest_population": pa.Column(str, nullable=False, coerce=True), 
        "CityPopulation_highest": pa.Column(int, pa.Check(lambda x: x > 0), nullable=False, coerce=True), 
        "OfficialLanguage": pa.Column(str, nullable=False, coerce=True),
        "OfficialLanguage_percentage": pa.Column(float, pa.Check(lambda x: x >= 0), nullable=False, coerce=True),
        "GNP": pa.Column(int, pa.Check(lambda x: x >= 0), nullable=False, coerce=True), 
    })

    return scheme

def DebugDecorator(func):

    def wrapper(*args, **kwargs):
        
        func_name = func.__name__
        print(f"[{datetime.datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S')} UTC][Start] {func_name}()")
        result = func(*args, **kwargs)
        
        info_msg = ">>>>> Dimension of the output dataframe:"
        if isinstance(result, pd.DataFrame):
            print(f'{info_msg} {result.shape}')
        elif isinstance(result, tuple):
            for idx, k in enumerate(result):
                if isinstance(k, pd.DataFrame):
                    print(f'({idx+1} item in the tuple) {info_msg} {k.shape}')
    
        print(f"[{datetime.datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S')} UTC][End]   {func_name}()")

        return result

    return wrapper    