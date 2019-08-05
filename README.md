# TwitWeather

This is a small Twitter bot that tweets a weather forecast each morning. 

The project is based in part on [williamsmj's dwx](https://github.com/williamsmj/dwx) and uses the [Dark Sky API](https://darksky.net/dev) for weather info. The purpose of this project was to learn more about Zappa while creating something useful. 

Check out the live Twitter bot at [TwitWeatherAKL](https://twitter.com/TwitWeatherAKL).


<blockquote class="twitter-tweet"><p lang="und" dir="ltr">🌚🌚⛅⛅⛅⛅⛅⛅⛅⛅⛅⛅🌚🌚🌚🌚🌚 🌡13</p>&mdash; TwitWeatherAKL (@TwitWeatherAKL) <a href="https://twitter.com/TwitWeatherAKL/status/1158437670927790081?ref_src=twsrc%5Etfw">August 5, 2019</a></blockquote>



# Installation

Follow these steps to get up and running with your own version of TwitWeather deployed to AWS Lambda:
1. Create a virtual env for the project `mkproject twitweather`
2. Clone this repo `git clone https://github.com/aell039/TwitWeather .`
3. Install required libraries `pip install pytz requests zappa tweepy`
4. Initialise Zappa `zappa init`
5. Modify your `zappa_settings.json` to use your own API keys, location, and AWS settings:
    ```json
    {
        "dev": {
            "profile_name": "default",
            "project_name": "twitweather",
            "runtime": "python3.6",
            "s3_bucket": "your-s3-bucket",
            "aws_region": "ap-southeast-2",
            "events": [{
                "function": "twitweather.check_time_and_post",
                "expression": "cron(0 * * * ? *)"
             }],
             "environment_variables": {
                "DS_KEY": "your-dark-sky-key",
                "TW_CONSUMERKEY": "your-twitter-consumer-key",
                "TW_CONSUMERKEYSECRET": "your-twitter-consumer-secret",
                "TW_ACCESSTOKEN": "your-twitter-access-token",
                "TW_ACCESSTOKENSECRET": "your-twitter-secret",
                "LATITUDE": "-36.852501",
                "LONGITUDE": "174.763081",
                "LOCAL_TZ": "Pacific/Auckland"           
            }
        }
    }
    ```
   Note: an AWS region must be set even though Zappa does not include it by default.

6. Deploy! `zappa deploy dev`

⚡⚡⚡
