# %%
import os
import sys
import pandas as pd
from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.Entities as ent

# %%

def GetMySQLAddress():
    
    dv = ent.DefaultValues()
    address = (
        f"mysql+pymysql://{dv.MYSQL_DATA_USER}:{dv.MYSQL_DATA_PASSWORD}"
        f"@{dv.MYSQL_DATA_HOST}:{dv.MYSQL_DATA_PORT}/{dv.MYSQL_DATA_DATABASE}"
    )
    # print(address)

    return address


def GetMySQLConnect():
    address = GetMySQLAddress()
    engine = create_engine(address)
    mysql_conn = engine.connect()

    return mysql_conn


def RunGetQueryAgainstMySQL(query: str) -> pd.DataFrame: 
    
    mysql_conn = GetMySQLConnect()
    df = pd.read_sql_query(query, mysql_conn)
    mysql_conn.close()

    return df

ent.DebugDecorator
def LoadCompleteDataFromDB() -> pd.DataFrame:

    dv = ent.DefaultValues()
    query = dv.SQLQuery_CallProc_DataPreprocessing

    df = RunGetQueryAgainstMySQL(query)

    return df

# %%
if __name__ == '__main__':

    df = LoadCompleteDataFromDB()
    # df.head()
