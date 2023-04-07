
# %%
import os
import sys
import pandas as pd
import pandera as pa

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.Entities as ent
import src.s01_LoadDataFromDB as ld

# %%
@ent.DebugDecorator
def DropDuplicatedData(df: pd.DataFrame) -> pd.DataFrame:

    df_after = df.drop_duplicates()

    return df_after


def DataSchemeCheckAndRemoveInavlidRows(scheme: pa.api.pandas.container.DataFrameSchema, df: pd.DataFrame) -> pd.DataFrame:

    try:
        scheme.validate(df, lazy=True)
        df_clean = df
    
    except pa.errors.SchemaErrors as err:
        # print(err.failure_cases)  # dataframe of schema errors
        # print(err.data)  # invalid dataframe
        df_clean = df[~df.index.isin(err.failure_cases["index"])] 

    return df_clean

@ent.DebugDecorator
def DataSchemeCheckAndCorrectForDBData(df: pd.DataFrame) -> pd.DataFrame:

    scheme = ent.DataFrameScheme_DataFromDB()
    df_clean = DataSchemeCheckAndRemoveInavlidRows(scheme, df)

    return df_clean

# %%
if __name__ == '__main__':

    df_db = ld.LoadCompleteDataFromDB()
    
    df_clean = (df_db
        .pipe(DropDuplicatedData)
        .pipe(DataSchemeCheckAndCorrectForDBData)
    )



    