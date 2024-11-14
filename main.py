"""Entry point."""

# import external packages
from datetime import datetime, timedelta
import warnings


# import project packages
import helpers.datas as datas # store links, directories and personnal datas

# ignore Warning
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')


def raspberry_sequence():
    from helpers.managingraspberry import Raspberry

    # SEQUENCE RASPBERRY REGARDING TEMPERATURE
    # Initialise the raspberry class in order to use ssh and scp
    rasp = Raspberry(datas.server, datas.port, datas.user, datas.password)
    # Check if python script is running
    stdout = rasp.execute_command(datas.rasp_python_running, 2)
    print(stdout.read().decode('utf-8'))
    # Kill python scripts running
    # rasp.execute_command(datas.rasp_kill_python)
    # Download the temperature file in database
    rasp.download_file(datas.rasp_database_folder_path, datas.rasp_temperature_file, datas.temperatures_raspberry_folder_path,
                       "temperatures_raspberry " + datetime.now(tz=None).isoformat(' ', "seconds") + ".csv")
    # Download the temperature file in backup database
    rasp.download_file(datas.rasp_database_folder_path, datas.rasp_temperature_file,
                       datas.local_rasp_backup_temeperatures_folder,
                       "temperatures_raspberry " + datetime.now(tz=None).isoformat(' ', "seconds") + ".csv")
    # Replace the temperature file by an empty one
    rasp.upload_file(datas.rasp_database_folder_path, datas.local_temperature_file, datas.local_rasp_folder_path)
    # Download the log file
    rasp.download_file(datas.rasp_database_folder_path, datas.rasp_log_file, datas.local_log_folder,
                       "log_raspberry " + datetime.now(tz=None).isoformat(' ', "seconds") + ".csv")
    # Replace the log file by an empty one
    rasp.upload_file(datas.rasp_database_folder_path, "log_raspberry.csv", datas.local_rasp_folder_path)
    # Upload new python scripts
    # rasp.upload_folder("/home/pi/python/", datas.local_rasp_scripts_folder_path)
    # Run the main python script on Raspberry
    # rasp.execute_command(datas.rasp_start_python + datas.rasp_python_folder_path + datas.rasp_python_main + datas.rasp_python_capture)
    # Make sure the python script is running
    stdout = rasp.execute_command(datas.rasp_python_running, 2)
    print(stdout.read().decode('utf-8'))
    # Close connection with Raspberry
    rasp.close_connection()
    pass


def call_conso_api_sequence():
    from helpers.API.consoAPI import ConsoAPI
    import helpers.managingfiles as managingfiles
    # Call APIs only if no update has been done today
    if datas.last_update_date != datetime.now(tz=None).strftime("%Y-%m-%d"):

        # SEQUENCE conso API ~ data from ENEDIS
        # Initialise the consoapi class
        consoapi = ConsoAPI(datas.conso_api_url, datas.prm, datas.conso_api_token)

        # Get daily consumption
        data_raw = consoapi.get_daily_consumption(datas.last_update_date, datetime.now(tz=None).strftime("%Y-%m-%d"))
        df = managingfiles.enedis_json_to_df(data_raw)
        managingfiles.df_to_csv(df, datas.consumption_ENEDIS_folder_path + 'daily_consumption_' + datetime.now(tz=None).strftime("%Y-%m-%d") + '.csv')

        if datetime.now(tz=None) - datetime.strptime(datas.last_update_date, '%Y-%m-%d') <= timedelta(days=7):
            # Get consumption_load_curve AKA hourly consumption
            data_raw = consoapi.get_consumption_load_curve(datas.last_update_date, datetime.now(tz=None).strftime("%Y-%m-%d"))
            df = managingfiles.enedis_json_to_df(data_raw)
            df.to_csv(datas.consumption_ENEDIS_folder_path + 'consumption_load_curve_' + datetime.now(tz=None).strftime("%Y-%m-%d") + '.csv', encoding='utf-8', index=False)
        else:
            print("Period of time longer as 7 days, no call for hourly consumption.")
        # Get consumption_max_power
        data_raw = consoapi.get_consumption_max_power(datas.last_update_date, datetime.now(tz=None).strftime("%Y-%m-%d"))
        df = managingfiles.enedis_json_to_df(data_raw)
        df.to_csv(datas.consumption_ENEDIS_folder_path + 'consumption_max_power_' + datetime.now(tz=None).strftime("%Y-%m-%d") + '.csv', encoding='utf-8', index=False)

        # Update the last update date in datas file
        with open("helpers/datas.py", "r") as file:
            data = file.read()
            data = data.replace(datas.last_update_date, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
        with open("helpers/datas.py", "w") as file:
            file.write(data)
        print("Has been updated.")

    else:
        print("No need to call APIs, already up to date.")
    pass


def compiling_datas():
    # COMPILING THE DATABASE FILES
    import helpers.compiling_files as compiling_files
    import helpers.managingfiles as managingfiles

    # Raspberry
    compiling_files.compiling_raspberry_files_in_folder(datas.temperatures_raspberry_folder_path, datas.database_folder_path)
    # ENEDIS
    compiling_files.compiling_enedis_files_in_folder(datas.consumption_ENEDIS_folder_path, datas.database_folder_path)

    # Daily status from Calcul EDF
    managingfiles.excel_to_csv(datas.consumption_EDF_folder_path + "Calcul EDF.xlsx",
                               datas.database_folder_path + "daily_status.csv", "mes-index-elec",
                               ["date", "accumulateur", "chauffage", "presence", "new windows", "day", "cout"])

    pass


def main():

    # SEQUENCE RASPBERRY
    raspberry_sequence()

    # CALL CONSO API
    call_conso_api_sequence()

    # CALL COMPILING FUNCTION
    compiling_datas()

    print("Done.")
    pass


if __name__ == "__main__":
    main()
