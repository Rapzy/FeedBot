from secret import bot_token, feed_token
from pyrfc3339 import parse
from time import sleep
import requests


def make_url(method):
    url = 'https://api.telegram.org/bot'+bot_token+'/'+method
    return url


def get_feed():
    url = 'https://test.bop.rest/api/feed/'
    token = 'Token '+feed_token
    headers = {'Authorization': token}
    return requests.get(url, headers=headers).json()


class Message:
    def __init__(self):
        url = make_url('getupdates')
        response = requests.get(url).json()

        self.id = response['result'][-1]['update_id']
        self.text = response['result'][-1]['message']['text']
        self.chat = response['result'][-1]['message']['chat']['id']

    def send_response(self):
        method = 'sendmessage?chat_id={}&text={}'
        message = ''
        feed = get_feed()
        for event in feed:
            message += 'Name: {}\n'.format(event['name'])
            message += 'Time: {}\n'.format(parse(event['time']))
            message += 'Id: {}\n'.format(event['id'])
            message += '\n'
        url = make_url(method.format(self.chat, message))
        requests.get(url)


def main():
    last_id = 0
    while True:
        last_message = Message()
        if last_id != last_message.id:
            last_id = last_message.id

            if last_message.text == "/feed":
                last_message.send_response()
        sleep(2)


if __name__ == '__main__':
    main()

