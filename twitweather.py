import os
import datetime
import pytz
import requests
import tweepy

ds_key = os.environ['DS_KEY']
ds_url = 'https://api.darksky.net/forecast'
ds_apiparams = {'exclude': 'alerts,currently,minutely', 'units': 'ca'}
post_time = datetime.time(6, 00)  # 6am local time
post_time_tol_seconds = 5 * 60
forecast_from = datetime.time(6, 00)  # 6am local time
forecast_to = datetime.time(23, 00)  # 11pm local time

emoji = {
    "clear-day": "\U00002600",
    "clear-night": "\U0001F30C",
    "rain": "\U0001F327",
    "snow": "\U00002744",
    "sleet": "\U0001F328",
    "wind": "\U0001F32C",
    "fog": "\U0001F32B",
    "cloudy": "\U00002601",
    "partly-cloudy-day": "\U000026C5",
    "partly-cloudy-night": "\U0001F318"
}


def local_tz():
    return pytz.timezone(os.environ['LOCAL_TZ'])


def get_times():
    """Return time in server timezone, local time in location timezone, and
    target post_time in location timezone."""
    server = datetime.datetime.now().astimezone()
    local = server.astimezone(local_tz())
    target = local.replace(hour=post_time.hour,
                            minute=post_time.minute,
                            second=0, microsecond=0)
    forecast_lower = local.replace(hour=forecast_from.hour,
                            minute=forecast_from.minute,
                            second=0, microsecond=0)
    forecast_upper = local.replace(hour=forecast_to.hour,
                            minute=forecast_to.minute,
                            second=0, microsecond=0)

    return {'server': server, 'local': local, 'target': target,
     'forecast_lower': forecast_lower, 'forecast_upper': forecast_upper}


def check_time():
    """Return True if within post_time_tol_seconds of post_time in timezone of
    location."""
    times = get_times()
    time_difference = abs((times['local'] - times['target']).total_seconds())
    return time_difference < post_time_tol_seconds


def get_wx():
    date = datetime.datetime.now()
    url_args = [os.environ['LATITUDE'],
                os.environ['LONGITUDE'],
                str(round(date.timestamp()))]
    url = f"{ds_url}/{ds_key}/{','.join(url_args)}"
    wx = requests.get(url, params=ds_apiparams).json()
    return wx


def describe_wx():
    wx = get_wx()
    times = get_times()
    forecast_lower_utc = times['forecast_lower'].timestamp()
    forecast_upper_utc = times['forecast_upper'].timestamp()
    forecast = []

    for hour in wx['hourly']['data']:
        if hour['time'] >= forecast_lower_utc and hour['time'] <= forecast_upper_utc:
            print(hour['time'], hour['icon'])
            forecast.append(hour['icon'])
    
    print(forecast)
    forecast = [ emoji.get(item,item) for item in forecast ]
    
    # insert breaks in list to help with readability
    forecast[12:12] = ["  "]
    forecast[6:6] = ["  "]

    forecast = "".join(forecast)
    hi_temp = wx['daily']['data'][0]['temperatureHigh']
    hi_temp = " \U0001F321" + str(round(hi_temp))
    forecast = forecast + hi_temp
    return forecast


def make_api():
    auth = tweepy.OAuthHandler(os.environ['TW_CONSUMERKEY'],
                               os.environ['TW_CONSUMERKEYSECRET'])
    auth.set_access_token(os.environ['TW_ACCESSTOKEN'],
                          os.environ['TW_ACCESSTOKENSECRET'])
    return tweepy.API(auth)


def post(tweet):
    api = make_api()
    api.update_status(tweet)


def check_time_and_post():
    if check_time():
        tweet = describe_wx()
        post(tweet)
    else:
        print(str(datetime.datetime.now().astimezone(local_tz())) + 'Not time yet.')

if __name__ == '__main__':
    print(describe_wx())
