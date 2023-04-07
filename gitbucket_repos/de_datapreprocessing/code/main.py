# %%
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import src.Entities as ent
import src.s01_LoadDataFromDB as ld
import src.s02_DataPreprocessing as dp
import src.s03_SplitData as spd
import src.s04_SaveData as sd

# %%
if __name__ == "__main__":

    df_db = ld.LoadCompleteDataFromDB()
    df_clean = (df_db
        .pipe(dp.DropDuplicatedData)
        .pipe(dp.DataSchemeCheckAndCorrectForDBData)
    )
    df_train, df_test = spd.SplitDataToTrainAndTest(df_clean)

    df_all = {'df_db': df_db, 'df_clean': df_clean, 'df_train': df_train, 'df_test': df_test}
    sd.SaveAllData(df_all)
