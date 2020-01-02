from selenium import webdriver
import requests
import time
import re
from telethon import TelegramClient
import urllib.request
import asyncio


async def main():
    n = 0

    app_id = 1154776
    app_hash = '0f9a89943dec9626ba314fb564b92672'

    client = TelegramClient('anon', app_id, app_hash)

    await client.start()

    dialogs = await client.get_dialogs()

    tegmo = None

    for dialog in dialogs:
        if dialog.title == 'LTC Click Bot':
            tegmo = dialog

    if not tegmo:
        raise ValueError('Couldn\'t find proper dialog')

    def test_method(required_url, wait):
        capabilities = {'browserName': 'chrome'}
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=capabilities)
        driver.maximize_window()
        driver.get(required_url)
        time.sleep(wait * 10)
        driver.close()
        driver.quit()

    while True:
        messages = await client.get_messages(tegmo, limit=1)

        for message in messages:
            if re.search(r'\bseconds\b', message.message):
                print('Got \'Reward\'')
                message_string = str(message)
                message_string_formatted = message_string.replace('Please stay on the site for at least ', '')
                timeout = message_string_formatted.replace(' seconds...', '')
                waiting = int(timeout)
                print('Timeout set to ', waiting)
                await client.send_message('LTC Click Bot', '/visit')
                time.sleep(3)
                messages2 = await client.get_messages(tegmo, limit=1)

                for message2 in messages2:
                    button_data = message2.reply_markup.rows[0].buttons[0].url
                    message_id = message2.id

                    print('Following the link')
                    time.sleep(2)
                    print(messages[0].reply_markup.rows[0].buttons[0])
                    url_rec = messages[0].reply_markup.rows[0].buttons[0].url
                    test_method(required_url=url_rec, wait=waiting)
                    time.sleep(6)
                    url_opened = urllib.request.urlopen(url_rec)
                    my_bytes = url_opened.read()
                    my_str = my_bytes.decode('utf8')
                    url_opened.close()

                    if re.search(r'\bSwitch to reCAPTCHA\b', my_str):
                        from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
                        response = client(GetBotCallbackAnswerRequest(
                            peer='LTC Click Bot',
                            msg_id=message_id,
                            data=button_data))
                        time.sleep(2)
                        print('CAPTCHA')
                    else:
                        time.sleep(waiting)
                        time.sleep(2)
            elif re.search(r'\bSorry\b', message.message):
                await client.send_message('LTC Click Bot', '/visit')
                time.sleep(6)
                print('Got \'Sorry\'')
            else:
                messages = await client.get_messages('Litecoin_click_bot')
                url_rec = messages[0].reply_markup.rows[0].buttons[0]
                print(url_rec)
                file = open('per10.txt')
                file_content = file.read()
                if file_content == url_rec:
                    print("Variable repetition found")
                    messages2 = await client.get_messages(tegmo, limit=1)
                    for message2 in messages2:
                        button_data = message2.reply_markup.rows[1].buttons[1].data
                        message_id = message2.id
                        from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

                        resp = client(GetBotCallbackAnswerRequest(
                            tegmo,
                            message_id,
                            data=button_data
                        ))
                        time.sleep(2)
                else:
                    url = 'http://www.virustotal.com/vtapi/v2/url/scan'
                    params = {
                        'apiKey': '52aeccedfd225ce06866aba82a68f7465704a44fe173f4da974c5f3d206c057a',
                        'url': url
                    }
                    response = requests.post(url, data=params)
                    my_file = open('per10.txt', 'w')
                    my_file.write(str(url_rec))
                    print('File overwritten')
                    time.sleep(16)
                    n -= - 1
                    print('Cycles completed', n)

asyncio.run(main())
