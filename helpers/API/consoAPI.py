
# import librairies
import requests


class ConsoAPI():
    """This class manages the communication with conso API

    Args :

    """

    def __init__(self, url, prm, token):

        self.url = url
        self.prm = prm
        self.token = token

        pass

    def get(self, data_type, start_date, end_date):

        api_url = self.url + data_type + "?prm=" + self.prm + "&start=" + start_date + "&end=" + end_date
        self.headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get(api_url, headers=self.headers)
        return response.json()

    def get_daily_consumption(self, start_date, end_date):

        data_type = "daily_consumption"
        return self.get(data_type, start_date, end_date)

    def get_consumption_load_curve(self, start_date, end_date):

        data_type = "consumption_load_curve"
        return self.get(data_type, start_date, end_date)

    def get_consumption_max_power(self, start_date, end_date):

        data_type = "consumption_max_power"
        return self.get(data_type, start_date, end_date)
