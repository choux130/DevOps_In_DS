# %%
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.Entities as ent
import src.s01_LoadDataFromDB as ld
import src.s02_DataPreprocessing as dp


# %%
@ent.DebugDecorator
def SplitDataToTrainAndTest(df:pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    dv = ent.DefaultValues()
    df_train = df.sample(frac=dv.FRAC_TEST_DATASET,random_state=dv.RANDOMSEED)
    df_test = df.drop(df_train.index)

    return df_train, df_test

# %% 
if __name__ == '__main__':

    df_db = ld.LoadCompleteDataFromDB()
    
    df_clean = (df_db
        .pipe(dp.DropDuplicatedData)
        .pipe(dp.DataSchemeCheckAndCorrectForDBData)
    )

    df_train, df_test = SplitDataToTrainAndTest(df_clean)

