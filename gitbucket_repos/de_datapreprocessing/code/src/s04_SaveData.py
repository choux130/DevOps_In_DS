# %%
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.Entities as ent
import src.s01_LoadDataFromDB as ld
import src.s02_DataPreprocessing as dp
import src.s03_SplitData as spd

# %%
def SaveDataAsCSVFile(df:pd.DataFrame, file_name:str):

    dv = ent.DefaultValues()
    proj_dir = dv.PROJECT_DIR
    data_foldername = dv.DATA_FOLDERNAME

    full_file_path = os.path.join(proj_dir, data_foldername, file_name)
    if not os.path.exists(os.path.dirname(full_file_path)):
        os.makedirs(os.path.dirname(full_file_path))

    df.to_csv(full_file_path, index=False)

@ent.DebugDecorator
def SaveAllData(df_all: dict[str, pd.DataFrame]):

    SaveDataAsCSVFile(df_all['df_db'], "raw/df_raw_from_db.csv")
    SaveDataAsCSVFile(df_all['df_clean'], "interim/df_preprocessing.csv")
    SaveDataAsCSVFile(df_all['df_train'], "processed/df_train.csv")
    SaveDataAsCSVFile(df_all['df_train'], "processed/df_test.csv")


# %% 
if __name__ == '__main__':

    df_db = ld.LoadCompleteDataFromDB()
    df_clean = (df_db
        .pipe(dp.DropDuplicatedData)
        .pipe(dp.DataSchemeCheckAndCorrectForDBData)
    )
    df_train, df_test = spd.SplitDataToTrainAndTest(df_clean)

    df_all = {'df_db': df_db, 'df_clean': df_clean, 'df_train': df_train, 'df_test': df_test}
    SaveAllData(df_all)
