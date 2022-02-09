from flask import current_app
import requests


def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        'q': city_name,
        'appid': current_app.config['WEATHER_API_KEY'],
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if 'main' in weather:
            weather['main']['temp'] = round(weather['main']['temp'])
            weather['main']['feels_like'] = round(weather['main']['feels_like'])
            return weather['main']
    except(requests.RequestException, ValueError, TypeError):
        print('Сетевая ошибка')
        return False
    return False


if __name__ == '__main__':
    print(weather_by_city('Moscow,Russia'))
