from twilio.rest import Client
import re
import json
import time
import twitter
import twilio
import os

DCFC_ACCOUNT = {
        'id': '412519173',
        'screen_name': 'DetroitCityFC'
        }
BREW_ACCOUNT = {
        'id': '1405616368859463692',
        'screen_name': 'DetroitBrew'
        }



def main():
    with open('twitter.json') as f:
        keys = json.load(f)

    with open('twilio.json') as f:
        twilio = json.load(f)

    with open('phones.json') as f:
        phones = json.load(f)

    api = twitter.Api(
            consumer_key=keys['apiKey'],
            consumer_secret=keys['apiKeySecret'],
            access_token_key=keys['accessToken'],
            access_token_secret=keys['accessTokenSecret'])

    dcfc_tweets = api.GetUserTimeline(user_id=DCFC_ACCOUNT['id'], include_rts=True, count=10)
    since_id = None
    client = Client(twilio['account_sid'], twilio['auth_token'])

    while True:
        if len(dcfc_tweets) != 0:
            print(f'checking {dcfc_tweets}')
            for tweet in dcfc_tweets:
                text = tweet.text.lower()
                if 'keg' in text and 'roll' in text:
                    print(text)
                    cleaned = re.sub(r'[^\w]', ' ', text)
                    message = client.messages.create(
                        to=phones['to'], 
                        from_=phones['from'],
                        body=cleaned)

            since_id = dcfc_tweets[0].id
        dcfc_tweets = api.GetUserTimeline(user_id=DCFC_ACCOUNT['id'], include_rts=True, since_id=since_id)
        time.sleep(60)


if __name__ == '__main__':
    main()

