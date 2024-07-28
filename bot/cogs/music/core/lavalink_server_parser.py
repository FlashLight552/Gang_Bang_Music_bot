import requests
import re

def lavalink_server_parser():
    link = 'https://raw.githubusercontent.com/DarrenOfficial/lavalink-list/master/docs/NoSSL/lavalink-without-ssl.md'
    r = requests.get(link)
    body = (str(r.text).split('\n'))
    dict_ =  {}
    num = 0
    for i, item in enumerate(body):
        if re.search('Version 4', item):
            for j in range(0,10):
                if re.search('Host', body[i+j]):
                    num = j
                    break

            host = body[i+num].split(' : ')[1].replace('"', '')
            port = body[i+num+1].split(' : ')[1].replace('"', '')
            pw = body[i+num+2].split(' : ')[1].replace('"', '')
            dict_.update({i:{'host':host, 'port':port, 'password': pw}})
    return dict_


