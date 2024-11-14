
# import external packages
import pandas as pd
import os


def compiling_raspberry_files_in_folder(folder_path_to_read, folder_path_to_save, encoding=None):

    # Compile files with same name's start in few files
    visible_files = list_of_files_in_folder(folder_path_to_read)

    cat = files_with_similar_names(folder_path_to_read)

    for ind, ele in enumerate(cat):

        list_temp_1 = []
        files = [file for file in visible_files if file.startswith(ele)]

        # Looping through all the files to make a list of dataframes
        for index, element in enumerate(files):
            df_temp_1 = pd.read_csv(folder_path_to_read + element, encoding=encoding, header="infer")
            list_temp_1.append(df_temp_1)

        # Concatenating all dataframes together
        try:
            df_temp_2 = pd.concat(list_temp_1)
        except Exception:
            df_temp_2 = list_temp_1[0]
            pass
        # Drop duplicates
        df_temp_2.drop_duplicates(inplace=True)
        # Reset index
        df_temp_2.reset_index(drop=True, inplace=True)
        df_temp_2.to_csv(folder_path_to_save + ele + '.csv', index=False)

    pass


def compiling_enedis_files_in_folder(folder_path_to_read, folder_path_to_save, encoding=None):

    # Compile files with same name's start in few files
    visible_files = list_of_files_in_folder(folder_path_to_read)

    cat = files_with_similar_names(folder_path_to_read)

    list_temp_1 = []  # Hourly consumption datas
    list_temp_2 = []  # Pmax datas
    list_temp_3 = []  # Daily consumption datas

    for ind, ele in enumerate(cat):

        files = [file for file in visible_files if file.startswith(ele)]

        if ele.startswith('Enedis_Conso_Jour'):
            continue

        elif ele.startswith('consumption_load_curve'):
            for index, element in enumerate(files):
                df_temp_1 = pd.read_csv(folder_path_to_read + element, header="infer")
                list_temp_1.append(df_temp_1)

        elif ele.startswith('consumption_max_power'):
            for index, element in enumerate(files):
                df_temp_2 = pd.read_csv(folder_path_to_read + element, header="infer")
                list_temp_2.append(df_temp_2)

        elif ele.startswith('daily_consumption'):
            for index, element in enumerate(files):
                df_temp_3 = pd.read_csv(folder_path_to_read + element, header="infer")
                list_temp_3.append(df_temp_3)

        elif ele.startswith('Enedis_Conso_Heure'):
            # Looping through all the files to make a list of dataframes
            for index, element in enumerate(files):
                df_temp_1 = pd.read_csv(folder_path_to_read + element, delimiter=';', header=2)
                df_temp_1 = df_temp_1.rename(columns={'Horodate': "date", 'Valeur': 'value'}, errors="raise")
                df_temp_1['date'] = pd.to_datetime(df_temp_1['date'], format='mixed', utc=True)
                df_temp_1.sort_values('date', inplace=True)
                df_temp_1 = df_temp_1[['value', 'date']]

                diff = df_temp_1['date'][1] - df_temp_1['date'][0]
                if diff.value == 1800000000000:
                    df_temp_1['interval_length'] = 'PT30M'
                    df_temp_1['measure_type'] = 'B'
                elif diff.value == 1800000000000 * 2:
                    df_temp_1['interval_length'] = 'PT60M'
                    df_temp_1['measure_type'] = 'B'

                df_temp_1['date'] = pd.to_datetime(df_temp_1['date'], format='mixed', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')

                list_temp_1.append(df_temp_1)

        elif ele.startswith('Enedis_Conso_Pmax'):
            # Looping through all the files to make a list of dataframes
            for index, element in enumerate(files):
                df_temp_2 = pd.read_csv(folder_path_to_read + element, delimiter=';', header=2)
                df_temp_2 = df_temp_2.rename(columns={'Horodate': "date", 'Valeur': 'value'}, errors="raise")
                df_temp_2['date'] = pd.to_datetime(df_temp_2['date'], format='mixed', utc=True)
                df_temp_2.sort_values('date', inplace=True)
                df_temp_2 = df_temp_2[['value', 'date']]

                df_temp_2['date'] = pd.to_datetime(df_temp_2['date'], format='mixed', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
                list_temp_2 .append(df_temp_2)

    # Concatenating Hourly consumption datas
    try:
        df_temp_1 = pd.concat(list_temp_1)
    except Exception:
        df_temp_1 = list_temp_1[0]
        pass
    # Drop duplicates
    df_temp_1.drop_duplicates(inplace=True)
    df_temp_1.sort_values('date', inplace=True)
    # Reset index
    df_temp_1.reset_index(drop=True, inplace=True)
    df_temp_1.to_csv(folder_path_to_save + 'consumption_load_curve' + '.csv', index=False)

    # Concatenating Pmax datas
    try:
        df_temp_2 = pd.concat(list_temp_2)
    except Exception:
        df_temp_2 = list_temp_2[0]
        pass
    # Drop duplicates
    df_temp_2.drop_duplicates(inplace=True)
    df_temp_2.sort_values('date', inplace=True)
    # Reset index
    df_temp_2.reset_index(drop=True, inplace=True)
    df_temp_2.to_csv(folder_path_to_save + 'consumption_max_power' + '.csv', index=False)

    # Concatenating Daily consumption datas
    try:
        df_temp_3 = pd.concat(list_temp_3)
    except Exception:
        df_temp_3 = list_temp_1[0]
        pass
    # Drop duplicates
    df_temp_3.drop_duplicates(inplace=True)
    df_temp_3.sort_values('date', inplace=True)
    # Reset index
    df_temp_3.reset_index(drop=True, inplace=True)
    df_temp_3.to_csv(folder_path_to_save + 'daily_consumption' + '.csv', index=False)
    pass


def files_with_similar_names(folder_path):

    visible_files = list_of_files_in_folder(folder_path)

    file_names = []
    debut = 'c'
    longueur = 0
    for index, element in enumerate(visible_files):
        if element[0:longueur - 1] == debut:
            continue
        else:
            debut = 'c'
            longueur = 0
            for i, j in enumerate(element):
                try:
                    if type(int(j)) == int:
                        longueur = i
                        debut = element[0:longueur - 1]
                        break
                except Exception:
                    continue
            file_names.append(debut)
    return file_names


def list_of_files_in_folder(folder_path):

    # Getting the list of all the files in the directory
    file_list = os.listdir(folder_path)
    # Filtering it only to visible files (not starting with ".") and .csv files
    file_list = [file for file in file_list if (not file.startswith('.'))]
    file_list.sort(key=str.casefold)

    return file_list
