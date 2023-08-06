import requests


class Weather:
    """
    The object of this class can be initialized by
        (i) providing a valid city
        (ii) providing valid latitude and longitude

    The data is provided by the https://openweathermap.org/ api
    Create your own account and get an api
    wait few hours for the api to get activated
    example for making object is shown below
        weather = Weather(api="<your api key>","chicago")
        weather1 = Weather(api="<your api key>",lat=30.5, long=32.5)

    you have two methods
        weather_object.next_12h returns a dictionary of weather for next 12 hours
        weather_object.next_12h_simplified returns a list of 4 3 hour updates on date-time, temperature, weather conditions, icon
    """

    def __init__(self, city=None, api="e09e6a792ec6636cd1b9f882e1a71f81", lat=None, long=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}&units=metric"
            content = requests.get(url)
            self.data = content.json()
        elif lat and long:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api}&units=metric"
            content = requests.get(url)
            self.data = content.json()
        else:
            raise TypeError("You did not enter any location details")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """
        weather_object.next_12h has data['list'][:4]
        :return: a dictionary of weather for next 12 hours
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """
        weather_object.next_12h_simplified list of (dict['dt_txt'],dict['main']['temp'],dict['weather'][0]['description']
        :return:a list of 4 3 hour updates on date-time, temperature, weather conditions
        """
        simple_data = []
        for dict in self.data['list'][:4]:
            simple_data.append((dict['dt_txt'], dict['main']['temp'], dict['weather'][0]['description'],dict['weather'][0]['icon']))
        return simple_data


