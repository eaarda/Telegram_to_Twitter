import json
import requests
import time
import urllib
import tweepy

import config


TOKEN = config.telegram_bot_api_key
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

user_handler = tweepy.OAuthHandler(config.consumer_key,config.consumer_secret)
user_handler.set_access_token(config.access_token,config.access_token_secret)
api = tweepy.API(user_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
            a = get_last_chat_id_and_text(updates)
            print(a[0])
            api.update_status(status=a[0])
        time.sleep(0.5)
    


if __name__ == '__main__':
    main()