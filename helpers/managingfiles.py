
# import external packages
import json
import pandas as pd


def enedis_json_to_df(data_raw):

    data_json = json.dumps(data_raw, indent=4)
    data = json.loads(data_json)
    df = pd.DataFrame(data["interval_reading"])

    return df


def df_to_csv(data, folder_to_save):

    data.to_csv(folder_to_save, index=False)

    pass


def excel_to_csv(file_to_open, file_to_save, sheet_name, columns_to_keep):

    df_temp = pd.read_excel(file_to_open, sheet_name)
    df_temp.to_csv(file_to_save, index=False, columns=columns_to_keep)

    pass
