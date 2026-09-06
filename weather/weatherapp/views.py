from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'delhi'
    API_KEY = 'AIzaSyC1mlzHPI7r_XvIb5ICSenVqpyxJhiRtz0'
    API_KEY = '89ebd02412b115e2ec896c711763ab7f'
    SEARCH_ENGINE_ID = '00aa8881f3bc04c16'
    # GOOGLE_API_KEY = 'AIzaSyC1mlzHPI7r_XvIb5ICSenVqpyxJhiRtz0'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'

    city_url = "https://www.googleapis.com/customsearch/v1"

    PARAMS = {
        'key': 'AIzaSyC1mlzHPI7r_XvIb5ICSenVqpyxJhiRtz0',
        'cx': '89ebd02412b115e2ec896c711763ab7f',
        'q': query,
        'start': start,
        'searchType': searchType
    }

    try:

        # Google Image Search API
        data = requests.get(city_url, params=PARAMS).json()

        search_items = data.get("items", [])

        if search_items:
            image_url = search_items[0]['link']
        else:
            image_url = ""

        # OpenWeather API
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'

        weather_params = {
            'units': 'metric'
        }

        weather_data = requests.get(
            url,
            params=weather_params
        ).json()

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']

        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception as e:

        messages.error(
            request,
            'Entered data is not available to API'
        )

        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': '',
            'icon': '',
            'temp': '',
            'day': day,
            'city': city,
            'exception_occurred': True,
            'image_url': 'image_url'
        })






    