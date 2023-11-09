import datetime

from bs4 import BeautifulSoup
import requests

from . import models


# currently gets description for three closest days, including today
# but weather is for 5 days
def get_weather():
    """
    :return: dict[date] = (temperature: str, description:str)]
    """

    print('service started')
    def get_description(url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        bs = BeautifulSoup(response.text, features="html.parser")

        # getting weather details for this day
        today_info = bs.find("div", class_="wrapper city__main-info") \
            .find("div", class_="city__main-info") \
            .find("span", class_="city__main-image-descr") \
            .find_all("span")

        description_today = ""
        for elem in today_info:
            description_today += str.capitalize(elem.text) + " "

        return description_today

    # getting web page
    url = 'https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, features="html.parser")

    # selecting necessary elements with weather in it
    today_elem = bs.find_all("div", class_="city__day fl-col active")
    next_days_elem = bs.find_all("div", class_="city__day fl-col")
    list_to_parse = today_elem + next_days_elem

    # updating or creating data for a week
    for i, elem in enumerate(list_to_parse):
        day_element = elem['id']
        date = datetime.date.fromisoformat(day_element)

        # parsing temperature for this date
        temperature = int(elem.find("div", class_="city__day-temperature").find("span").text[1:-1])

        # today

        def update_weather(date, temperature, description_link="https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/"):

            if description_link:
                description = get_description(description_link)
            else:
                description = ""

            # if created, fills table with default values
            d, created = models.KyivWeather.objects.get_or_create(date=date,
                                                                  defaults={
                                                                      'description': description,
                                                                      'temperature': temperature}
                                                                  )
            # else automatic assignment
            if not created:
                # updating
                d.temperature = temperature
                d.description = description

            d.save(force_update=True)

        if i == 0:
            update_weather(date, temperature)
        # tomorrow
        elif i == 1:
            update_weather(date, temperature, "https://pogoda.meta.ua/ua/Kyivska/Kyivskiy/Kyiv/tomorrow")
        # other days - no static link for description
        else:
            update_weather(date, temperature, "")

    return None

